import pandas as pd
import numpy as np
import httpx
from api_get import build_census_csv
import io


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
    df["elementary"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10)).astype(int)
    df["middle"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13)).astype(int)
    df["high_school"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18)).astype(int)


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
        "middle",
        "high_school",
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
                "atten_middle_w",
                "atten_middle_women_w",
                "atten_middle_men_w",
                "atten_middle_black_w",
                "atten_middle_non_black_w",
                "middle_w",
                "atten_high_school_w",
                "atten_high_school_non_black_w",
                "atten_high_school_black_w",
                "atten_high_school_men_w",
                "atten_high_school_women_w",
                "high_school_w",
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


def education_indicators(year: int, full_fetch=False):
    """
    Creates education indicators, adds a 'year' column, and returns the aggregated DataFrame.
    """
    df = education_vars(full_fetch=False)

    # Calculate attendance rates (as percentages)
    df["attendance_rate_elementary"] = (
        df["atten_elementary_w"] / df["elementary_w"]
    ) * 100
    df["attendance_rate_middle"] = (df["atten_middle_w"] / df["middle_w"]) * 100
    df["attendance_rate_high"] = (df["atten_high_school_w"] / df["high_school_w"]) * 100

    # calculate school age population rates (as percentages)
    df["elementary_percentage"] = (df["elementary_w"] / df["PWGTP"]) * 100
    df["middle_percentage"] = (df["middle_w"] / df["PWGTP"]) * 100
    df["high_percentage"] = (df["high_school_w"] / df["PWGTP"]) * 100

    # Add a new column for the year
    df["year"] = year
    
   
    return df

"""
def chicago_totals(df):
    var_lst =  [
                "atten_elementary_w",
                "atten_elementary_women_w",
                     "atten_elementary_men_w",
                "atten_elementary_black_w",
                "atten_elementary_non_black_w"
                "elementary_w",
                "atten_middle_w",
                "atten_middle_women_W",
                "atten_middle_men_w",
                "atten_middle_black_w",
                "atten_middle_non_black_w",
                "middle_w",
                "atten_high_school_w",
                "atten_high_school_non_black_w",
                "atten_high_school_black_w",
                "atten_high_school_men_w",
                "atten_high_school_women_w",
                "high_school_w",
                "PWGTP",
                "HINCP_w",
                "men_w",
                "woman_w",
                "black_w",
                "non_black_w",
            ]
    
    for pop in var_lst:
        df.loc[df[pop].sum, "PUMA"] = "CHICAGO"
        df[pop] 
"""
def variable_labels(year, full_fetch=False):
    df = education_indicators(year, full_fetch=False)
     # PUMAS labels
    df.loc[(df["PUMA"] == 3151), "puma_label"] = "(Northwest) - Albany Park, Norwood Park, Forest Glen, North Park & O'Hare"
    df.loc[(df["PUMA"] == 3152), "puma_label"] = "(North) - West Ridge, Lincoln Square & North Center"  
    df.loc[(df["PUMA"] == 3153), "puma_label"] = "(North) - Uptown, Edgewater & Rogers Park"  
    df.loc[(df["PUMA"] == 3154), "puma_label"] = "(North) - Lake View & Lincoln Park" 
    df.loc[(df["PUMA"] == 3155), "puma_label"] = "(Northwest) - Logan Square, Irving Park & Avondale" 
    df.loc[(df["PUMA"] == 3156), "puma_label"] = "(Northwest) - Portage Park, Dunning & Jefferson Park" 
    df.loc[(df["PUMA"] == 3157), "puma_label"] = "(West) - Belmont Cragin, Humboldt Park, Hermosa & Montclare" 
    df.loc[(df["PUMA"] == 3158), "puma_label"] = "(West) - Austin, North Lawndale & East/West Garfield Park" 
    df.loc[(df["PUMA"] == 3159), "puma_label"] = "(West) - West Town & Near West Side" 
    df.loc[(df["PUMA"] == 3160), "puma_label"] = "(Central) - Near North Side, Loop & Near South Side" 
    df.loc[(df["PUMA"] == 3161), "puma_label"] = "(South) - Hyde Park, Grand Boulevard, Woodlawn, Douglas & Kenwood" 
    df.loc[(df["PUMA"] == 3162), "puma_label"] = "(Southwest) - New City, Lower West Side, Bridgeport & McKinley Park" 
    df.loc[(df["PUMA"] == 3163), "puma_label"] = "(Southwest) - South Lawndale, Brighton Park & Gage Park"
    df.loc[(df["PUMA"] == 3164), "puma_label"] = "(Southwest) - Ashburn, Garfield Ridge, West Lawn, Clearing & West Elsdon" 
    df.loc[(df["PUMA"] == 3165), "puma_label"] = "(South) - Chicago Lawn, Greater Grand Crossing & West Englewood/Englewood" 
    df.loc[(df["PUMA"] == 3166), "puma_label"] = "(Southwest) - Auburn Gresham, Washington Heights, Morgan Park & Beverly" 
    df.loc[(df["PUMA"] == 3167), "puma_label"] = "(South) - Roseland, Chatham, West Pullman, Calumet Heights & Avalon Park" 
    df.loc[(df["PUMA"] == 3168), "puma_label"] = "(South) - South Shore, South Chicago, East Side & South Deering" 

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
