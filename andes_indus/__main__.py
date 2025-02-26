import argparse
import os
from sodapy import Socrata
from crime_utils import get_crime_data, Crime
from merge_shp import load_pumas_shp, load_neighborhood_shp, gen_chi_bbox, gen_quadtree, assign_puma, load_schools, School
from census_utils import process_multiple_years
import pandas as pd
from pathlib import Path
from education import get_all_school_ids, fetch_school_profiles, save_to_csv
import folium as fm
import geopandas as gpd
import webbrowser

def main():


    # Creating all the API and APP Keys for the data sources. 
    try:
        CHICAGO_APP_TOKEN = os.environ["CHICAGO_APP_TOKEN"]
    except KeyError:
        raise Exception(
            "Make sure that you have set the APP Token environment variable as described in the README."
        )

    # Gathering the crime data from the City of Chicago Data web
    client = Socrata("data.cityofchicago.org", CHICAGO_APP_TOKEN, timeout=10)
    crime_code = "ijzp-q8t2"
    homicides_code = "gumc-mgzr"
    lst_years = list(range(2021, 2024))

    # Creating the pd.Dataframes for crime and homicides_data
    crime_data = get_crime_data(client, crime_code, lst_years)
    homicides_data = get_crime_data(client, homicides_code, lst_years)

    # INSERT EDUCATION CODE
    school_ids = get_all_school_ids()  # Fetch School IDs
    if school_ids:
        school_profiles_df = fetch_school_profiles(school_ids)  # Fetch selected school details
        save_to_csv(school_profiles_df)

    path_schools = Path('data/cps_school_profiles.csv')
    schools_data = load_schools(path_schools)

    # INSERT CENSUS CODE
    process_multiple_years("data/census_df.csv")
    census_data = pd.read_csv("data/census_df.csv")

    # Merging crime and school data to pumas
    path_pumas = Path("data/shapefiles/pumas/pumas2022")
    #path_neighborhoods = Path("data/shapefiles/chicago_neighborhoods.csv")
    pumas = load_pumas_shp(path_pumas)
    #neighborhoods = load_neighborhood_shp(path_neighborhoods)

    quadtree_chi = gen_quadtree(pumas, gen_chi_bbox(pumas))

    new_crime_data = []
    for crime in crime_data:
        new_puma = assign_puma(quadtree_chi, crime)
        if new_puma is None:
            continue
        else:
            new_crime_data.append(Crime(*crime[:-1], puma = new_puma))

    new_school_data = []
    for school in schools_data:
        new_puma = assign_puma(quadtree_chi, school)
        if new_puma is None:
            continue
        else:
            new_school_data.append(School(*school[:-1], puma = new_puma))

    crimes = pd.DataFrame(new_crime_data)
    schools = pd.DataFrame(new_school_data)

    pumas_shp = gpd.read_file('data/shapefiles/pumas/pumas2022.shp')
    z = fm.Map(location = [41.8783874319104, -87.62875352665596], tiles='cartodbpositron', zoom_start = 10.5)

    fm.Choropleth(
        geo_data=pumas_shp,
        data=census_data,
        columns=['PUMA', 'attendance_rate_high'],
        key_on="feature.properties.PUMACE20",
        fill_color="YlOrRd",
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name="Attendance rate (%)",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        overlay=True,
        nan_fill_color = "White"  # fill white missing values 
        ).add_to(z)

    z.save("visualizations/high_school_rate.html")
    

if __name__ == "__main__":
    main()
    html = Path("visualizations/high_school_rate.html")
    webbrowser.open_new_tab(html)