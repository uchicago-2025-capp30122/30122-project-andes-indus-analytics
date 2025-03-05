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
                        puma=row.get("puma", None),
                        neighborhood=row.get("neighborhood", None),
                    )
                )
    return lst_results

def get_all_crime_data():

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

def load_crime_data():

    # Original Google Drive share link (VIEW link)
    dict_paths = {'crime_by_puma' : 'https://drive.usercontent.google.com/download?id=1JUDBpR3ot26PW-2F93pLGkIbZy7dFpF7&export=download&authuser=0&confirm=t&uuid=26c3238d-a65a-449f-a6c0-9195dec5f1b8&at=AEz70l6g5TH5Nh_sh4o71wbuDkur:1741115211114',
                    'crime_by_neighborhood': 'https://drive.usercontent.google.com/download?id=1dUEmZnPna1hQv55Czi38KYIv4Z6oHcZy&export=download&authuser=0&confirm=t&uuid=47ca72e8-6681-453e-8eae-0f6e4730a14d&at=AEz70l5OzlGvfrEsZ2JLIPiaY653:1741115182166'}
    
    data_lst = []
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
        data_lst.append(df)

    return data_lst[0] , data_lst[1]
    
if __name__ == '__main__':
    get_all_crime_data()