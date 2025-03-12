from pathlib import Path
import pandas as pd
import httpx
import time
import io

YEAR = [2013, 2018, 2023]


class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


def get_params_for_year(year: int) -> dict:
    """
    Returns the correct 'params' dictionary for the given ACS PUMS year.
    """
    if year == 2023:
        return {
            "get": "STATE,SEX,PUMA,RACBLK,AGEP,HISP,FHISP,PWGTP,SCH,ESR,"
            "HINCP,ADJINC,SCHG,SCHL,NP,WORKSTAT,HHT"
        }
    else:
        # Default parameters for other years
        return {
            "get": "ST,SEX,PUMA,RACBLK,AGEP,HISP,FHISP,PWGTP,SCH,ESR,"
            "HINCP,ADJINC,SCHG,SCHL,NP,WORKSTAT,HHT"
        }


def combine_url_with_params(url, query_params):
    """
    Use httpx.URL to create a URL joined to its parameters, suitable for use.
    we dont need key for this query

    Parameters:
        - url: a URL with or without parameters already
        - query_params: a dictionary of parameters to add

    Returns:
        The URL with parameters added, for example:

        combine_url_with_params(
            "https://example.com/api/",
            {"api_key": "abc", "page": 2}
        )
        "https://example.com/api/?api_key=abc&page=2"
    """
    url = httpx.URL(url)
    merged = dict(url.params) | query_params  # merge
    encoded_url = str(url.copy_with(params=merged))
    return encoded_url.replace("%2C", ",")


def cached_get(url, query_params) -> dict:
    """
    This function caches all GET requests it makes by writing
    the successful responses to disk.
    """

    full_url = combine_url_with_params(
        url, query_params
    )  # Ensure 'params' is defined in your context.
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


def build_census_csv(year, output_filename):
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
    - `WORKSTAT' - work status householder
    - `HHT  -   `Household type'

    Parameters:
        output_filename: Path object representing location to write file.
    """

    START_URL = f"https://api.census.gov/data/{year}/acs/acs1/pums"
    query_params = get_params_for_year(year)

    data = cached_get(START_URL, query_params)
    # Convert to DataFrame if data is available
    if data:
        df = pd.DataFrame(data[1:], columns=data[0])  # First row is headers
        # return df
        # Write the DataFrame to a CSV file
        df.to_csv(output_filename, index=False)
    else:
        print(f"No data available for {year}")


def read_csv_census(text):
    return [line.split(",") for line in text.split("\n")]  # this is intended for 2018


def get_google_drive_files(path) -> pd.DataFrame:
    # Fetch the raw CSV data from Google Drive
    response = httpx.get(path, follow_redirects=True)

    # Check that we got a valid 200 OK
    if response.status_code != 200:
        # Debug: print the first part of the error text
        print("Response text (first 500 chars):", response.text[:500])
        raise RuntimeError(f"Error fetching file (status={response.status_code}).")

    text_buffer = io.StringIO(response.text)
    # Read the CSV contents
    df = pd.read_csv(text_buffer)

    return df


def chicago_dataframe(year, output_filename_ch, full_fetch=False):
    """
    Filters the PUMAS to only the Chicago city
    """
    if full_fetch:
        df = build_census_csv(year, output_filename_ch)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(output_filename_ch)
        # Filter the DataFrame for rows where PUMA is between 3151 and 3168
    else:
        # dict of paths
        if year == 2023:
            path = "https://drive.usercontent.google.com/download?id=1KqviAJthq8RzZa9nVoBS5dp553ix55I7&export=download&authuser=0&confirm=t&uuid=abf16c04-2bbc-48ee-8a9b-9a501f2b315a&at=AEz70l6_lxclQ30xwZyTTaVqhBtR:1740868465146"
        elif year == 2013:
            path = "https://drive.usercontent.google.com/download?id=1h8D9WeDCCBe0F75ZNbKqyQ7078ca9HHO&export=download&authuser=0&confirm=t&uuid=580455ba-d495-4801-939f-313992f725dd&at=AEz70l7IHPdNQzGZwfDYNnRNRFEZ:1741292537535"
        elif year == 2018:
            path = "https://drive.usercontent.google.com/download?id=1zcP7YJyW5NemZ_FAF2r3Ub-dcAsjYVc7&export=download&authuser=0&confirm=t&uuid=7940c379-4f49-46fa-924a-6055f0c631c5&at=AEz70l5Qlq8c0GftWr8-e9X4u-GA:1741481012388"

        df = get_google_drive_files(path)
    # print(len(df))
    # print(df.head())
    if year == 2023:
        chicago_df = df[
            (df["PUMA"].astype(int) >= 3151) & (df["PUMA"].astype(int) <= 3168)
        ]
    else:
        df = df[df["ST"] != ""]
        chicago_df = df[
            (df["ST"].astype(int) == 17)
            & (
                ((df["PUMA"].astype(int) >= 3501) & (df["PUMA"].astype(int) <= 3504))
                | ((df["PUMA"].astype(int) >= 3520) & (df["PUMA"].astype(int) <= 3532))
            )
        ]

    if full_fetch:
        chicago_df.to_csv(output_filename_ch, index=False)

    return chicago_df


if __name__ == "__main__":
    for yr in YEAR:
        output_filename = Path(f"census_{yr}.csv")
        output_filename_ch = Path(f"census_{yr}_ch.csv")
        chicago_dataframe(yr, output_filename_ch, full_fetch=False)
        time.sleep(10)
