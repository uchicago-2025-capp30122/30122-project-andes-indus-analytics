from crime_utils import Crime
from merge_shp import (
    load_pumas_shp,
    load_neighborhood_shp,
    gen_chi_bbox,
    gen_quadtree,
    load_schools,
    assign_division,
    School,
)
import pandas as pd
from quadtree import Quadtree
import os
from sodapy import Socrata
from crime_utils import get_crime_data, Crime
from pathlib import Path
from education import get_all_school_ids, fetch_school_profiles, save_to_csv
from census_utils import process_multiple_years
import geopandas as gpd


def assign_puma_to_list(
    data_lst: list[Crime | School], quadtree_chi: Quadtree
) -> list[Crime | School]:
    new_data_lst = []
    for point in data_lst:
        new_puma = assign_division(quadtree_chi, point)
        if new_puma is None:
            continue
        else:
            if type(point) == Crime:
                new_data_lst.append(
                    Crime(*point[:-2], puma=new_puma, neighborhood=point[-1])
                )
            elif type(point) == School:
                new_data_lst.append(
                    School(*point[:-2], puma=new_puma, neighborhood=point[-1])
                )
    return new_data_lst


def assign_neighborhood_to_list(
    data_lst: list[Crime | School], quadtree_chi: Quadtree
) -> list[Crime | School]:
    new_data_lst = []
    for point in data_lst:
        new_neighborhood = assign_division(quadtree_chi, point)
        if new_neighborhood is None:
            continue
        else:
            if type(point) == Crime:
                new_data_lst.append(Crime(*point[:-1], neighborhood=new_neighborhood))
            elif type(point) == School:
                new_data_lst.append(School(*point[:-1], neighborhood=new_neighborhood))
    return new_data_lst
    pass


def data_list_to_dataframe(data_lst: list[Crime | School]) -> pd.DataFrame:
    return pd.DataFrame(data_lst)


def grouped_data_by(
    data_lst: list[Crime | School], quadtree_chi: Quadtree, group: str
) -> pd.DataFrame:
    assert group in ("puma", "neighborhood")
    if group == "puma":
        new_data_lst = assign_puma_to_list(data_lst, quadtree_chi)
    else:
        new_data_lst = assign_neighborhood_to_list(data_lst, quadtree_chi)

    data = data_list_to_dataframe(new_data_lst)

    if type(data_lst[0]) is Crime:
        final_data = (
            data.groupby([group, "year", "primary_type"])
            .size()
            .reset_index(name="Count")
        )
        final_data = final_data.pivot_table(
            index=[group, "year"], columns="primary_type", values="Count", fill_value=0
        )
        final_data = final_data.reset_index()
        final_data["total_crimes"] = final_data.drop(columns=[group, "year"]).sum(
            axis=1
        )
    else:
        numeric_cols = ["student_count", "graduation_rate"]
        boolean_cols = [
            "is_high_school",
            "is_middle_school",
            "is_ele_school",
            "is_pre_school",
        ]
        data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors="coerce")
        data[boolean_cols] = data[boolean_cols].astype(bool)
        final_data = (
            data.groupby(group)
            .agg(
                num_schools=("id", "count"),
                num_high_schools=("is_high_school", "sum"),
                num_middle_schools=("is_middle_school", "sum"),
                num_ele_schools=("is_ele_school", "sum"),
                num_pre_schools=("is_pre_school", "sum"),
                total_students=("student_count", "sum"),
            )
            .reset_index()
        )
        grad_rate = (
            data[data["is_high_school"]]
            .groupby(group)
            .apply(
                lambda x: (x["graduation_rate"] * x["student_count"]).sum()
                / x["student_count"].sum()
                if x["graduation_rate"].notna().any()
                else None
            )
            .reset_index(name="weighted_hs_grad_rate")
        )
        final_data = final_data.merge(grad_rate, on=group, how="left")
        final_data["year"] = 2023
    return final_data


def lower_colnames(data: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function to lower all columns of a dataframe before merging
    """
    data.columns = data.columns.str.lower()
    return data


def gen_final_data():
    # Creating the APP Key for the data sources.
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

    # Gathering education data
    path_schools = Path("data/cps_school_profiles.csv")
    if path_schools.exists():
        schools_data = load_schools(path_schools)
    else:
        school_ids = get_all_school_ids()  # Fetch School IDs
        if school_ids:
            school_profiles_df = fetch_school_profiles(
                school_ids
            )  # Fetch selected school details
            save_to_csv(school_profiles_df)
        schools_data = load_schools(path_schools)

    # Gathering census data
    path_census = Path("data/census_df.csv")
    if path_census.exists():
        census_data = lower_colnames(pd.read_csv(path_census))
    else:
        process_multiple_years(path_census)
        census_data = lower_colnames(pd.read_csv(path_census))

    # Merging crime and school data to pumas
    path_pumas = Path("data/shapefiles/pumas/pumas2022")
    pumas = load_pumas_shp(path_pumas)
    quadtree_chi_pumas = gen_quadtree(pumas, gen_chi_bbox(pumas))
    crimes_by_puma = lower_colnames(
        grouped_data_by(crime_data, quadtree_chi_pumas, "puma")
    )
    schools_by_puma = lower_colnames(
        grouped_data_by(schools_data, quadtree_chi_pumas, "puma")
    )

    pumas_shp = gpd.read_file("data/shapefiles/pumas/pumas2022.shp")
    pumas_shp = pumas_shp.rename(columns={"PUMACE20": "puma"})
    pumas_shp["puma"] = pumas_shp["puma"].astype(dtype=str).str.zfill(5)

    pumas_shp = lower_colnames(pumas_shp)

    census_data["puma"] = census_data["puma"].astype(dtype=str).str.zfill(5)
    data_pumas = pd.merge(
        crimes_by_puma, schools_by_puma, how="inner", on=["puma", "year"]
    )
    data_pumas = pd.merge(data_pumas, census_data, how="inner", on=["puma", "year"])
    data_pumas = pd.merge(data_pumas, pumas_shp, how="inner", on=["puma"])
    data_pumas.to_csv("data/data_pumas.csv")

    # Merging crime and school data to neighborhoods
    path_neighborhoods = Path("data/shapefiles/chicomm/chicomm")
    neighborhoods = load_neighborhood_shp(path_neighborhoods)
    quadtree_chi_neighborhoods = gen_quadtree(
        neighborhoods, gen_chi_bbox(neighborhoods)
    )
    crimes_by_neighborhood = lower_colnames(
        grouped_data_by(crime_data, quadtree_chi_neighborhoods, "neighborhood")
    )
    schools_by_neighborhood = lower_colnames(
        grouped_data_by(schools_data, quadtree_chi_neighborhoods, "neighborhood")
    )

    neighborhoods_shp = gpd.read_file("data/shapefiles/chicomm/chicomm.shp")
    neighborhoods_shp = neighborhoods_shp.rename(columns={"CHICOMNO": "neighborhood"})

    data_neighborhoods = pd.merge(
        crimes_by_neighborhood,
        schools_by_neighborhood,
        how="inner",
        on=["neighborhood", "year"],
    )
    data_neighborhoods = pd.merge(
        data_neighborhoods, neighborhoods_shp, how="inner", on=["neighborhood"]
    )

    data_neighborhoods.to_csv("data/data_neighborhoods.csv")
