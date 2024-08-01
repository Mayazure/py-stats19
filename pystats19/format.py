import pandas as pd
import geopandas as gpd
from shapely import Point

from pystats19 import stats19_code_label_map, logger


def convert_code_to_label(df: pd.DataFrame, table=None) -> pd.DataFrame:
    """Convert categorical class ids to labels

    :param pd.DataFrame df: The main DataFrame
    :param str table: one of ['Accident', 'Vehicle', 'e_scooter', 'Casualty', 'historical_revisions',
     'collision_adjustment','casualty_adjustment']. If None will infer from the data
    :return: DataFrame with categorical class id converted to text labels
    """
    table_code_label_map = stats19_code_label_map.get(table)
    if table_code_label_map is None:
        return df

    for name in df.columns:
        mapping = table_code_label_map.get(name)
        if mapping is not None:
            try:
                df[name] = df[name].apply(lambda x: mapping.get(x, pd.NA))
            except Exception:
                logger.warn(f"Cannot convert {name}. Skipped.")
    return df


season_mapping = {
    3: "spring",
    4: "spring",
    5: "spring",
    6: "summer",
    7: "summer",
    8: "summer",
    9: "autumn",
    10: "autumn",
    11: "autumn",
    12: "winter",
    1: "winter",
    2: "winter",
}

weekday_mapping = {
    0: "weekday",
    1: "weekday",
    2: "weekday",
    3: "weekday",
    4: "weekday",
    5: "weekend",
    6: "weekend",
}


def when_was_it(hour):
    if 7 <= hour < 10:
        return "morning rush (7-10)"
    elif 10 <= hour < 16:
        return "office hours (10-16)"
    elif 16 <= hour < 19:
        return "afternoon rush (16-19)"
    elif 19 <= hour < 23:
        return "evening (19-23)"
    else:
        return "night (23-7)"


def add_temporal_info(df: pd.DataFrame) -> pd.DataFrame:
    """Add additional temporal columns to the dataframe.

    The data column must be presented and is in the following format: %d/%m/%Y.
    Optionally,

    :param pd.DataFrame df: The main DataFrame.
    :return: DataFrame with additional temporal columns.
    """
    columns = df.columns

    if "date" in columns and "time" in columns:
        df['datetime'] = df.apply(lambda x: f"{x['date']} {x['time']}", axis=1)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%Y %H:%M", errors="coerce")
        df['daytime'] = df['datetime'].dt.hour.apply(when_was_it)
    elif "date" in columns and "time" not in columns:
        df['datetime'] = pd.to_datetime(df['date'], format="%d/%m/%Y")
    else:
        logger.warn("Column date not found. Temporal data not added.")

    if "datetime" in columns:
        df['day_of_year'] = df['datetime'].dt.dayofyear
        df["season"] = df["datetime"].apply(lambda x: season_mapping[x.month])
        df['month'] = df['datetime'].dt.month
        df['weekday'] = df['datetime'].apply(lambda x: weekday_mapping[x.dayofweek])

    return df


def add_geo_info(df: pd.DataFrame, crs="EPSG:4326", epsg=27700) -> gpd.GeoDataFrame | pd.DataFrame:
    """Convert DataFrame to GeoDataFrame with formatted geo info.

    DataFrame without latitude and longitude columns will be ignored and original DataFrame will be returned.
    Rows with null latitude or longitude value will be removed.

    :param df: the main DataFrame
    :param crs: CRS code
    :param epsg: EPSG code
    :return: GeoDataFrame with formatted geo info
    """
    if "longitude" not in df.columns or "latitude" not in df.columns:
        logger.warn("Column longitude or latitude not found. Geo info not added.")
        return df
    df_no_coordinates = df[(df["longitude"].isna()) | (df["latitude"].isna())]
    n_no_coordinates = df_no_coordinates.shape[0]
    if n_no_coordinates > 0:
        logger.warn(f"Removed {n_no_coordinates} records due to missing Latitude or Longitude.")
    df = df[~((df["longitude"].isna()) | (df["latitude"].isna()))]
    df = df.assign(
        geometry=df[["longitude", "latitude"]].apply(
            lambda row: Point(row['longitude'], row['latitude']), axis=1)
    )

    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=crs)
    gdf = gdf.to_crs(epsg=epsg)
    return gdf
