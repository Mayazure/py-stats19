# stats19
Xiaowei Gao(SpacetimeLab, UCL, UK), Jinshuai Ma(LSE Data Science Institute, UK)
Supervised by Dr. James Haworth and Prof. Tao Cheng to support the digital twins for urban accident

Ported from the [R stats19 package](https://github.com/ropensci/stats19)

## Installation

Download the latest release, e.g. [pystats19-0.0.1-py3-none-any.whl](https://github.com/Mayazure/py-stats19/releases/download/py-stats19-v0.0.1/pystats19-0.0.1-py3-none-any.whl).

```bash
$ pip install pystats19-0.0.1-py3-none-any.whl
```

## list_files()

`list_files()` can list all available stats19 dataset files, which can be simply filtered by passing `year` and `table` arguments.

```python
from pystats19.read import list_files

# List all files contain year 2021 data
list_files(year=2021) 
# ['dft-road-casualty-statistics-casualty-1979-latest-published-year.csv',
#  'dft-road-casualty-statistics-casualty-2021.csv',
#  'dft-road-casualty-statistics-casualty-last-5-years.csv',
#  'dft-road-casualty-statistics-collision-1979-latest-published-year.csv',
#  'dft-road-casualty-statistics-collision-2021.csv',
#  'dft-road-casualty-statistics-collision-last-5-years.csv',
#  'dft-road-casualty-statistics-vehicle-1979-latest-published-year.csv',
#  'dft-road-casualty-statistics-vehicle-2021.csv',
#  'dft-road-casualty-statistics-vehicle-e-scooter-2020-Latest-Published-Year.csv',
#  'dft-road-casualty-statistics-vehicle-last-5-years.csv']

# List all files contain year 2021 and table vehicle data
list_files(year=2021, table="vehicle")
# ['dft-road-casualty-statistics-vehicle-1979-latest-published-year.csv',
#  'dft-road-casualty-statistics-vehicle-2021.csv',
#  'dft-road-casualty-statistics-vehicle-last-5-years.csv']
```

## pull_file()

`pull()` requires `filename` parameter, downloading the data file. `filename` should be obtained using `list_files()`.  

Optionally, `data_dir` can specify the location where the file will be stored.

```python
from pystats19.source import pull_file

pull_file('dft-road-casualty-statistics-vehicle-2019.csv', data_dir="./data")
```
### Data directory

Data directory can also be configured globally by setting an environment variable *PYSTATS19_DOWNLOAD_DIRECTORY*

```bash
$ export PYSTATS19_DOWNLOAD_DIRECTORY=~/my_pystats19_data
```

## load()

`load()` loads the data file as a `pandas.DataFrame` or `geopandas.GeoDataFrame`. Set `auto_download=True` to automatically download the file if not exists. 

Optionally, 

set `convert_code_to_label=True` to convert categorical data codes to text labels.  

set `add_temporal_info=True` to format `datetime` and `time` and add additional time information.

set `add_geo_info=True` to add geo information. This will return a `geopandas.GeoDataFrame`.

```python
from pystats19.read import load

load(
    'dft-road-casualty-statistics-collision-2021.csv',
    auto_download=True,
    convert_code_to_label=True,
    add_temporal_info=True,
    add_geo_info=True
)

# Removed 17 records due to missing Latitude or Longitude.
# 
#        accident_index  ...                       geometry
# 0       2021010287148  ...   POINT (521509.659 193079.41)
# 1       2021010287149  ...  POINT (535380.824 180783.228)
# 2       2021010287151  ...  POINT (529702.828 170398.085)
# 3       2021010287155  ...  POINT (525313.658 178385.183)
# 4       2021010287157  ...  POINT (512145.497 171526.072)
# ...               ...  ...                            ...
# 101082  2021991196247  ...  POINT (325545.894 674547.399)
# 101083  2021991196607  ...  POINT (271195.339 558271.954)
# 101084  2021991197944  ...   POINT (357296.909 860766.24)
# 101085  2021991200639  ...  POINT (326935.908 675924.391)
# 101086  2021991201030  ...  POINT (270574.351 556367.939)
# [101070 rows x 39 columns]
```