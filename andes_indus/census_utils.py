import pandas as pd
import numpy as np
import httpx
from api_get import build_census_csv
import io
import re


def chicago_dataframe(full_fetch=False):
    """
    Filters the PUMAS to only the Chicago city
    """
    if full_fetch:
        df = build_census_csv()
        # Read the CSV file into a DataFrame
        # df = pd.read_csv(csv_file)
        # Filter the DataFrame for rows where PUMA is between 3151 and 3168
    else:
        # Original Google Drive share link (VIEW link)

        path = "https://drive.usercontent.google.com/download?id=1KqviAJthq8RzZa9nVoBS5dp553ix55I7&export=download&authuser=0&confirm=t&uuid=abf16c04-2bbc-48ee-8a9b-9a501f2b315a&at=AEz70l6_lxclQ30xwZyTTaVqhBtR:1740868465146"

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
    chicago_df = df[(df["PUMA"].astype(int) >= 3151) & (df["PUMA"].astype(int) <= 3168)]
    
    return chicago_df


def cleaning_data(full_fetch=False):
    """
    load a cvs file and clean:
    - transform variables from string to numeric
    - drop observations with no income information
    """
    df = chicago_dataframe(full_fetch=False)
    # convert to numeric
    cols = ["SCHL", "SCHG", "AGEP", "PUMA", "PWGTP", "HINCP", "SEX", "RACBLK"]
    df[cols] = df[cols].apply(pd.to_numeric)
    # we are assuming missing values are at random and droping them
    df.loc[(df["HINCP"] == -60000), "HINCP"] = None
    
    # race 

    # dummy
    df["men"]       = np.where((df["SEX"] == 1), 1, 0)
    df["woman"]     = np.where((df["SEX"] == 2), 1, 0)
    df["black"]     = np.where((df["RACBLK"] == 1), 1, 0)
    df["non_black"] = np.where((df["RACBLK"] == 0), 1, 0)

    df_clean = df.dropna(subset=["HINCP"])
    return df_clean


def education_vars(full_fetch=False):
    """creates the education variables to be used
    in the analysis
    """
    df = cleaning_data(full_fetch=False)
    # total population

    # years of education
    df.loc[df["SCHL"] <= 3, "years_education"] = 0
    df.loc[df["SCHL"] == 4, "years_education"] = 1
    df.loc[df["SCHL"] == 5, "years_education"] = 2
    df.loc[df["SCHL"] == 6, "years_education"] = 3
    df.loc[df["SCHL"] == 7, "years_education"] = 4
    df.loc[df["SCHL"] == 8, "years_education"] = 5
    df.loc[df["SCHL"] == 9, "years_education"] = 6
    df.loc[df["SCHL"] == 10, "years_education"] = 7
    df.loc[df["SCHL"] == 11, "years_education"] = 8
    df.loc[df["SCHL"] == 12, "years_education"] = 9
    df.loc[df["SCHL"] == 13, "years_education"] = 10
    df.loc[df["SCHL"] == 14, "years_education"] = 11
    df.loc[df["SCHL"] == 15, "years_education"] = 12
    df.loc[df["SCHL"] >= 16, "years_education"] = 13

    # School age population
    df["school_age"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 18)).astype(int)
    # School levels theoretical age
    df["elementary"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10)).astype(int)
    df["middle"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13)).astype(int)
    df["high_school"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18)).astype(int)

    # School age population by sex and race
    df["school_age_men"]   = ((df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["SEX"] == 1)).astype(int)
    df["school_age_women"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["SEX"] == 2)).astype(int)

    df["school_age_black"]     = ((df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["RACBLK"] == 1)).astype(int)
    df["school_age_non_black"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["RACBLK"] == 0)).astype(int)

    # School levels theoretical age
    df["elementary"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10) ).astype(int)
    df["middle"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13)).astype(int)
    df["high_school"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18)).astype(int)

    # School levels theoretical age
    df["elementary_men"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["SEX"] == 1)).astype(int)
    df["middle_men"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["SEX"] == 1)).astype(int)
    df["high_school_men"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["SEX"] == 1)).astype(int)

# School levels theoretical age
    df["elementary_women"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["SEX"] == 2)).astype(int)
    df["middle_women"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["SEX"] == 2)).astype(int)
    df["high_school_women"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["SEX"] == 2)).astype(int)

# School levels theoretical age
    df["elementary_black"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["RACBLK"] == 1)).astype(int)
    df["middle_black"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["RACBLK"] == 1)).astype(int)
    df["high_school_black"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["RACBLK"] == 1)).astype(int)

# School levels theoretical age
    df["elementary_non_black"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["RACBLK"] == 0)).astype(int)
    df["middle_non_black"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["RACBLK"] == 0)).astype(int)
    df["high_school_non_black"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["RACBLK"] == 0)).astype(int)



    # School attendance SCH
    #  "0": "N/A (less than 3 years old)",
    #  "3": "Yes, private school or college or home school",
    #  "1": "No, has not attended in the last 3 months",
    #  "2": "Yes, public school or public college"

    # Compute binary school attendance
    df["school_attendance"] = ((df["SCH"] != "1") & (df["school_age"] == 1)).astype(int)

    # Create a mask for school-age observations
    mask = df["school_age"] == 1

    # Compute school attendance by education level
    df["atten_elementary"] = np.where(
        mask & (df["years_education"] <= 4) & (df["elementary"] == 1), 1, 0
    )
    df["atten_middle"] = np.where(
        mask & df["years_education"].between(5, 7) & (df["middle"] == 1), 1, 0
    )
    df["atten_high_school"] = np.where(
        mask & df["years_education"].between(8, 11) & (df["high_school"] == 1), 1, 0
    )

    # school attendance by sex, level and race 
    # elementary

    df["atten_elementary_women"] = np.where(
        mask & (df["years_education"] <= 4) & (df["elementary"] == 1) & (df["SEX"] == 2), 1, 0
    )
    df["atten_elementary_men"] = np.where(
        mask & (df["years_education"] <= 4) & (df["elementary"] == 1) & (df["SEX"] == 1), 1, 0
    )
    df["atten_elementary_black"] = np.where(
        mask & (df["years_education"] <= 4) & (df["elementary"] == 1) & (df["RACBLK"] == 1), 1, 0
    )
    df["atten_elementary_non_black"] = np.where(
        mask & (df["years_education"] <= 4) & (df["elementary"] == 1) & (df["RACBLK"] == 0), 1, 0
    )

    # middleschool

    df["atten_middle_women"] = np.where(
        mask & df["years_education"].between(5, 7) & (df["middle"] == 1) & (df["SEX"] == 2), 1, 0
    )

    df["atten_middle_men"] = np.where(
        mask & df["years_education"].between(5, 7) & (df["middle"] == 1) & (df["SEX"] == 1), 1, 0
    )

    df["atten_middle_black"] = np.where(
        mask & df["years_education"].between(5, 7) & (df["middle"] == 1) & (df["RACBLK"] == 1), 1, 0
    )

    df["atten_middle_non_black"] = np.where(
        mask & df["years_education"].between(5, 7) & (df["middle"] == 1) & (df["RACBLK"] == 0), 1, 0
    )

    # Highschool

    df["atten_high_school_women"] = np.where(
        mask & df["years_education"].between(8, 11) & (df["high_school"] == 1) & (df["SEX"] == 2), 1, 0
    )

    df["atten_high_school_men"] = np.where(
        mask & df["years_education"].between(8, 11) & (df["high_school"] == 1) & (df["SEX"] == 1), 1, 0
    )

    df["atten_high_school_black"] = np.where(
        mask & df["years_education"].between(8, 11) & (df["high_school"] == 1) & (df["RACBLK"] == 1), 1, 0
    )

    df["atten_high_school_non_black"] = np.where(
        mask & df["years_education"].between(8, 11) & (df["high_school"] == 1) & (df["RACBLK"] == 0), 1, 0
    )
    # List of columns that need to be weighted by PWGTP
    cols_to_weight = [
        "school_attendance",
        "school_age",
        "atten_elementary",
        "atten_elementary_women",
        "atten_elementary_men",
        "atten_elementary_black",
        "atten_elementary_non_black",
        "atten_middle",
        "atten_middle_women",
        "atten_middle_men",
        "atten_middle_black",
        "atten_middle_non_black",
        "atten_high_school",
        "atten_high_school_non_black",
        "atten_high_school_black",
        "atten_high_school_men",
        "atten_high_school_women",
        "elementary",
        "elementary_men",
        "elementary_women",
        "elementary_black",
        "elementary_non_black",
        "middle",
        "middle_men",
        "middle_women",
        "middle_black",
        "middle_non_black",
        "high_school",
        "high_school_men",
        "high_school_women",
        "high_school_black",
        "high_school_non_black",
        "HINCP",
        "men",
        "woman",
        "black",
        "non_black",
    ]

    # Multiply each column by PWGTP and save as a new column with _w appended
    df[[f"{col}_w" for col in cols_to_weight]] = df[cols_to_weight].multiply(
        df["PWGTP"], axis=0
    )

    selected_columns_df = (
        df[
            [
                "PUMA",
                "atten_elementary_w",
                "atten_elementary_women_w",
                "atten_elementary_men_w",
                "atten_elementary_black_w",
                "atten_elementary_non_black_w",
                "elementary_w",
                "elementary_men_w",
                "elementary_women_w",
                "elementary_black_w",
                "elementary_non_black_w",
                "atten_middle_w",
                "atten_middle_women_w",
                "atten_middle_men_w",
                "atten_middle_black_w",
                "atten_middle_non_black_w",
                "middle_men_w",
                "middle_women_w",
                "middle_black_w",
                "middle_non_black_w",
                "middle_w",
                "atten_high_school_w",
                "atten_high_school_non_black_w",
                "atten_high_school_black_w",
                "atten_high_school_men_w",
                "atten_high_school_women_w",
                "high_school_w",
                "high_school_men_w",
                "high_school_women_w",
                "high_school_black_w",
                "high_school_non_black_w",
                "PWGTP",
                "HINCP_w",
                "men_w",
                "woman_w",
                "black_w",
                "non_black_w",
            ]
        ]
        .groupby("PUMA")
        .sum()
        .reset_index()
    )
    return selected_columns_df



def aggregate_puma_data(full_fetch=False):
    """
    Aggregates all PUMA information into a single row while keeping the original data.   
    Returns:
    pd.DataFrame: The dataset with an additional aggregated PUMA row.
    """
    df = education_vars(full_fetch=False)
    # Drop non-numeric columns before summing
    aggregated_puma = df.drop(columns=["PUMA"]).sum()
    
    # Assign a new identifier for the aggregated PUMA
    aggregated_puma["PUMA"] = 9999

    # Convert to DataFrame
    aggregated_puma_df = pd.DataFrame([aggregated_puma])

    # Append the aggregated PUMA row to the original dataset
    df_with_aggregated = pd.concat([df, aggregated_puma_df], ignore_index=True)

    return df_with_aggregated


def reshape_long_format(df, id_vars=["PUMA", "PWGTP", "year"]):
    """
    Reshapes a wide-format dataframe into long format.

    Parameters:
        df (pd.DataFrame): The wide-format dataframe.
        id_vars (list): List of columns to retain as identifier variables.

    Returns:
        pd.DataFrame: A long-format dataframe with columns:
            - 'indicator': The base indicator name with subgroup suffix removed.
            - 'value': The value of the indicator.
            - 'cut_name': Subgroup identifier derived from the original indicator name.
    
    The function assigns:
      - 'women' if the indicator ends with _women or _women_w,
      - 'men' if it ends with _men or _men_w,
      - 'afroamerican' if it ends with _black or black_w,
      - 'non_africanamerican' if it ends with _non_black or non_black_w.
    """
    # Identify columns to be melted (all columns not in id_vars)
    
    df_long = df.melt(id_vars=id_vars, var_name="indicator", value_name="value")
    
    # Create the 'cut_name' column using vectorized string matching
    conditions = [
        df_long["indicator"].str.endswith("_women") | df_long["indicator"].str.endswith("_women_w"),
        df_long["indicator"].str.endswith("_men") | df_long["indicator"].str.endswith("_men_w"),
        df_long["indicator"].str.endswith("_black") | df_long["indicator"].str.endswith("black_w"),
        df_long["indicator"].str.endswith("_non_black") | df_long["indicator"].str.endswith("non_black_w")
    ]
    choices = ["women", "men", "afroamerican", "non_africanamerican"]
    df_long["cut_name"] = np.select(conditions, choices, default="")
    
    # Remove subgroup suffix from the indicator name using the standalone remove_suffix function
    df_long["indicator"] = df_long["indicator"]
    
    return df_long

def rename_functions(year,output_file="data/census_df_long.csv", full_fetch=False):
    df = variable_labels(year, full_fetch=False)
    df_long = reshape_long_format(df, id_vars=["PUMA", "PWGTP", "year"])
    # Create cut_name column based on indicator suffixes
    conditions = [
        df_long["indicator"].str.endswith("_women") | df_long["indicator"].str.endswith("_women_w"),
        df_long["indicator"].str.endswith("_men") | df_long["indicator"].str.endswith("_men_w"),
        df_long["indicator"].str.endswith("_black") | df_long["indicator"].str.endswith("black_w"),
        df_long["indicator"].str.endswith("_non_black") | df_long["indicator"].str.endswith("non_black_w")
    ]
    choices = ["women", "men", "afroamerican", "non_africanamerican"]
    df_long["cut_name"] = np.select(conditions, choices, default="Total")

    df_long["indicator"] = df_long["indicator"]

   
    pattern = re.compile(r'(\_men|\_women|\_black|\_non\_black)')
    df_long['indicator'] = df_long['indicator'].str.replace(pattern, '', regex=True)

    df_long.to_csv(output_file, index=False)

def education_indicators(year: int, full_fetch=False):
    """
    Creates education indicators, adds a 'year' column, and returns the aggregated DataFrame.
    """
    df = aggregate_puma_data(full_fetch=False)

    # Calculate attendance rates (as percentages)
    df["attendance_rate_elementary"] = (
        df["atten_elementary_w"] / df["elementary_w"]
    ) * 100
    df["attendance_rate_middle"] = (df["atten_middle_w"] / df["middle_w"]) * 100
    df["attendance_rate_high"] = (df["atten_high_school_w"] / df["high_school_w"]) * 100

        # Calculate attendance rates (men)
    df["attendance_rate_elementary_men"] = (
        df["atten_elementary_men_w"] / df["elementary_men_w"]
    ) * 100
    df["attendance_rate_middle_men"] = (df["atten_middle_men_w"] / df["middle_men_w"]) * 100
    df["attendance_rate_high_men"] = (df["atten_high_school_men_w"] / df["high_school_men_w"]) * 100

        # Calculate attendance rates (women)
    df["attendance_rate_elementary_women"] = (
        df["atten_elementary_women_w"] / df["elementary_women_w"]
    ) * 100
    df["attendance_rate_middle_women"] = (df["atten_middle_women_w"] / df["middle_women_w"]) * 100
    df["attendance_rate_high_women"] = (df["atten_high_school_women_w"] / df["high_school_women_w"]) * 100

        # Calculate attendance rates (black)
    df["attendance_rate_elementary_black"] = (
        df["atten_elementary_black_w"] / df["elementary_black_w"]
    ) * 100
    df["attendance_rate_middle_black"] = (df["atten_middle_black_w"] / df["middle_black_w"]) * 100
    df["attendance_rate_high_black"] = (df["atten_high_school_black_w"] / df["high_school_black_w"]) * 100

        # Calculate attendance rates (none black)
    df["attendance_rate_elementary_non_black"] = (
        df["atten_elementary_non_black_w"] / df["elementary_non_black_w"]
    ) * 100
    df["attendance_rate_middle_non_black"] = (df["atten_middle_non_black_w"] / df["middle_non_black_w"]) * 100
    df["attendance_rate_high_non_black"] = (df["atten_high_school_non_black_w"] / df["high_school_non_black_w"]) * 100

    # calculate school age population rates (as percentages)
    df["elementary_percentage"] = (df["elementary_w"] / df["PWGTP"]) * 100
    df["middle_percentage"] = (df["middle_w"] / df["PWGTP"]) * 100
    df["high_percentage"] = (df["high_school_w"] / df["PWGTP"]) * 100

    # Add a new column for the year
    df["year"] = year
     
    return df

def variable_labels(year, full_fetch=False):
    df = education_indicators(year, full_fetch=full_fetch)
    label_map = {
    3151: "(Northwest) - Albany Park, Norwood Park, Forest Glen, North Park & O'Hare",
    3152: "(North) - West Ridge, Lincoln Square & North Center",
    3153: "(North) - Uptown, Edgewater & Rogers Park",
    3154: "(North) - Lake View & Lincoln Park",
    3155: "(Northwest) - Logan Square, Irving Park & Avondale",
    3156: "(Northwest) - Portage Park, Dunning & Jefferson Park",
    3157: "(West) - Belmont Cragin, Humboldt Park, Hermosa & Montclare",
    3158: "(West) - Austin, North Lawndale & East/West Garfield Park",
    3159: "(West) - West Town & Near West Side",
    3160: "(Central) - Near North Side, Loop & Near South Side",
    3161: "(South) - Hyde Park, Grand Boulevard, Woodlawn, Douglas & Kenwood",
    3162: "(Southwest) - New City, Lower West Side, Bridgeport & McKinley Park",
    3163: "(Southwest) - South Lawndale, Brighton Park & Gage Park",
    3164: "(Southwest) - Ashburn, Garfield Ridge, West Lawn, Clearing & West Elsdon",
    3165: "(South) - Chicago Lawn, Greater Grand Crossing & West Englewood/Englewood",
    3166: "(Southwest) - Auburn Gresham, Washington Heights, Morgan Park & Beverly",
    3167: "(South) - Roseland, Chatham, West Pullman, Calumet Heights & Avalon Park",
    3168: "(South) - South Shore, South Chicago, East Side & South Deering",
    9999: "Chicago Area"
    }
    df["puma_label"] = df["PUMA"].map(label_map)
    return df

def process_multiple_years(output_file="data/census_df.csv", full_fetch=False):
    """
    Processes multiple CSV files (one per year), appends the results with a 'year' column,
    and saves the final DataFrame to CSV.

    Parameters:
        file_year_pairs: list of tuples (csv_file, year)
        output_file: path for the output CSV file
    """
    dfs = []
    for year in [2023]:
        # for year in range(2021,2024):
        dfs.append(variable_labels(year, full_fetch=False))

    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv(output_file, index=False)



if __name__ == "__main__":
    process_multiple_years("data/census_df.csv", full_fetch=False)
    rename_functions(2023,"data/census_df_long.csv", full_fetch=False)
