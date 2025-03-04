from typing import NamedTuple
from sodapy import Socrata
import os
import pandas as pd
import httpx
import io


class Crime(NamedTuple):
    case_number: str
    latitude: float
    longitude: float
    block: str
    year: int
    date: str
    primary_type: str
    description: str
    puma: None | str
    neighborhood: None | str


def get_crime_data(client, data_set: str, lst_years: list, full_fetch=False) -> list[Crime]:
    """
    Gathers data from an specific dataset from the City of Chicago's Data

    Args:
        - data_set: data set code
        - lst_years: list of years to gather

    Returns: pd.DataFrame with all the records from the data_set in lst_years
    """
    if full_fetch:
        if data_set == "gumc-mgzr":
            results = client.get(data_set, limit=100000000)
            return process_results(results, [])
        else:
            results = [client.get(data_set, year=y, limit=100000000) for y in lst_years]
            return process_results([r for year in results for r in year], [])


def process_results(results, lst_results, full_fetch = False) -> list:

    if full_fetch:
        for row in results:
            if "latitude" in row.keys():
                lst_results.append(
                    Crime(
                        case_number=row["case_number"],
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        block=row["block"],
                        year=int(row["date"][0:4]),
                        date=row["date"],
                        primary_type=row.get("primary_type", "homicide"),
                        description = row.get("description", "-"),
                        puma=None,
                        neighborhood=None,
                    )
                )
    else:
        for _, row in results.iterrows():
            if "latitude" in results.columns and not pd.isna(row["latitude"]):
                lst_results.append(
                    Crime(
                        case_number=row["case_number"],
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        block=row["block"],
                        year=int(str(row["date"])[0:4]),
                        date=row["date"],
                        primary_type=row.get("primary_type", "homicide"),
                        description=row.get("description", "-"),
                        puma=None,
                        neighborhood=None,
                    )
                )
    return lst_results

def get_all_crime_data(full_fetch=False):

    # Creating the pd.Dataframes for crime and homicides_data
    if full_fetch:
        # Creating the APP Key for the data sources.
        try:
            CHICAGO_APP_TOKEN = os.environ["CHICAGO_APP_TOKEN"]
        except KeyError:
            raise Exception(
                "Make sure that you have set the APP Token environment variable as described in the README."
            )

        # Gathering the crime data from the City of Chicago Data web
        client = Socrata("data.cityofchicago.org", CHICAGO_APP_TOKEN, timeout=10)
        crime_code = "ijzp-q8t2"
        homicides_code = "gumc-mgzr"
        lst_years = [2013,2018,2023]
    
        crime_data = get_crime_data(client, crime_code, lst_years)
        homicides_data = get_crime_data(client, homicides_code, lst_years)

        crime_df = pd.DataFrame(crime_data)
        crime_df.to_csv("data/crime_df.csv", index=False)
        
        homicides_df = pd.DataFrame(homicides_data)
        homicides_df.to_csv("data/homicides_df.csv", index=False)

        return crime_data , homicides_data
    
    else:

    # Original Google Drive share link (VIEW link)
        dict_paths = {'crime' : 'https://drive.usercontent.google.com/download?id=1czf5w2gz8pp2_eQVHQ0XyFcABfHKLY3v&export=download&authuser=0&confirm=t&uuid=85720b0a-11ba-40c7-ab60-284e86d84892&at=AEz70l5d2KfQCDFLMMX9tZE7HLDr:1741110765742',
                      'homicide': 'https://drive.usercontent.google.com/download?id=1wMsC1pNPm2Fr4SOuokAww9nClSlkGp0o&export=download&authuser=0&confirm=t&uuid=3cf0b2aa-7c0d-448f-9c3a-97e9d849ba69&at=AEz70l6AnERF72xb7U0TNg84Wf5U:1741110822006'}
        
        data_lists = []
        for type, path in dict_paths.items():

            # Fetch the raw CSV data from Google Drive
            response = httpx.get(path, follow_redirects=True)

            # Check that we got a valid 200 OK
            if response.status_code != 200:
                # Debug: print the first part of the error text
                print("Response text (first 500 chars):", response.text[:500])
                raise RuntimeError(f"Error fetching file (status={response.status_code}).")

            # Convert the response text into a file-like object
            text_buffer = io.StringIO(response.text)

            # Read the CSV contents
            df = pd.read_csv(text_buffer)
            data_lists.append(process_results(df,[],full_fetch))

        return data_lists[0] , data_lists[1]
    
if __name__ == '__main__':
    get_all_crime_data(True)