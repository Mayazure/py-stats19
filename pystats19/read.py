import os
from urllib.error import HTTPError

import pandas as pd
import geopandas as gpd

from pystats19 import stats19_data_files, options, stats19_file_table, stats19_table_dtype, logger, stats19_file_year
from pystats19.source import pull_file
import pystats19.format as formatter
from pystats19.utils import replace_pd_dtype

table_mapping = {
    "accident": "Accident",
    "Accident": "Accident",
    "collision": "Accident",
    "Collision": "Accident",
    "casualty": "Casualty",
    "Casualty": "Casualty",
    "vehicle": "Vehicle",
    "Vehicle": "Vehicle",
    "e_scooter": "e_scooter",
    "E_scooter": "e_scooter"
}


def list_files(year: int = None, table: str = None):
    """List all available data files.

    :param year: Year of the data.
    :param table: Table. One of ("accident", "collisions", "casualty", "vehicle", "e_scooter")
    :return:
    """
    table_index = stats19_file_table
    year_index = stats19_file_year

    filenames = stats19_data_files

    if table is not None:
        if type(table) is not str:
            raise TypeError("Table must be a string.")

        if table not in table_mapping.keys():
            logger.warning(f"Skipped invalid table: {table}")
            return []
        table = table_mapping[table]
        filenames = [k for k, v in table_index.items() if v == table]

    if year is not None:
        if type(year) is not int:
            raise TypeError("Year must be an integer.")
        filenames = [k for k, v in year_index.items() if year in v and k in filenames]

    filenames.sort()
    return filenames


def load(
        filename: str,
        data_dir=options.data_directory,
        auto_download: bool = False,
        convert_code_to_label: bool = False,
        add_temporal_info: bool = False,
        add_geo_info: bool = False,
        **override_pandas_kwargs
) -> pd.DataFrame | gpd.GeoDataFrame:
    """Load a specific data file.

    :param filename: The filename of the file to load. Can be acquired from list_files().
    :param data_dir: The directory where to search for the file.
    :param auto_download: Whether to download the file if not exist locally.
    :param convert_code_to_label: Whether to convert class code to labels for categorical column.
    :param add_temporal_info: Whether to add additional temporal information.
    :param add_geo_info: Whether to add geo information.
    :return: A DataFrame or GeoDataFrame if format_geo_info is True, with specified formatting.
    """
    local_filepath = os.path.join(data_dir, filename)
    if not os.path.exists(local_filepath):
        if auto_download:
            try:
                pull_file(filename, data_dir=data_dir)
            except HTTPError as e:
                if e.code == 404:
                    raise ValueError(
                        f"{filename} is not a valid filename. Call list_files() to get a list of valid filenames."
                    )
        else:
            raise FileNotFoundError(
                f"{filename}. Call pull_file('{filename}') or set auto_download to True to download."
            )
    table_dtype = None
    file_table = stats19_file_table.get(filename)
    if file_table is not None:
        table_dtype = stats19_table_dtype.get(file_table)
        if table_dtype is not None:
            table_dtype = replace_pd_dtype(table_dtype)
    df = pd.read_csv(local_filepath, dtype=table_dtype, **override_pandas_kwargs)
    if convert_code_to_label:
        df = formatter.convert_code_to_label(df, file_table)
    if add_temporal_info:
        df = formatter.add_temporal_info(df)
    if add_geo_info:
        df = formatter.add_geo_info(df)
    return df


def na_ratio(df: pd.DataFrame) -> pd.Series:
    return df.isnull().mean().sort_values(ascending=False).rename("na ratio").loc[lambda x: x > 0]
