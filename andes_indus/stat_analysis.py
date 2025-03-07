from .api_get import build_census_csv, chicago_dataframe
import pandas as pd
import time

def append_microdata():

    df = pd.DataFrame()
    for year in [2013,2023]:
        df = pd.concat([df, chicago_dataframe(year, '', False)])
    return df

def merge_census_crime():
    df = append_microdata()

    return df 
