import pandas as pd
import numpy as np
from .api_get import chicago_dataframe
import re


def cleaning_data(df):
    """
    Load a cvs file and clean:
    - transform variables from string to numeric
    - drop observations with no income information
    """
    # convert to numeric
    cols = ["SCHL", "SCHG", "AGEP", "PUMA", "PWGTP", "HINCP", "SEX", "RACBLK"]
    df[cols] = df[cols].apply(pd.to_numeric)
    # we are assuming missing values are at random and droping them
    df.loc[(df["HINCP"] < 0)] = None

    df_clean = df.dropna(subset=["HINCP"])
    return df_clean


def social_variables(df):
    '''
    Creates dummy variables for gender and ethnicity
    '''
    df.loc[:, "men"] = np.where((df["SEX"] == 1), 1, 0)
    df.loc[:, "woman"] = np.where((df["SEX"] == 2), 1, 0)
    df.loc[:, "black"] = np.where((df["RACBLK"] == 1), 1, 0)
    df.loc[:, "hispanic"] = np.where(((df["HISP"] != 1) & (df["RACBLK"] != 1)), 1, 0)
    df.loc[:, "non_black_non_hispanic"] = np.where(
        ((df["black"] == 0) & (df["hispanic"]) == 0)
        | ((df["black"] == 1) & (df["hispanic"]) == 1),
        1,
        0,
    )

    return df


def education_vars(df):
    """creates the education variables to be used
    in the analysis
    """
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
    df.loc[:, "school_age"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 18)).astype(int)
    # School levels theoretical age
    df.loc[:, "elementary"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10)).astype(int)
    df.loc[:, "middle"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13)).astype(int)
    df.loc[:, "high_school"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18)).astype(int)

    # School age population by sex and race
    df.loc[:, "school_age_men"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["SEX"] == 1)
    ).astype(int)
    df.loc[:, "school_age_women"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["SEX"] == 2)
    ).astype(int)

    df.loc[:, "school_age_black"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["RACBLK"] == 1)
    ).astype(int)
    df.loc[:, "school_age_non_black"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 18) & (df["RACBLK"] == 0)
    ).astype(int)

    # School levels theoretical age
    df.loc[:, "elementary"] = ((df["AGEP"] >= 5) & (df["AGEP"] <= 10)).astype(int)
    df.loc[:, "middle"] = ((df["AGEP"] >= 11) & (df["AGEP"] <= 13)).astype(int)
    df.loc[:, "high_school"] = ((df["AGEP"] >= 14) & (df["AGEP"] <= 18)).astype(int)

    # School levels theoretical age
    df.loc[:, "elementary_men"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["SEX"] == 1)
    ).astype(int)
    df.loc[:, "middle_men"] = (
        (df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["SEX"] == 1)
    ).astype(int)
    df.loc[:, "high_school_men"] = (
        (df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["SEX"] == 1)
    ).astype(int)

    # School levels theoretical age
    df.loc[:, "elementary_women"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["SEX"] == 2)
    ).astype(int)
    df.loc[:, "middle_women"] = (
        (df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["SEX"] == 2)
    ).astype(int)
    df.loc[:, "high_school_women"] = (
        (df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["SEX"] == 2)
    ).astype(int)

    # School levels theoretical age
    df.loc[:, "elementary_black"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["RACBLK"] == 1)
    ).astype(int)
    df.loc[:, "middle_black"] = (
        (df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["RACBLK"] == 1)
    ).astype(int)
    df.loc[:, "high_school_black"] = (
        (df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["RACBLK"] == 1)
    ).astype(int)

    # School levels theoretical age
    df.loc[:, "elementary_hispanic"] = (
        (df["AGEP"] >= 5) & (df["AGEP"] <= 10) & (df["hispanic"] == 1)
    ).astype(int)
    df.loc[:, "middle_hispanic"] = (
        (df["AGEP"] >= 11) & (df["AGEP"] <= 13) & (df["hispanic"] == 1)
    ).astype(int)
    df.loc[:, "high_school_hispanic"] = (
        (df["AGEP"] >= 14) & (df["AGEP"] <= 18) & (df["hispanic"] == 1)
    ).astype(int)

    # School levels theoretical age
    df.loc[:, "elementary_non_black_non_hispanic"] = (
        (df["AGEP"] >= 5)
        & (df["AGEP"] <= 10)
        & (df["RACBLK"] == 0)
        & (df["hispanic"] == 0)
    ).astype(int)
    df.loc[:, "middle_non_black_non_hispanic"] = (
        (df["AGEP"] >= 11)
        & (df["AGEP"] <= 13)
        & (df["RACBLK"] == 0)
        & (df["hispanic"] == 0)
    ).astype(int)
    df.loc[:, "high_school_non_black_non_hispanic"] = (
        (df["AGEP"] >= 14)
        & (df["AGEP"] <= 18)
        & (df["RACBLK"] == 0)
        & (df["hispanic"] == 0)
    ).astype(int)

    # School attendance SCH
    #  "0": "N/A (less than 3 years old)",
    #  "3": "Yes, private school or college or home school",
    #  "1": "No, has not attended in the last 3 months",
    #  "2": "Yes, public school or public college"

    # Compute binary school attendance
    df.loc[:, "school_attendance"] = (
        (df["SCH"] != "1") & (df["school_age"] == 1)
    ).astype(int)

    # Create a mask for school-age observations
    mask = df["school_age"] == 1

    # Compute school attendance by education level
    df.loc[:, "atten_elementary"] = np.where(
        mask & (df["years_education"] <= 4) & (df["elementary"] == 1), 1, 0
    )
    df.loc[:, "atten_middle"] = np.where(
        mask & df["years_education"].between(5, 7) & (df["middle"] == 1), 1, 0
    )
    df.loc[:, "atten_high_school"] = np.where(
        mask & df["years_education"].between(8, 11) & (df["high_school"] == 1), 1, 0
    )

    # school attendance by sex, level and race
    # elementary

    df.loc[:, "atten_elementary_women"] = np.where(
        mask
        & (df["years_education"] <= 4)
        & (df["elementary"] == 1)
        & (df["SEX"] == 2),
        1,
        0,
    )
    df.loc[:, "atten_elementary_men"] = np.where(
        mask
        & (df["years_education"] <= 4)
        & (df["elementary"] == 1)
        & (df["SEX"] == 1),
        1,
        0,
    )
    df.loc[:, "atten_elementary_black"] = np.where(
        mask
        & (df["years_education"] <= 4)
        & (df["elementary"] == 1)
        & (df["RACBLK"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_elementary_hispanic"] = np.where(
        mask
        & (df["years_education"] <= 4)
        & (df["elementary"] == 1)
        & (df["hispanic"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_elementary_non_black_non_hispanic"] = np.where(
        mask
        & (df["years_education"] <= 4)
        & (df["elementary"] == 1)
        & ((df["RACBLK"] == 0) & (df["hispanic"] == 0)),
        1,
        0,
    )

    # middleschool

    df.loc[:, "atten_middle_women"] = np.where(
        mask
        & df["years_education"].between(5, 7)
        & (df["middle"] == 1)
        & (df["SEX"] == 2),
        1,
        0,
    )

    df.loc[:, "atten_middle_men"] = np.where(
        mask
        & df["years_education"].between(5, 7)
        & (df["middle"] == 1)
        & (df["SEX"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_middle_black"] = np.where(
        mask
        & df["years_education"].between(5, 7)
        & (df["middle"] == 1)
        & (df["RACBLK"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_middle_hispanic"] = np.where(
        mask
        & df["years_education"].between(5, 7)
        & (df["middle"] == 1)
        & (df["hispanic"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_middle_non_black_non_hispanic"] = np.where(
        mask
        & df["years_education"].between(5, 7)
        & (df["middle"] == 1)
        & ((df["RACBLK"] == 0) & (df["hispanic"] == 0)),
        1,
        0,
    )

    # Highschool

    df.loc[:, "atten_high_school_women"] = np.where(
        mask
        & df["years_education"].between(8, 11)
        & (df["high_school"] == 1)
        & (df["SEX"] == 2),
        1,
        0,
    )

    df.loc[:, "atten_high_school_men"] = np.where(
        mask
        & df["years_education"].between(8, 11)
        & (df["high_school"] == 1)
        & (df["SEX"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_high_school_black"] = np.where(
        mask
        & df["years_education"].between(8, 11)
        & (df["high_school"] == 1)
        & (df["RACBLK"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_high_school_hispanic"] = np.where(
        mask
        & df["years_education"].between(8, 11)
        & (df["high_school"] == 1)
        & (df["hispanic"] == 1),
        1,
        0,
    )

    df.loc[:, "atten_high_school_non_black_non_hispanic"] = np.where(
        mask
        & df["years_education"].between(8, 11)
        & (df["high_school"] == 1)
        & ((df["RACBLK"] == 0) & (df["hispanic"] == 0)),
        1,
        0,
    )
    # List of columns that need to be weighted by PWGTP
    cols_to_weight = [
        "school_attendance",
        "school_age",
        "atten_elementary",
        "atten_elementary_women",
        "atten_elementary_men",
        "atten_elementary_black",
        "atten_elementary_hispanic",
        "atten_elementary_non_black_non_hispanic",
        "atten_middle",
        "atten_middle_women",
        "atten_middle_men",
        "atten_middle_black",
        "atten_middle_hispanic",
        "atten_middle_non_black_non_hispanic",
        "atten_high_school",
        "atten_high_school_non_black_non_hispanic",
        "atten_high_school_hispanic",
        "atten_high_school_black",
        "atten_high_school_men",
        "atten_high_school_women",
        "elementary",
        "elementary_men",
        "elementary_women",
        "elementary_black",
        "elementary_hispanic",
        "elementary_non_black_non_hispanic",
        "middle",
        "middle_men",
        "middle_women",
        "middle_black",
        "middle_hispanic",
        "middle_non_black_non_hispanic",
        "high_school",
        "high_school_men",
        "high_school_women",
        "high_school_black",
        "high_school_hispanic",
        "high_school_non_black_non_hispanic",
        "HINCP",
        "men",
        "woman",
        "black",
        "hispanic",
        "non_black_non_hispanic",
    ]

    # Multiply each column by PWGTP and save as a new column with _w appended
    df[[f"{col}_w" for col in cols_to_weight]] = df.loc[:, cols_to_weight].multiply(df["PWGTP"], axis=0)

    selected_columns_df = (
        df[
            [
                "PUMA",
                "atten_elementary_w",
                "atten_elementary_women_w",
                "atten_elementary_men_w",
                "atten_elementary_black_w",
                "atten_elementary_hispanic_w",
                "atten_elementary_non_black_non_hispanic_w",
                "elementary_w",
                "elementary_men_w",
                "elementary_women_w",
                "elementary_black_w",
                "elementary_hispanic_w",
                "elementary_non_black_non_hispanic_w",
                "atten_middle_w",
                "atten_middle_women_w",
                "atten_middle_men_w",
                "atten_middle_black_w",
                "atten_middle_hispanic_w",
                "atten_middle_non_black_non_hispanic_w",
                "middle_men_w",
                "middle_women_w",
                "middle_black_w",
                "middle_hispanic_w",
                "middle_non_black_non_hispanic_w",
                "middle_w",
                "atten_high_school_w",
                "atten_high_school_non_black_non_hispanic_w",
                "atten_high_school_black_w",
                "atten_high_school_hispanic_w",
                "atten_high_school_men_w",
                "atten_high_school_women_w",
                "high_school_w",
                "high_school_men_w",
                "high_school_women_w",
                "high_school_black_w",
                "high_school_hispanic_w",
                "high_school_non_black_non_hispanic_w",
                "PWGTP",
                "HINCP_w",
                "men_w",
                "woman_w",
                "black_w",
                "hispanic_w",
                "non_black_non_hispanic_w",
            ]
        ]
        .groupby("PUMA")
        .sum()
        .reset_index()
    )
    return selected_columns_df


def aggregate_puma_data(df):
    """
    Aggregates all PUMA information into a single row while keeping the original data.
    Returns:
    pd.DataFrame: The dataset with an additional aggregated PUMA row.
    """

    # Drop non-numeric columns before summing
    aggregated_puma = df.drop(columns=["PUMA"]).sum()

    # Assign a new identifier for the aggregated PUMA
    aggregated_puma["PUMA"] = 9999

    # Convert to DataFrame
    aggregated_puma_df = pd.DataFrame([aggregated_puma])

    # Append the aggregated PUMA row to the original dataset
    df_with_aggregated = pd.concat([df, aggregated_puma_df], ignore_index=True)

    return df_with_aggregated


def reshape_long_format(df, id_vars=["PUMA", "puma_label", "year"]):
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

    """
    # Identify columns to be melted (all columns not in id_vars)

    df_long = df.melt(id_vars=id_vars, var_name="indicator", value_name="value")

    return df_long


def education_indicators(df):
    """
    Creates education indicators, adds a 'year' column, and returns the aggregated DataFrame.
    """

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
    df["attendance_rate_middle_men"] = (
        df["atten_middle_men_w"] / df["middle_men_w"]
    ) * 100
    df["attendance_rate_high_men"] = (
        df["atten_high_school_men_w"] / df["high_school_men_w"]
    ) * 100

    # Calculate attendance rates (women)
    df["attendance_rate_elementary_women"] = (
        df["atten_elementary_women_w"] / df["elementary_women_w"]
    ) * 100
    df["attendance_rate_middle_women"] = (
        df["atten_middle_women_w"] / df["middle_women_w"]
    ) * 100
    df["attendance_rate_high_women"] = (
        df["atten_high_school_women_w"] / df["high_school_women_w"]
    ) * 100

    # Calculate attendance rates (black)
    df["attendance_rate_elementary_black"] = (
        df["atten_elementary_black_w"] / df["elementary_black_w"]
    ) * 100
    df["attendance_rate_middle_black"] = (
        df["atten_middle_black_w"] / df["middle_black_w"]
    ) * 100
    df["attendance_rate_high_black"] = (
        df["atten_high_school_black_w"] / df["high_school_black_w"]
    ) * 100

    # Calculate attendance rates (hispanic)
    df["attendance_rate_elementary_hispanic"] = (
        df["atten_elementary_hispanic_w"] / df["elementary_hispanic_w"]
    ) * 100
    df["attendance_rate_middle_hispanic"] = (
        df["atten_middle_hispanic_w"] / df["middle_hispanic_w"]
    ) * 100
    df["attendance_rate_high_hispanic"] = (
        df["atten_high_school_hispanic_w"] / df["high_school_hispanic_w"]
    ) * 100

    # Calculate attendance rates (none black)
    df["attendance_rate_elementary_non_black_non_hispanic"] = (
        df["atten_elementary_non_black_non_hispanic_w"]
        / df["elementary_non_black_non_hispanic_w"]
    ) * 100
    df["attendance_rate_middle_non_black_non_hispanic"] = (
        df["atten_middle_non_black_non_hispanic_w"]
        / df["middle_non_black_non_hispanic_w"]
    ) * 100
    df["attendance_rate_high_non_black_non_hispanic"] = (
        df["atten_high_school_non_black_non_hispanic_w"]
        / df["high_school_non_black_non_hispanic_w"]
    ) * 100

    # calculate school age population rates (as percentages)
    df["elementary_percentage"] = (df["elementary_w"] / df["PWGTP"]) * 100
    df["middle_percentage"] = (df["middle_w"] / df["PWGTP"]) * 100
    df["high_percentage"] = (df["high_school_w"] / df["PWGTP"]) * 100

    return df


def variable_labels(df, year):
    '''
    Helper function to create labels for each PUMA.
    '''
    if year == 2023:
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
            9999: "Chicago Area",
        }
    else:
        label_map = {
            3504: "(Northwest) - Irving Park, Albany Park, Forest Glen & North Park",
            3503: "(North) - West Ridge, Lincoln Square & North Center",
            3501: "(North) - Edgewater, Uptown & Rogers Park",
            3502: "(North) - Lake View & Lincoln Park",
            3522: "(Northwest) - Logan Square, Avondale & Hermosa",
            3520: "(Northwest) - Portage Park, Dunning & Jefferson Park",
            3521: "(West) - Austin, Belmont Cragin & Montclare",
            3523: "(West) - North & South Lawndale, Humboldt Park, East & West Garfield Park",
            3524: "(West) - West Town, Near West Side & Lower West Side",
            3525: "(Central) - Near North Side, Loop & Near South Side",
            3529: "(South) - South Shore, Hyde Park, Woodlawn, Grand Boulevard & Douglas",
            3526: "(Southwest) - Brighton Park, New City, Bridgeport & McKinley Park",
            3527: "(Southwest) - Gage Park, Garfield Ridge & West Lawn",
            3528: "(South) - Chicago Lawn, Englewood/West Englewood & Greater Grand Crossing",
            3530: "(South) - Ashburn, Washington Heights, Morgan Park & Beverly",
            3531: "(South) - Auburn Gresham, Roseland, Chatham, Avalon Park & Burnside",
            3532: "(South) - South Chicago, Pullman, West Pullman, East Side & South Deering",
            9999: "Chicago Area",
        }

    df["puma_label"] = df["PUMA"].map(label_map)
    # Add a new column for the year
    df["year"] = year
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
    for year in [2013, 2018, 2023]:
        # for year in range(2021,2024):
        df = chicago_dataframe(year, "", full_fetch=False)
        dfs.append(
            variable_labels(
                education_indicators(
                    aggregate_puma_data(
                        education_vars(social_variables(cleaning_data(df)))
                    )
                ),
                year,
            )
        )

    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv(output_file, index=False)


def rename_functions(output_file="data/census_df_long.csv"):
    df = pd.read_csv("data/census_df.csv")
    df_long = reshape_long_format(df, id_vars=["PUMA", "puma_label", "year"])
    # Create cut_name column based on indicator suffixes
    conditions = [
        df_long["indicator"].str.endswith("_women")
        | df_long["indicator"].str.endswith("_women_w"),
        df_long["indicator"].str.endswith("_men")
        | df_long["indicator"].str.endswith("_men_w"),
        df_long["indicator"].str.endswith("_non_black_non_hispanic")
        | df_long["indicator"].str.endswith("_non_black_non_hispanic_w"),
        df_long["indicator"].str.endswith("_black")
        | df_long["indicator"].str.endswith("_black_w"),
        df_long["indicator"].str.endswith("_hispanic")
        | df_long["indicator"].str.endswith("_hispanic_w"),
    ]
    choices = ["women", "men", "nonafroamerican_hispanic", "afroamerican", "hispanic"]
    df_long["cut_name"] = np.select(conditions, choices, default="Total")

    df_long["indicator"] = df_long["indicator"]

    pattern = re.compile(
        r"(\_men|\_women|\_black||\_hispanic|\_non\_black\_non\_hispanic)"
    )
    df_long["indicator"] = df_long["indicator"].str.replace(pattern, "", regex=True)

    df_long.to_csv(output_file, index=False)


if __name__ == "__main__":
    process_multiple_years("data/census_df.csv", full_fetch=False)
    rename_functions("data/census_df_long.csv")
