import os
import pandas as pd
from importlib.resources import path

from pathlib import Path

DEFAULT_DOWNLOAD_DIRECTORY = Path.home() / ".stats19"

DEFAULT_SOURCE_DOMAIN = "https://data.dft.gov.uk"
DEFAULT_SOURCE_DIRECTORY = "road-accidents-safety-data"

PREFIX = "dft-road-casualty-statistics-"

FILE_NAMES = [
    "dft-road-casualty-statistics-casualty-adjustment-lookup_2004-latest-published-year.csv",
    "dft-road-casualty-statistics-collision-adjustment-lookup_2004-latest-published-year.csv",
    "dft-road-casualty-statistics-vehicle-e-scooter-2020-Latest-Published-Year.csv",
    "dft-road-casualty-statistics-historical-revisions-data.csv",
    "dft-road-casualty-statistics-casualty-2022.csv",
    "dft-road-casualty-statistics-vehicle-2022.csv",
    "dft-road-casualty-statistics-collision-2022.csv",
    "dft-road-casualty-statistics-casualty-1979-latest-published-year.csv",
    "dft-road-casualty-statistics-vehicle-1979-latest-published-year.csv",
    "dft-road-casualty-statistics-collision-1979-latest-published-year.csv",
    "dft-road-casualty-statistics-casualty-2021.csv",
    "dft-road-casualty-statistics-vehicle-2021.csv",
    "dft-road-casualty-statistics-collision-2021.csv",
    "dft-road-casualty-statistics-casualty-2020.csv",
    "dft-road-casualty-statistics-vehicle-2020.csv",
    "dft-road-casualty-statistics-collision-2020.csv",
    "dft-road-casualty-statistics-casualty-2019.csv",
    "dft-road-casualty-statistics-vehicle-2019.csv",
    "dft-road-casualty-statistics-collision-2019.csv",
    "dft-road-casualty-statistics-casualty-2018.csv",
    "dft-road-casualty-statistics-vehicle-2018.csv",
    "dft-road-casualty-statistics-collision-2018.csv",
    "dft-road-casualty-statistics-casualty-last-5-years.csv",
    "dft-road-casualty-statistics-vehicle-last-5-years.csv",
    "dft-road-casualty-statistics-collision-last-5-years.csv",
]


class Option:
    timeout = 60
    data_directory = os.environ.get(
        "STATS19_DOWNLOAD_DIRECTORY",
        DEFAULT_DOWNLOAD_DIRECTORY
    )


option = Option()

# print(option.data_directory)


with path("pystats19.data", "stats19_variables.pkl") as p:
    stats19_variables = pd.read_pickle(p)

with path("pystats19.data", "stats19_schema.pkl") as p:
    stats19_schema: pd.DataFrame = pd.read_pickle(p)

with path("pystats19.data", "file_names.pkl") as p:
    file_names = pd.read_pickle(p)
