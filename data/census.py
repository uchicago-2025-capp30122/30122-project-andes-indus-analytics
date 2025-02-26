import csv
import json
import os
import sys
from pathlib import Path
import pandas as pd
import httpx

params = {"get": "SEX,PUMA,RACBLK,AGEP,HISP,FHISP,PWGTP,SCH,ESR,HINCP,ADJINC,SCHG,SCHL"} # variables to get
url = "https://api.census.gov/data/2021/acs/acs1/pums"

class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )

def combine_url_with_params(url, params):
    """
    Use httpx.URL to create a URL joined to its parameters, suitable for use.
    we dont need key for this query

    Parameters:
        - url: a URL with or without parameters already
        - params: a dictionary of parameters to add

    Returns:
        The URL with parameters added, for example:

        >>> combine_url_with_params(
            "https://example.com/api/",
            {"api_key": "abc", "page": 2}
        )
        "https://example.com/api/?api_key=abc&page=2"
    """
    url = httpx.URL(url)
    merged_params  = dict(url.params) | params  # merge the dictionaries
    encoded_url = str(url.copy_with(params=merged_params))
    return encoded_url.replace("%2C", ",")

def cached_get(url) -> dict:
    """
    This function caches all GET requests it makes by writing
    the successful responses to disk.
    """
    full_url = combine_url_with_params(url, params)  # Ensure 'params' is defined in your context.
    
    try:
        response = httpx.get(full_url, follow_redirects=False, timeout=10000.0)
    except httpx.ReadTimeout as exc:
        # Log the error or handle it as needed.
        raise FetchException(f"Request to {full_url} timed out") from exc

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise FetchException(response)
    
START_URL = "https://api.census.gov/data/2021/acs/acs1/pums"
CSV_COLUMNS = ("STATE","SEX","PUMA","RACBLK","AGEP","HISP","FHISP","PWGTP","SCH","ESR","HINCP","ADJINC","SCHG","SCHL")



def build_census_csv(output_filename: Path):
    """
    Create a CSV file populated with the following columns:

    - `state`   - State
    - `sex`     - sex of the informant.
    - `PUMA`    - Public Use Microdata Area.
    - `RACBLK`  - Race = Black.
    - `HISP`    - Race = Hispanic.
    - `AGEP`    - Population age.
    - `FHISP`   - URL of the API call that returned this record.
    - `PWGTP`   - URL of the API call that returned this record.
    - `SCH`     - School enrollment.
    - `ESR`     - URL of the API call that returned this record.
    - `HINCP`   - Household income (past 12 months, use ADJINC to 
                adjust HINCP to constant dollars)
    - `SCHG` -  Grade level attending
    - `SCHL` -  Education attainment

    Parameters:
        output_filename: Path object representing location to write file.
    """  
    new_url = START_URL


    data = cached_get(new_url)
 # Convert to DataFrame if data is available
    if data:
        df = pd.DataFrame(data[1:], columns=data[0])  # First row is headers
        print(df.head())  # Print the first few rows for a quick look

        # Write the DataFrame to a CSV file
        df.to_csv(output_filename, index=False)
        print(f"CSV file created at: {output_filename}")
    else:
        print("No data available")

if __name__ == "__main__":
    build_census_csv("output_filename.csv")
