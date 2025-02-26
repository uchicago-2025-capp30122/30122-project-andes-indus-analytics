import csv
from pathlib import Path
import pandas as pd
import numpy as np
from .api_get import build_census_csv


def chicago_dataframe():
    """
    Filters the PUMAS to only the Chicago city
    """
    
    df = build_census_csv()
    # Read the CSV file into a DataFrame
    #df = pd.read_csv(csv_file)   
    # Filter the DataFrame for rows where PUMA is between 3151 and 3168
    chicago_df = df[(df["PUMA"].astype(int) >= 3151) & (df["PUMA"].astype(int) <= 3168)]
    return chicago_df

def cleaning_data():
    """
    load a cvs file and clean:
    - transform variables from string to numeric 
    - drop observations with no income information
    """
    df = chicago_dataframe()
    # convert to numeric
    cols = ["SCHL", "SCHG", "AGEP", "PUMA", "PWGTP", "HINCP"]
    df[cols] = df[cols].apply(pd.to_numeric)
    # we are assuming missing values are at random and droping them 
    df.loc[(df["HINCP"] == -60000), "HINCP"] = None
    df_clean = df.dropna(subset=['HINCP']) 

    return df_clean

def education_vars():
    """ creates the education variables to be used
    in the analysis  
    """
    df = cleaning_data()
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
    df["school_age"]   = ((df["AGEP"] >= 5) & (df["AGEP"] <=18)).astype(int)
 # School levels theoretical age 
    df["elementary"]    = ((df["AGEP"] >= 5)  & (df["AGEP"] <=10)).astype(int)
    df["middle"]        = ((df["AGEP"] >= 11) & (df["AGEP"] <=13)).astype(int)
    df["high_school"]   = ((df["AGEP"] >= 14) & (df["AGEP"] <=18)).astype(int)

    # School attendance SCH
    #  "0": "N/A (less than 3 years old)",
    #  "3": "Yes, private school or college or home school",
    #  "1": "No, has not attended in the last 3 months",
    #  "2": "Yes, public school or public college"

    # Compute binary school attendance
    df["school_attendance"] = (((df["SCH"] != "1") & (df["school_age"] == 1)).astype(int))

    # Create a mask for school-age observations
    mask = df["school_age"] == 1

    # Compute school attendance by education level
    df["atten_elementary"] = np.where(mask & (df["years_education"] <= 4) & (df["elementary"] ==1), 1, 0)
    df["atten_middle"]     = np.where(mask & df["years_education"].between(5, 7) & (df["middle"] ==1), 1, 0)
    df["atten_high_school"] = np.where(mask & df["years_education"].between(8, 11) & (df["high_school"] ==1), 1, 0)

    # List of columns that need to be weighted by PWGTP
    cols_to_weight = [
        "school_attendance", "school_age",
        "atten_elementary", "atten_middle", "atten_high_school",
        "elementary", "middle", "high_school"
    ]

    # Multiply each column by PWGTP and save as a new column with _w appended
    df[[f"{col}_w" for col in cols_to_weight]] = df[cols_to_weight].multiply(df["PWGTP"], axis=0)
    
    selected_columns_df = df[['PUMA', "atten_elementary_w", 'elementary_w', 
                          'atten_middle_w', 'middle_w', 
                          'atten_high_school_w', 'high_school_w']].groupby("PUMA").sum().reset_index()
    return selected_columns_df


def education_indicators(year:int):
    """
    Creates education indicators, adds a 'year' column, and returns the aggregated DataFrame.
    """
    df = education_vars()
    
    # Calculate attendance rates (as percentages)
    df["attendance_rate_elementary"] = (df["atten_elementary_w"] / df["elementary_w"]) * 100
    df["attendance_rate_middle"] = (df["atten_middle_w"] / df["middle_w"]) * 100
    df["attendance_rate_high"] = (df["atten_high_school_w"] / df["high_school_w"]) * 100
    
    # Add a new column for the year
    df["year"] = year
    return df

def process_multiple_years(output_file="data/census_df.csv"):
    """
    Processes multiple CSV files (one per year), appends the results with a 'year' column,
    and saves the final DataFrame to CSV.
    
    Parameters:
        file_year_pairs: list of tuples (csv_file, year)
        output_file: path for the output CSV file
    """
    dfs = []
    for year in [2023]:
    #for year in range(2021,2024):
        dfs.append(education_indicators(year))
        
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    process_multiple_years("census_df.csv")