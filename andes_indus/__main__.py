import os
from sodapy import Socrata
from .crime_utils import get_crime_data 
import pandas as pd

# Creating all the API and APP Keys for the data sources. 
try:
    CHICAGO_APP_TOKEN = os.environ["CHICAGO_APP_TOKEN"]
except KeyError:
    raise Exception(
        "Make sure that you have set the APP Token environment variable as described in the README."
    )

# Gathering the crime data from the City of Chicago Data web
client = Socrata("data.cityofchicago.org", CHICAGO_APP_TOKEN, timeout=10)

# Establishing the arguments
crime_code = "ijzp-q8t2"
homicides_code = "gumc-mgzr"
lst_years = list(range(2021, 2024))

# Creating the pd.Dataframes for crime and homicides_data
crime_data = get_crime_data(client, crime_code, lst_years)
homicides_data = get_crime_data(client, homicides_code, lst_years)