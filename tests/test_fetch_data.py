import pytest
from andes_indus.api_get import (get_params_for_year,
                                 get_google_drive_files,
                                 chicago_dataframe)

from andes_indus.crime_utils import get_crime_data

from andes_indus.census_utils import (cleaning_data,
                                      social_variables,
                                      education_vars,
                                      aggregate_puma_data)

from andes_indus.education import (get_all_school_ids,
                                   fetch_school_profiles)
from sodapy import Socrata
import os

def test_get_params():
    for year in [2013,2018,2023]:
        assert len(get_params_for_year(year)['get'].split(',')) == 17

def test_get_google_drive_files():
    path_dict = {'census23' : 'https://drive.usercontent.google.com/download?id=1KqviAJthq8RzZa9nVoBS5dp553ix55I7&export=download&authuser=0&confirm=t&uuid=abf16c04-2bbc-48ee-8a9b-9a501f2b315a&at=AEz70l6_lxclQ30xwZyTTaVqhBtR:1740868465146',
                 'census18' : 'https://drive.usercontent.google.com/download?id=1zcP7YJyW5NemZ_FAF2r3Ub-dcAsjYVc7&export=download&authuser=0&confirm=t&uuid=7940c379-4f49-46fa-924a-6055f0c631c5&at=AEz70l5Qlq8c0GftWr8-e9X4u-GA:1741481012388',
                 'crime_by_puma': 'https://drive.usercontent.google.com/download?id=1JUDBpR3ot26PW-2F93pLGkIbZy7dFpF7&export=download&authuser=0&confirm=t&uuid=26c3238d-a65a-449f-a6c0-9195dec5f1b8&at=AEz70l6g5TH5Nh_sh4o71wbuDkur:1741115211114',
                 'crime_by_neighborhood': 'https://drive.usercontent.google.com/download?id=1dUEmZnPna1hQv55Czi38KYIv4Z6oHcZy&export=download&authuser=0&confirm=t&uuid=47ca72e8-6681-453e-8eae-0f6e4730a14d&at=AEz70l5OzlGvfrEsZ2JLIPiaY653:1741115182166',
                 'crime_by_block' :'https://drive.usercontent.google.com/download?id=17lrQgaXcTAQTM4kMqt19RYvC4gtF9wCn&export=download&authuser=0&confirm=t&uuid=f69248de-b684-4c5f-976b-63576e8c9741&at=AEz70l53DiY7nTnR_fRZmhZYPvOx:1741223440221'}

    assert len(get_google_drive_files(path_dict['census23'])) == 3405809
    assert len(get_google_drive_files(path_dict['census18'])) == 3214540
    assert len(get_google_drive_files(path_dict['crime_by_puma'])) == 822278
    assert len(get_google_drive_files(path_dict['crime_by_neighborhood'])) == 827734
    assert len(get_google_drive_files(path_dict['crime_by_block'])) == 831220

def test_chicago_dataframe():
    assert len(chicago_dataframe(2023,'',False)) == 18244
    assert len(chicago_dataframe(2018,'',False)) == 20605
    assert len(chicago_dataframe(2013,'',False)) == 22611

def test_get_crime_data():

    try:
        CHICAGO_APP_TOKEN = os.environ["CHICAGO_APP_TOKEN"]
    except KeyError:
        raise Exception(
            "Make sure that you have set the APP Token environment variable as described in the README."
        )

    # Gathering the crime data from the City of Chicago Data web
    client = Socrata("data.cityofchicago.org", CHICAGO_APP_TOKEN)
    crime_code = "ijzp-q8t2"
    lst_years = [2013, 2018, 2023]

    assert len(get_crime_data(client, crime_code, [2023], True)) == 261243
    assert len(get_crime_data(client, crime_code, lst_years[0:2], True)) == 569977

def test_agg_puma():
    df = chicago_dataframe(2013,"", full_fetch=False)
    assert len(aggregate_puma_data(
                        education_vars(
                            social_variables(
                                cleaning_data(df))))) == 18


api_url="https://api.cps.edu/schoolprofile/CPS/TypeaheadSchoolSearch"

def test_get_all_schools():
    assert len(get_all_school_ids(api_url)) == 649

def test_fetch_school_profiles():
    api_base_url="https://api.cps.edu/schoolprofile/CPS/SingleSchoolProfile?SchoolID={SchoolID}"
    assert len(fetch_school_profiles(get_all_school_ids(api_url),
                                     api_base_url)) == 649