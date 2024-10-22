import logging
import os
import pandas as pd
from logging import getLogger
from pathlib import Path
from importlib.resources import as_file, files

DEFAULT_DOWNLOAD_DIRECTORY = Path.home() / ".stats19"


class Option:

    @property
    def data_directory(self):
        return os.environ.get(
            "PYSTATS19_DOWNLOAD_DIRECTORY",
            DEFAULT_DOWNLOAD_DIRECTORY
        )


options = Option()

with as_file(files("pystats19.data").joinpath("pystats19_prebuilt_schema.pkl")) as f:
    stats19_prebuilt_index = pd.read_pickle(f)
    stats19_data_files = stats19_prebuilt_index["STATS19_DATA_FILES"]
    stats19_adjustment_files = stats19_prebuilt_index["STATS19_ADJUSTMENT_FILES"]
    stats19_dataguide_files = stats19_prebuilt_index["STATS19_DATAGUIDE_FILE"]
    stats19_schema = stats19_prebuilt_index["STATS19_PREBUILT_SCHEMA"]
    stats19_dataguide = stats19_prebuilt_index["STATS19_DATAGUIDE"]
    stats19_file_table = stats19_prebuilt_index["STATS19_FILE_TABLE"]
    stats19_table_dtype = stats19_prebuilt_index["STATS19_TABLE_DTYPE"]
    stats19_file_year = stats19_prebuilt_index["STATS19_FILE_YEAR"]
    stats19_code_label_map = stats19_prebuilt_index["STATS19_CODE_LABEL_MAP"]
    stats19_source_domain = stats19_prebuilt_index["STATS19_SOURCE_DOMAIN"]
    stats19_source_directory = stats19_prebuilt_index["STATS19_SOURCE_DIRECTORY"]

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
