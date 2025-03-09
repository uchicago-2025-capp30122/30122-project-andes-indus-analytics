import pytest
import random
from andes_indus.merge_shp import (load_pumas_shp, 
                                   load_neighborhood_shp, 
                                   load_schools,
                                   assign_puma_neighborhood,
                                   gen_quadtree,
                                   gen_chi_bbox,
                                   School)
from andes_indus.crime_utils import process_results
from pathlib import Path
import pandas as pd

path_pumas2020 = Path("data/shapefiles/pumas/pumas2022")
pumas2020 = load_pumas_shp(path_pumas2020,2020)
quadtree_chi_pumas2020 = gen_quadtree(pumas2020, gen_chi_bbox(pumas2020))

path_pumas2010 = Path("data/shapefiles/pumas2010/pumas2010")
pumas2010 = load_pumas_shp(path_pumas2010,2010)
quadtree_chi_pumas2010 = gen_quadtree(pumas2010, gen_chi_bbox(pumas2010))

path_neighborhoods = Path("data/shapefiles/chicomm/chicomm")
neighborhoods = load_neighborhood_shp(path_neighborhoods)
quadtree_chi_neighborhoods = gen_quadtree(neighborhoods, gen_chi_bbox(neighborhoods))

path_schools = Path("data/merged_school_data.csv")
schools = load_schools(path_schools)

crime_sample = [
    {
        "case_number": "HW229606",
        "latitude": 41.770565416,
        "longitude": -87.702945412,
        "block": "067XX S KEDZIE AVE",
        "year": 2023,
        "date": "2023-04-12T08:30:00.000",
        "primary_type": "HOMICIDE",
        "description": "FIRST DEGREE MURDER",
        "puma": '03165',
        "neighborhood": "0066"
    },
    {
        "case_number": "JF324889",
        "latitude": 41.931829482,
        "longitude": -87.723840371,
        "block": "038XX W DIVERSEY AVE",
        "year": 2023,
        "date": "2023-02-08T00:00:00.000",
        "primary_type": "OFFENSE INVOLVING CHILDREN",
        "description": "AGGRAVATED CRIMINAL SEXUAL ABUSE BY FAMILY MEMBER",
        "puma": '03155',
        "neighborhood": "0021"
    },
    {
        "case_number": "HW481136",
        "latitude": 41.873229682,
        "longitude": -87.720354876,
        "block": "006XX S INDEPENDENCE BLVD",
        "year": 2023,
        "date": "2023-10-05T12:00:00.000",
        "primary_type": "CRIMINAL SEXUAL ASSAULT",
        "description": "NON-AGGRAVATED",
        "puma": '03158',
        "neighborhood": "0027"
    },
    {
        "case_number": "HW336307",
        "latitude": 41.750112571,
        "longitude": -87.703028287,
        "block": "032XX W COLUMBUS AVE",
        "year": 2023,
        "date": "2023-06-26T15:50:00.000",
        "primary_type": "ROBBERY",
        "description": "ARMED - HANDGUN",
        "puma": '03164', 
        "neighborhood": "0070"
    },
    {
        "case_number": "HW244724",
        "latitude": 41.74084104,
        "longitude": -87.648618464,
        "block": "084XX S MORGAN ST",
        "year": 2023,
        "date": "2023-04-23T08:08:00.000",
        "primary_type": "BURGLARY",
        "description": "FORCIBLE ENTRY",
        "puma": '03166',
        "neighborhood": "0071"
    }
]

crime_lists = process_results(pd.DataFrame(crime_sample), [], False)

def test_load_pumas():
    assert len(pumas2020) == 18
    assert len(pumas2010) == 17

def test_load_neighborhood():
    assert len(neighborhoods) == 77

def test_load_schools():
    assert len(schools) == 3220

def test_assign_pumas():
    crimes_by_puma = assign_puma_neighborhood(crime_lists, quadtree_chi_pumas2020, 'puma')
    assigned_pumas = crimes_by_puma.puma.unique()
    correct_pumas = pd.DataFrame(crime_sample).puma.unique()
    for ix, item in enumerate(assigned_pumas):
        assert item == correct_pumas[ix]

    shorted_list = [schools[ix] for ix in range(0,2500,500)]
    schools_by_puma = assign_puma_neighborhood(shorted_list, quadtree_chi_pumas2020, 'puma')
    assigned_pumas = schools_by_puma.puma.unique()
    correct_pumas = ['03152', '03158', '03159', '03161', '03161']
    for ix, item in enumerate(assigned_pumas):
        assert item == correct_pumas[ix]

def test_assign_neighborhoods():
    crimes_by_neigh = assign_puma_neighborhood(crime_lists, quadtree_chi_neighborhoods, 'neighborhood')
    assigned_neighborhoods = crimes_by_neigh.neighborhood.unique()
    correct_neighborhoods = pd.DataFrame(crime_sample).neighborhood.unique()
    for ix, item in enumerate(assigned_neighborhoods):
        assert item == correct_neighborhoods[ix]

    