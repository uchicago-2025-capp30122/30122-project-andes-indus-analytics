from typing import NamedTuple
from sodapy import Socrata
import os
import pandas as pd
import httpx
import io
import numpy as np
from api_get import get_google_drive_files

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


def get_crime_data(
    client, data_set: str, lst_years: list, full_fetch=False
) -> list[Crime]:
    """
    Gathers data from an specific dataset from the City of Chicago's Data

    Args:
        - data_set: data set code
        - lst_years: list of years to gather

    Returns: 
    """
    if full_fetch:
        if data_set == "gumc-mgzr":
            results = client.get(data_set, limit=100000000)
            return process_results(results, [], full_fetch)
        else:
            results = [client.get(data_set, year=y, limit=100000000) for y in lst_years]
            return process_results(
                [r for year in results for r in year], [], full_fetch
            )


def process_results(results, lst_results, full_fetch=False) -> list:
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
                        description=row.get("description", "-"),
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
    client = Socrata("data.cityofchicago.org", CHICAGO_APP_TOKEN)
    crime_code = "ijzp-q8t2"
    homicides_code = "gumc-mgzr"
    lst_years = [2013, 2018, 2023]

    crime_data = get_crime_data(client, crime_code, lst_years, True)
    homicides_data = get_crime_data(client, homicides_code, lst_years, True)

    crime_df = pd.DataFrame(crime_data)
    mask1_1 = crime_df["primary_type"] == "HOMICIDE"
    mask1_2 = crime_df["primary_type"] == "ROBBERY"
    mask1_3 = crime_df["primary_type"] == "CRIMINAL SEXUAL ASSAULT"
    mask2 = crime_df["primary_type"] == "ASSAULT"
    mask3 = crime_df["description"].str.startswith("AGGRAVATED")
    crime_df["crime_type"] = np.where(
        (mask1_1 | mask1_2 | mask1_3) | (mask2 & mask3), "Violent", "Non-violent"
    )

    crime_df.to_csv("data/crime_df.csv", index=False)

    homicides_df = pd.DataFrame(homicides_data)
    homicides_df.to_csv("data/homicides_df.csv", index=False)

    return crime_data, homicides_data


def load_crime_data():
    # Original Google Drive share link (VIEW link)
    dict_paths = {
        "crime_by_puma": "https://drive.usercontent.google.com/download?id=1JUDBpR3ot26PW-2F93pLGkIbZy7dFpF7&export=download&authuser=0&confirm=t&uuid=26c3238d-a65a-449f-a6c0-9195dec5f1b8&at=AEz70l6g5TH5Nh_sh4o71wbuDkur:1741115211114",
        "crime_by_neighborhood": "https://drive.usercontent.google.com/download?id=1dUEmZnPna1hQv55Czi38KYIv4Z6oHcZy&export=download&authuser=0&confirm=t&uuid=47ca72e8-6681-453e-8eae-0f6e4730a14d&at=AEz70l5OzlGvfrEsZ2JLIPiaY653:1741115182166",
    }

    data_lst = []
    for _, path in dict_paths.items():

        # Read the CSV contents
        df = get_google_drive_files(path)
        data_lst.append(df)

    return data_lst[0], data_lst[1]


def load_crimes_shp():
    path = 'https://drive.usercontent.google.com/download?id=17lrQgaXcTAQTM4kMqt19RYvC4gtF9wCn&export=download&authuser=0&confirm=t&uuid=f69248de-b684-4c5f-976b-63576e8c9741&at=AEz70l53DiY7nTnR_fRZmhZYPvOx:1741223440221'

    # Saved to a DataFrame
    data = get_google_drive_files(path)
    
    block_data = data.groupby(['block', 'year','crime_type']).agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            count=("case_number", "count"),
        ).reset_index()

    return block_data


if __name__ == "__main__":
    get_all_crime_data()
