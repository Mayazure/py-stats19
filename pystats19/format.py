import re
import warnings

import pandas as pd
import geopandas as gpd
from typing import Iterable

from shapely import Point

from pystats19 import stats19_schema


def get_code_to_label_mapping(table, formatted_variable):
    df_codes = stats19_schema[
        (stats19_schema["table"] == table) & (stats19_schema["variable_formatted"] == formatted_variable)
        ]
    if df_codes.shape[0] > 0:
        return df_codes[["code", "label"]].set_index("code").to_dict("dict")["label"]


def format_column_name(name: str) -> str:
    x = name.lower()
    x = x.replace(' ', '_')
    # x = re.sub("\\(|\\)", "", x)
    x = x.replace("(", "")
    x = x.replace(")", "")
    x = x.replace('1st', 'first')
    x = x.replace('2nd', 'second')
    x = x.replace('-', '_')
    x = re.sub("\\?", "", x)
    return x


def format_column_names(column_names: Iterable[str]) -> list[str]:
    return [format_column_name(x) for x in column_names]


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


def na_ratio(df: pd.DataFrame) -> pd.Series:
    return df.isnull().mean().sort_values(ascending=False).rename("na ratio").loc[lambda x: x > 0]


def add_temporal_info(df: pd.DataFrame) -> pd.DataFrame:
    """Add additional temporal columns to the dataframe.

    The data column must be presented and is in the following format: %d/%m/%Y.
    Optionally,

    :param df: The main DataFrame.
    :return: DataFrame with additional temporal columns.
    """
    columns = df.columns

    if "date" in columns and "time" in columns:
        df['datetime'] = df.apply(lambda x: f"{x['date']} {x['time']}", axis=1)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%Y %H:%M")
        df['daytime'] = df['datetime'].dt.hour.apply(when_was_it)
    elif "date" in columns and "time" not in columns:
        df['datetime'] = pd.to_datetime(df['date'], format="%d/%m/%Y")
    else:
        warnings.warn("Date not found. DataFrame not formatted.")

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
    # TODO Should we add a flag to let user to choose whether to exclude null value rows?

    if "longitude" not in df.columns or "latitude" not in df.columns:
        warnings.warn("Longitude or Latitude columns not found. DataFrame not formatted.")
        return df
    df_no_cordinates = df[(df["longitude"].isna()) | (df["latitude"].isna())]
    n_no_cordinates = df_no_cordinates.shape[0]
    if n_no_cordinates > 0:
        warnings.warn(f"Removed {n_no_cordinates} records due to missing Latitude or Longitude.")
    df = df[~((df["longitude"].isnull()) | (df["latitude"].isnull()))]
    df['geometry'] = df[["longitude", "latitude"]].apply(
        lambda row: Point(row['longitude'], row['latitude']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=crs)
    gdf = gdf.to_crs(epsg=epsg)
    return gdf


def convert_id_to_label(df: pd.DataFrame, type_) -> pd.DataFrame:
    """Convert categorical class ids to labels

    :param df: The main DataFrame
    :param type_: one of ("collisions", "casualty", "vehicle")
    :return: DataFrame with class id converted to label
    """
    old_names = df.columns
    new_names = format_column_names(old_names)
    names_mapping = dict(zip(old_names, new_names))
    df.rename(columns=names_mapping, inplace=True)
    for name in new_names:
        mapping = get_code_to_label_mapping(type_, name)
        if mapping is not None:
            try:
                df[name] = df[name].apply(lambda x: mapping.get(x, pd.NA))
            except Exception as e:
                print(name)
                raise e
    return df
