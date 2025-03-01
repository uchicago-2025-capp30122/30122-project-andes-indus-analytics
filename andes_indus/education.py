import requests
import pandas as pd


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
        school_ids = {
            school["SchoolID"] for school in data
        }  # Extracting School IDs into a set
        return school_ids
    else:
        print(f" Error fetching school IDs: {response.status_code}")
        return set()


# Step 2: Fetch Required School Data
def fetch_school_profiles(
    school_ids,
    api_base_url="https://api.cps.edu/schoolprofile/CPS/SingleSchoolProfile?SchoolID={SchoolID}",
):
    """
    Fetch only selected school profile data for a list of school IDs from the CPS API.

    Args:
        school_ids (set): A set of school IDs to query.
        api_base_url (str): Base URL of the API endpoint.

    Returns:
        pd.DataFrame: A DataFrame containing selected school profile data.
    """
    school_profiles = []

    for school_id in school_ids:
        url = api_base_url.replace(
            "{SchoolID}", str(school_id)
        )  # Correct URL formatting
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
                        "Address State": data.get(
                            "AddressState", "N/A"
                        ),  # Default to "N/A" if missing
                        "Address Street": data.get("AddressStreet", "N/A"),
                        "Address Zip Code": data.get("AddressZipCode", "N/A"),
                        "Is High School": bool(data.get("IsHighSchool", False)),
                        "Is Middle School": bool(data.get("IsMiddleSchool", False)),
                        "Is Elementarty School": bool(
                            data.get("IsElementarySchool", False)
                        ),
                        "Is Pre School": bool(data.get("IsPreSchool", False)),
                    }
                )
        else:
            print(
                f" Error fetching data for School ID {school_id}: {response.status_code}"
            )

    # Convert the list of dictionaries into a DataFrame
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
    print(f" Data saved to {filename}")


if __name__ == "__main__":
    school_ids = get_all_school_ids()  # Fetch School IDs
    if school_ids:
        school_profiles_df = fetch_school_profiles(
            school_ids
        )  # Fetch selected school details
        save_to_csv(school_profiles_df)
