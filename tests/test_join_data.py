import pytest
import random
import pandas as pd
import datetime
from pathlib import Path
from andes_indus.join_data import (lower_colnames,
                                   zero_fill_cols,
                                   transform_to_long_format)

# Sample data options
primary_types = ["THEFT", "BATTERY", "CRIMINAL DAMAGE", "ASSAULT", "BURGLARY"]
descriptions = ["OVER $500", "SIMPLE", "TO VEHICLE", "AGGRAVATED", "FORCIBLE ENTRY"]
neighborhoods = ["Loop", "Hyde Park", "Lincoln Park", "Englewood", "Chinatown"]
crime_types = ["violent", "non-violent"]
blocks = ["010XX W ADDISON ST", "035XX S MICHIGAN AVE", "078XX S HALSTED ST"]
pumas = [3168, 3169, 3170]

colnames = ['case_number','latitude','longitude',
            'block','year','date','primary_type',
            'description','puma','neighborhood',
            'crime_type']

# Function to generate random mock data
def generate_mock_data(n:int) -> pd.DataFrame:
    data = []
    for _ in range(n):
        data.append({
            "Case_number": f"JC{random.randint(100000, 999999)}",
            "Latitude": round(random.uniform(41.60, 42.05), 6),
            "Longitude": round(random.uniform(-87.90, -87.50), 6),
            "Block": random.choice(blocks),
            "Year": random.randint(2015, 2025),
            "Date": datetime.datetime(
                random.randint(2015, 2025), random.randint(1, 12), random.randint(1, 28)
            ).strftime("%Y-%m-%d"),
            "Primary_type": random.choice(primary_types),
            "Description": random.choice(descriptions),
            "Puma": random.choice(pumas),
            "Neighborhood": random.choice(neighborhoods),
            "cRime_type": random.choice(crime_types),
        })
    
    return pd.DataFrame(data)

# Generate mock data
crime_mock_data = generate_mock_data(30)

def test_lower_colnames():
    lower_df = lower_colnames(crime_mock_data)
    assert list(lower_df.columns) == colnames

def test_zero_fill_cols():
    crime_df = zero_fill_cols(lower_colnames(crime_mock_data),'puma',5)

    for item in crime_df['puma'].unique():
        assert len(item) == 5

def test_transform_to_long():
    path = Path("data/census_df.csv")
    df = pd.read_csv(path)
    long_df = transform_to_long_format(path, ['PUMA', 'year'],
                                  'indicator', 'value')
    
    num_ids = len(df.loc[:,['PUMA','year']]) # number of unique ids
    num_vars = len(df.columns) - 2 # Number of variables without the id vars
    assert len(long_df) == num_ids * num_vars

