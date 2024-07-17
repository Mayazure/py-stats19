import os.path
import warnings
from typing import Iterable

import pandas as pd
import geopandas as gpd

from pystats19 import option, FILE_NAMES
from pystats19.dl import dl_stats19
from pystats19.format import convert_id_to_label, add_temporal_info, add_geo_info

types = ("collisions", "casualty", "vehicle")


def list_files(years: int | Iterable[int] = None, type_: str = None):
    if type(years) is int:
        years = [years]
    if type_ is not None:
        # Assume filenames are all in lower case
        type_ = type_.lower()
        if type_ not in types:
            raise ValueError("type_ must be one of {}".format(types))

    result = FILE_NAMES
    if years is not None:
        if min(years) >= 2016:
            result = list(filter(lambda x: x.find("1979") <= 0, result))
        result = list(filter(lambda x: x.find("adjust") <= 0, result))
        result = list(filter(lambda x: any([x.find(str(y)) >= 0 for y in years]), result))
        result = result

    if type_ is not None:
        type_ = type_.replace("cas", "ics-cas")
        result_type = list(filter(lambda x: x.find(type_) >= 0, result))
        if len(result_type) > 0:
            result = result_type
        else:
            if years is None:
                warnings.warn("No files of that type found")
                return []
            else:
                warnings.warn("No files of that type found for that year.")
                # raise ValueError("No files of that type found for that year.")
                return []

    if len(result) < 1:
        warnings.warn("No files found. Check the stats19 website on data.gov.uk")

    return list(set(result))


def pull(
        filename: str,
        data_dir=option.data_directory
):
    dl_stats19(data_dir=data_dir, file_name=filename)


def detect_type(filename: str):
    if filename.find("vehicle") >= 0:
        return "Vehicle"
    if filename.find("collision") >= 0:
        return "Accident"
    else:
        return "Casualty"


def load(
        filename: str,
        data_dir=option.data_directory,
        auto_download: bool = False,
        format_label: bool = True,
        format_temporal_info: bool = False,
        format_geo_info: bool = False,
) -> pd.DataFrame | gpd.GeoDataFrame:

    local_filepath = os.path.join(data_dir, filename)
    if not os.path.exists(local_filepath):
        if auto_download:
            pull(filename, data_dir=data_dir)
        else:
            raise FileNotFoundError(local_filepath)
    df = pd.read_csv(local_filepath)
    if format_label:
        df = convert_id_to_label(df, detect_type(filename))
    if format_temporal_info:
        df = add_temporal_info(df)
    if format_geo_info:
        df = add_geo_info(df)
    return df
