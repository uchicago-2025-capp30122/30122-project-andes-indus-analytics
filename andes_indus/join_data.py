from .merge_shp import (
    load_pumas_shp,
    load_neighborhood_shp,
    gen_chi_bbox,
    gen_quadtree,
    load_schools,
    assign_puma_neighborhood,
)
from .crime_utils import (
    get_all_crime_data,
    load_crime_data,
    classify_violent_crimes,
)
from .education import main_education
from .census_utils import process_multiple_years
from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np


def group_crime_data_by(new_data_lst: pd.DataFrame, group: str) -> pd.DataFrame:
    path = Path(f"data/crime_by_{group}.csv")
    if not path.exists() and (__name__ == "__main__"):
        new_data_lst.to_csv(path)

    new_data_lst = classify_violent_crimes(new_data_lst)

    final_data = (
        new_data_lst.groupby([group, "year", "crime_type"])
        .size()
        .reset_index(name="Count")
    )
    final_data = final_data.pivot_table(
        index=[group, "year"],
        columns="crime_type",
        values="Count",
        fill_value=0,
        aggfunc="sum",
    )
    final_data = final_data.reset_index()
    final_data["total_crimes"] = final_data.drop(columns=[group, "year"]).sum(axis=1)
    return final_data


def group_school_data_by(new_data_lst: pd.DataFrame, group: str) -> pd.DataFrame:
    path = Path(f"data/schools_by_{group}.csv")
    if not path.exists() and (__name__ == "__main__"):
        new_data_lst.to_csv(path)

    numeric_cols = [
        "student_count",
        "graduation_rate",
        "attendance_rate",
        "dropout_rate",
        "num_dropouts",
        "total_students_dropout",
    ]
    boolean_cols = [
        "is_high_school",
        "is_middle_school",
        "is_ele_school",
        "is_pre_school",
    ]
    new_data_lst[numeric_cols] = new_data_lst[numeric_cols].apply(
        pd.to_numeric, errors="coerce"
    )
    new_data_lst[boolean_cols] = new_data_lst[boolean_cols].astype(bool)
    final_data = (
        new_data_lst.groupby([group, "year"])
        .agg(
            num_schools=("id", "count"),
            num_high_schools=("is_high_school", "sum"),
            num_middle_schools=("is_middle_school", "sum"),
            num_ele_schools=("is_ele_school", "sum"),
            num_pre_schools=("is_pre_school", "sum"),
            total_students=("student_count", "sum"),
            num_dropout=("num_dropouts", "sum"),
            total_students_dropout=("total_students_dropout", "sum"),
        )
        .reset_index()
    )
    grad_rate = (
        new_data_lst[new_data_lst["is_high_school"]]
        .groupby([group, "year"])
        .apply(
            lambda x: (x["graduation_rate"] * x["student_count"]).sum()
            / x["student_count"].sum()
            if x["graduation_rate"].notna().any()
            else None
        )
        .reset_index(name="weighted_hs_grad_rate")
    )
    final_data = final_data.merge(grad_rate, on=[group, "year"], how="left")
    return final_data


def lower_colnames(
    data: pd.DataFrame | gpd.GeoDataFrame,
) -> pd.DataFrame | gpd.GeoDataFrame:
    """
    Helper function to lower all columns of a dataframe before merging
    """
    data.columns = data.columns.str.lower()
    return data


def zero_fill_cols(
    df: pd.DataFrame | gpd.GeoDataFrame, colname: str, n_zeros: int
) -> pd.DataFrame | gpd.GeoDataFrame:
    df[colname] = df[colname].astype(dtype=str).str.zfill(n_zeros)
    return df


def gen_pc_stats(df: pd.DataFrame, popvar: str, full_fetch) -> pd.DataFrame:
    if full_fetch:
        cols_dic = {
            "non-violent": "non_violent",
            "violent": "violent",
            "total_crimes": "total_crim",
        }
    else:
        cols_dic = {
            "Non-violent": "non_violent",
            "Violent": "violent",
            "total_crimes": "total_crim",
        }
    df = df.rename(
        columns=cols_dic
    )

    for var in ["total_crim", "violent", "non_violent"]:
        df[f"{var}_pc"] = df[f"{var}"] / df[popvar] * 1000

    return df


def gen_final_data(full_fetch=False):
    # Gathering education data
    path_schools = Path("data/merged_school_data.csv")
    if path_schools.exists():
        schools_data = load_schools(path_schools)
    else:
        main_education()
        schools_data = load_schools(path_schools)

    # Gathering census data
    path_census = Path("data/census_df.csv")
    if path_census.exists():
        census_data = lower_colnames(pd.read_csv(path_census))
    else:
        process_multiple_years(path_census, True)
        census_data = lower_colnames(pd.read_csv(path_census))

    # Merging crime and school data to pumas
    path_pumas2020 = Path("data/shapefiles/pumas/pumas2022")
    pumas2020 = load_pumas_shp(path_pumas2020, 2020)
    quadtree_chi_pumas2020 = gen_quadtree(pumas2020, gen_chi_bbox(pumas2020))

    path_pumas2010 = Path("data/shapefiles/pumas2010/pumas2010")
    pumas2010 = load_pumas_shp(path_pumas2010, 2010)
    quadtree_chi_pumas2010 = gen_quadtree(pumas2010, gen_chi_bbox(pumas2010))

    path_neighborhoods = Path("data/shapefiles/chicomm/chicomm")
    neighborhoods = load_neighborhood_shp(path_neighborhoods)
    quadtree_chi_neighborhoods = gen_quadtree(
        neighborhoods, gen_chi_bbox(neighborhoods)
    )
    # Creating the pd.Dataframes for crime
    if full_fetch:
        crime_data_23, crime_data_1318 = get_all_crime_data()

        crimes_by_puma_23 = assign_puma_neighborhood(
            crime_data_23, quadtree_chi_pumas2020, "puma"
        )
        crimes_by_puma_1318 = assign_puma_neighborhood(
            crime_data_1318, quadtree_chi_pumas2010, "puma"
        )

        crime_data = pd.concat([crimes_by_puma_23, crimes_by_puma_1318])
        crimes_by_puma = lower_colnames(group_crime_data_by(crime_data, "puma"))

        crime_data_23.extend(crime_data_1318)
        crimes_by_neighborhood = lower_colnames(
            group_crime_data_by(
                assign_puma_neighborhood(
                    crime_data_23, quadtree_chi_neighborhoods, "neighborhood"
                ),
                "neighborhood",
            )
        )
    else:
        crime_df_puma, crime_df_neighborhood = load_crime_data()
        crimes_by_puma = group_crime_data_by(crime_df_puma, "puma")
        crimes_by_puma = zero_fill_cols(crimes_by_puma, "puma", 5)
        crimes_by_neighborhood = group_crime_data_by(
            crime_df_neighborhood, "neighborhood"
        )
        crimes_by_neighborhood = zero_fill_cols(
            crimes_by_neighborhood, "neighborhood", 4
        )

    school_data23, school_data1318 = [], []
    for school in schools_data:
        if school.year == "2023":
            school_data23.append(school)
        elif (school.year == "2013") or (school.year == "2018"):
            school_data1318.append(school)

    schools_by_puma23 = lower_colnames(
        group_school_data_by(
            assign_puma_neighborhood(school_data23, quadtree_chi_pumas2020, "puma"),
            "puma",
        )
    )
    schools_by_puma1318 = lower_colnames(
        group_school_data_by(
            assign_puma_neighborhood(school_data1318, quadtree_chi_pumas2010, "puma"),
            "puma",
        )
    )
    schools_by_puma = pd.concat([schools_by_puma23, schools_by_puma1318])

    pumas_shp23 = gpd.read_file(
        "data/shapefiles/pumas/pumas2022.shp",
        columns=["PUMACE20", "NAMELSAD20", "geometry"],
    ).rename(columns={"PUMACE20": "puma", "NAMELSAD20": "name"})
    pumas_shp1318 = gpd.read_file(
        "data/shapefiles/pumas2010/pumas2010.shp",
        columns=["PUMACE10", "NAME10", "geometry"],
    ).rename(columns={"PUMACE10": "puma", "NAME10": "name"})

    pumas_shp = pd.concat([pumas_shp23, pumas_shp1318])
    pumas_shp = zero_fill_cols(pumas_shp, "puma", 5)
    pumas_shp = lower_colnames(pumas_shp)

    census_data["puma"] = (
        census_data["puma"].astype(float).astype(int).astype(dtype=str).str.zfill(5)
    )
    schools_by_puma["year"] = schools_by_puma["year"].astype(int)

    data_pumas = pumas_shp.merge(crimes_by_puma, how="inner", on=["puma"])
    data_pumas = data_pumas.merge(schools_by_puma, how="inner", on=["puma", "year"])
    data_pumas = data_pumas.merge(census_data, how="inner", on=["puma", "year"])
    data_pumas = gen_pc_stats(data_pumas, "pwgtp", full_fetch)
    data_pumas.to_csv("data/data_pumas.csv")
    data_pumas.to_file("data/shapefiles/data_pumas.shp")

    # Merging crime and school data to neighborhoods

    schools_by_neighborhood = lower_colnames(
        group_school_data_by(
            assign_puma_neighborhood(
                schools_data, quadtree_chi_neighborhoods, "neighborhood"
            ),
            "neighborhood",
        )
    )
    neighborhoods_shp = gpd.read_file("data/shapefiles/chicomm/chicomm.shp")
    neighborhoods_shp = neighborhoods_shp.rename(columns={"CHICOMNO": "neighborhood"})
    schools_by_neighborhood["year"] = schools_by_neighborhood["year"].astype(int)
    data_neighborhoods = neighborhoods_shp.merge(
        crimes_by_neighborhood, how="inner", on=["neighborhood"]
    )
    data_neighborhoods = data_neighborhoods.merge(
        schools_by_neighborhood, how="inner", on=["neighborhood", "year"]
    )

    pop_neighborhoods = pd.read_csv("data/pop_neighborhood.csv", delimiter=";")
    pop_neighborhoods = zero_fill_cols(pop_neighborhoods, "neighborhood", 4)
    pop_neighborhoods["pop2020"] = (
        pop_neighborhoods["pop2020"].str.replace(",", "").astype(int)
    )

    data_neighborhoods = data_neighborhoods.merge(
        pop_neighborhoods, how="inner", on=["neighborhood"]
    )

    data_neighborhoods = gen_pc_stats(data_neighborhoods, "pop2020", full_fetch)

    data_neighborhoods.to_csv("data/data_neighborhoods.csv")
    data_neighborhoods.to_file("data/shapefiles/data_neighborhoods.shp")


def transform_to_long_format(
    input_csv: str = "data/census_df.csv",
    id_vars: list = ["PUMA", "year", "puma_label", "cut_name"],
    var_name: str = "indicator",
    value_name: str = "value",
) -> pd.DataFrame:
    """
    Reads a CSV file and transforms it from wide to long format.

    Parameters:
    -----------
    input_csv : str
        Path to the input CSV file.
    id_vars : list
        Columns to keep as identifier variables (they remain 'as is' in the long format).
    var_name : str, optional
        Name of the new column that will store the former wide column names.
    value_name : str, optional
        Name of the new column that will store the values from the melted columns.

    Returns:
    --------
    df_long : pd.DataFrame
        The reshaped DataFrame in long format.
    """

    # 1. Read the CSV
    df = pd.read_csv(input_csv)

    # 2. Reshape from wide to long using melt
    df_long = pd.melt(
        df,
        id_vars=id_vars,  # columns to keep in place
        var_name=var_name,  # new column name for old wide-column headers
        value_name=value_name,  # new column name for the data values
    )
    df_long.to_csv("data/census_df_long.csv", index=False)
    return df_long
