import pandas as pd
from sodapy import Socrata
from datetime import datetime
import os 

# Creating the client with credentials safely. 
try:
    APP_TOKEN = os.environ["APP_TOKEN"]
except KeyError:
    raise Exception(
        "Make sure that you have set the APP Token environment variable as described in the README."
    )

client = Socrata("data.cityofchicago.org", APP_TOKEN, timeout=10)

# Establishing the data sets' code and years
crime_data = "ijzp-q8t2"
homicides_data = "gumc-mgzr"
lst_years = list(range(2021, 2024))

def get_data(data_set: str, lst_years: list) -> pd.DataFrame:
    '''
    Gathers data from an specific dataset from the City of Chicago's Data 

    Args:
        - data_set: data set code
        - lst_years: list of years to gather
    
    Returns: pd.DataFrame with all the records from the data_set in lst_years
    '''
    if data_set == "gumc-mgzr":
        results = client.get_all(data_set)
        results_df = pd.DataFrame.from_records(results)
        results_df["year"] = pd.to_datetime(results_df["date"]).dt.year.astype(int)
        results_df = results_df[results_df["year"].isin(lst_years)]
    else:
        results_df = pd.DataFrame()
        for y in lst_years:
            results = client.get(data_set, year=y)
            results = pd.DataFrame.from_records(results)
            results_df = pd.concat((results_df, results))
        results_df["year"] = pd.to_datetime(results_df["date"]).dt.year.astype(int)

    return results_df

def get_missings(df: pd.DataFrame) -> pd.Series:
    """
    Helper function that returns a pd.Series that allocates the percentage of
    missing values in each variable in a pd.DataFrame, but only for the variables
    that has at least one missing value.
    """
    missings = df.isna().sum() / len(df)
    missings = missings[missings != 0]
    return pd.Series(missings)
 
def look_for_missings(data_set: str, lst_years: list) -> pd.DataFrame:
    '''
    Generates a yearly table of missings values for each variable that has at 
    least one missing value in the period of analysis
    
    Args:
        - data_set: data set code
        - lst_years: list of years to gather
    
    Returns: pd.DataFrame with the percentage of missing values in the dataframe
    '''
    results_df = get_data(data_set, lst_years)
    final_df = {}

    for year in lst_years:
        year_df = results_df[results_df["year"] == year]
        final_df[year] = get_missings(year_df)

    return pd.DataFrame(final_df)