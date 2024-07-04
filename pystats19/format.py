import re

import pandas as pd
from typing import Iterable

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


def format_stats19(df: pd.DataFrame, type_):
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
