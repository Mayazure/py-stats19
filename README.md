# stats19

Ported from the [R stats19 package](https://github.com/ropensci/stats19)

## list_files()

`list_files()` can list all available stats19 dataset files, which can be simply filtered by passing `years` and `type_` arguments.

```python
from pystats19.source import list_files

list_files(years=2021)
 
# ['dft-road-casualty-statistics-casualty-2021.csv',
#  'dft-road-casualty-statistics-vehicle-2021.csv',
#  'dft-road-casualty-statistics-collision-2021.csv']

list_files(years=range(2019,2023), type_="vehicle")

# ['dft-road-casualty-statistics-vehicle-2022.csv',
#  'dft-road-casualty-statistics-vehicle-e-scooter-2020-Latest-Published-Year.csv',
#  'dft-road-casualty-statistics-vehicle-2020.csv',
#  'dft-road-casualty-statistics-vehicle-2021.csv',
#  'dft-road-casualty-statistics-vehicle-2019.csv']
```

## pull()

`pull()` requires `filename` parameter, downloading the data file. `filename` should be obtained using `list_files()`.  

Optionally, `data_dir` can specify the location where the file will be stored.

```python
from pystats19.source import pull

pull('dft-road-casualty-statistics-vehicle-2019.csv', data_dir="./data")
```

## load()

`load()` loads the data file as a `pandas.DataFrame`. Set `auto_download` to `True` to automatically download the file if not exists. Set `format_` to `True` to format the data.

```python
from pystats19.source import load

load(
    'dft-road-casualty-statistics-vehicle-2019.csv', 
    data_dir="./data",
    format_=True,
    auto_download=True
)

#        accident_index  accident_year  ... driver_home_area_type  lsoa_of_driver
# 0       2019010128300           2019  ...            Urban area              -1
# 1       2019010128300           2019  ...            Urban area              -1
# 2       2019010152270           2019  ...            Urban area              -1
# 3       2019010152270           2019  ...            Urban area              -1
# 4       2019010155191           2019  ...            Urban area              -1
# ...               ...            ...  ...                   ...             ...
# 216376  2019984107019           2019  ...                 Rural              -1
# 216377  2019984107219           2019  ...            Small town              -1
# 216378  2019984107219           2019  ...                 Rural              -1
# 216379  2019984107419           2019  ...                 Rural              -1
# 216380  201998QC01004           2019  ...            Urban area              -1
```