import requests
import pandas as pd

# Define the API endpoint
url = "https://api.census.gov/data/2023/acs/acs1/pums?get=PUMA,SEX,PWGTP,MAR&SCHL=23"

# Make the GET request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()  # Convert JSON response to Python list
else:
    print("Failed to fetch data:", response.status_code)
    data = None

# Convert to DataFrame if data is available
if data:
    df = pd.DataFrame(data[1:], columns=data[0])  # First row is headers
    print(df.head())  # Print the first few rows for a quick look
else:
    print("No data available")