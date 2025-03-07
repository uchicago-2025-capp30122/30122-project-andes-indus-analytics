import requests
import pandas as pd
import openpyxl

# Step 1: Get All School IDs


def get_all_school_ids(
    api_url="https://api.cps.edu/schoolprofile/CPS/TypeaheadSchoolSearch",
):
    """
    Fetch all school IDs from the CPS API.

    Returns:
        set: A set of unique School IDs.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        school_ids = {school["SchoolID"] for school in data}
        return school_ids
    else:
        print(f"Error fetching school IDs: {response.status_code}")
        return set()


# Step 2: Fetch Required School Data


def fetch_school_profiles(
    school_ids,
    api_base_url="https://api.cps.edu/schoolprofile/CPS/SingleSchoolProfile?SchoolID={SchoolID}",
):
    """
    Fetch selected school profile data for a list of school IDs from the CPS API.

    Args:
        school_ids (set): A set of school IDs to query.
        api_base_url (str): Base URL of the API endpoint.

    Returns:
        pd.DataFrame: A DataFrame containing selected school profile data.
    """
    school_profiles = []

    for school_id in school_ids:
        url = api_base_url.replace("{SchoolID}", str(school_id))
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data:  # Ensure data is not empty
                school_profiles.append(
                    {
                        "School ID": data.get("SchoolID"),
                        "School Name": data.get("SchoolLongName"),
                        "Latitude": float(data.get("AddressLatitude", 0))
                        if data.get("AddressLatitude")
                        else None,
                        "Longitude": float(data.get("AddressLongitude", 0))
                        if data.get("AddressLongitude")
                        else None,
                        "Student Count": int(data.get("StudentCount", 0)),
                        "Low Income Student Count": int(
                            data.get("StudentCountLowIncome", 0)
                        ),
                        "Graduation Rate": float(data.get("GraduationRate", 0))
                        if data.get("GraduationRate")
                        else None,
                        "Atttendance Rate Current Year": float(
                            data.get("AttendanceRateCurrentYear", 0)
                        )
                        if data.get("AttendanceRateCurrentYear")
                        else None,
                        "Address State": data.get("AddressState", "N/A"),
                        "Address Street": data.get("AddressStreet", "N/A"),
                        "Address Zip Code": data.get("AddressZipCode", "N/A"),
                        "Is High School": bool(data.get("IsHighSchool", False)),
                        "Is Middle School": bool(data.get("IsMiddleSchool", False)),
                        "Is Elementarty School": bool(
                            data.get("IsElementarySchool", False)
                        ),
                        "Is Pre School": bool(data.get("IsPreSchool", False)),
                        "Statistics Summary": data.get("StatisticsSummary", "N/A"),
                        "Demograhics Summary": data.get("DemographicsSummary"),
                    }
                )
        else:
            print(
                f"Error fetching data for School ID {school_id}: {response.status_code}"
            )

    # Convert list of dictionaries to a DataFrame
    return pd.DataFrame(school_profiles)


# Step 3: Save Data to CSV


def save_to_csv(df, filename="data/cps_school_profiles.csv"):
    """
    Save DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame containing school data.
        filename (str): The filename to save.
    """
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def clean_dropout_data(file_path: str) -> pd.DataFrame:
    """
    Reads and cleans dropout data from an Excel file.

    The function reads the "All Students" sheet from the provided Excel file,
    skips the first two rows (so that the third row becomes the header), renames
    the columns based on groups, and reshapes the DataFrame into a long (tidy) format
    with one row per school per year.

    Args:
        file_path (str): The path to the dropout data Excel file.

    Returns:
        pd.DataFrame: A cleaned, long-format DataFrame of dropout data.
    """
    file_path = "data/Dropout_data.xlsx"
    # Read the "All Students" sheet, skipping the first two rows
    df = pd.read_excel(file_path, sheet_name="All Students", skiprows=2)

    # Print original columns for reference (optional)
    print("Original columns:")
    print(df.columns.tolist())

    # Create new column names based on groups
    new_columns = []
    for col in df.columns:
        # Keep identifier columns as-is.
        if col in ["School ID", "School Name", "Status as of 2024"]:
            new_columns.append(col)
        else:
            col_str = str(col)
            if col_str.isdigit():
                new_columns.append("DropoutRate_" + col_str)
            elif "." in col_str:
                year, suffix = col_str.split(".")
                if suffix == "1":
                    new_columns.append("NumDropouts_" + year)
                elif suffix == "2":
                    new_columns.append("TotalStudents_" + year)
                elif suffix == "3":
                    new_columns.append("AdjustedStudents_" + year)
                else:
                    new_columns.append(col_str)
            else:
                new_columns.append(col_str)

    df.columns = new_columns
    print("\nRenamed columns:")
    print(df.columns.tolist())

    # Reshape the DataFrame from wide to long format
    stubnames = ["DropoutRate", "NumDropouts", "TotalStudents", "AdjustedStudents"]
    id_vars = ["School ID", "School Name", "Status as of 2024"]

    df_long = pd.wide_to_long(
        df, stubnames=stubnames, i=id_vars, j="Year", sep="_", suffix=r"\d{4}"
    ).reset_index()

    print("\nLong-format DataFrame preview:")
    print(df_long.head())

    return df_long


# Merge Function: Merge Dropout CSV with API CSV


def merge_school_data(
    dropout_csv_path: str, api_csv_path: str, output_csv_path: str
) -> pd.DataFrame:
    """
    Merge dropout data with school profile data from the API.

    Args:
        dropout_csv_path (str): File path to the CSV file with dropout data.
        api_csv_path (str): File path to the CSV file created from the API.
        output_csv_path (str): File path to save the merged CSV.

    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    # Read both CSV files
    dropout_df = pd.read_csv(dropout_csv_path)
    api_df = pd.read_csv(api_csv_path)

    # Ensure that the "School ID" columns are of type string
    dropout_df["School ID"] = dropout_df["School ID"].astype(str)
    api_df["School ID"] = api_df["School ID"].astype(str)

    # Merge on "School ID" using a left join
    merged_df = pd.merge(dropout_df, api_df, on="School ID", how="left")

    # Save merged DataFrame to a CSV file
    merged_df.to_csv(output_csv_path, index=False)
    print(f"Merged data saved to {output_csv_path}")

    return merged_df


# Main execution block
def main_education():
    school_ids = get_all_school_ids()
    if school_ids:
        school_profiles_df = fetch_school_profiles(school_ids)
        api_csv_path = "data/cps_school_profiles.csv"
        save_to_csv(school_profiles_df, filename=api_csv_path)
    else:
        print("No school IDs fetched from the API.")

    # Clean the dropout data from Excel and save to CSV (if needed)
    dropout_excel_path = "data/Dropout_data.xlsx"
    dropout_df_long = clean_dropout_data(dropout_excel_path)
    dropout_csv_path = "data/cleaned_dropout_data.csv"
    dropout_df_long.to_csv(dropout_csv_path, index=False)
    print(f"Cleaned dropout data saved to {dropout_csv_path}")

    # Merge the dropout data with the API education data
    merged_csv_path = "data/merged_school_data.csv"
    try:
        merged_data = merge_school_data(dropout_csv_path, api_csv_path, merged_csv_path)
        print("\nMerged DataFrame preview:")
        print(merged_data.head())
    except FileNotFoundError as e:
        print(f"Error: {e}\nPlease ensure the dropout CSV path is correct.")


if __name__ == "__main__":
    # Fetch and save education data from API
    main_education()
