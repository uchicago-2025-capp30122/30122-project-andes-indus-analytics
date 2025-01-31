import pandas as pd
from sodapy import Socrata
from datetime import datetime

# Creating the client with credentials. Here we should put the APP Token in the 
# envieronment so we don't show it in the code.
client = Socrata(
        "data.cityofchicago.org",
        "Eqk9pQsM8RsYYawwjwyFUTlYj",
        timeout=10
    )

# 
crime_data = "ijzp-q8t2"
homicides_data = "gumc-mgzr"
lst_years = list(range(2020,2026))

def get_missings(df: pd.DataFrame) -> pd.Series:
    '''
    Helper function that returns a pd.Series that allocates the percentage of 
    missing values in each variable in a pd.DataFrame, but only for the variables
    that has at least one missing value.
    '''
    missings = df.isna().sum() / len(df)
    missings = missings[missings!=0]
    return pd.Series(missings)

def look_for_missings(data_set: str, lst_years: list, limit: int) -> pd.DataFrame:

    if data_set == "gumc-mgzr":
        results = client.get_all(data_set)
        results_df = pd.DataFrame.from_records(results)
        results_df['year'] = pd.to_datetime(results_df['date']).dt.year.astype(int)
        
        final_df = {}
        for y in lst_years:
            y_df = results_df[results_df['year'] == y]
            
            final_df[y] = get_missings(y_df)
        
        return pd.DataFrame(final_df)

    else:
        final_df = {}
        for y in lst_years:
            results = client.get(data_set, year = y, limit = limit)

            # Convert to pandas DataFrame
            results_df = pd.DataFrame.from_records(results)
            
            final_df[y] = get_missings(results_df)

        return pd.DataFrame(final_df)