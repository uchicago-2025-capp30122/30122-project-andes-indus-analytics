import os
from sodapy import Socrata
from .crime_utils import get_crime_data, Crime
from .merge_shp import load_pumas_shp, load_neighborhood_shp, gen_chi_bbox, gen_quadtree, assign_puma, load_schools, School
from .census_utils import process_multiple_years
import pandas as pd
from pathlib import Path
from .education import get_all_school_ids, fetch_school_profiles, save_to_csv
from .quadtree import Quadtree

def assign_puma_to_list(data_lst: list[Crime|School], quadtree_chi: Quadtree) -> list[Crime|School]:
    new_data_lst = []
    for point in data_lst:
        new_puma = assign_puma(quadtree_chi, point)
        if new_puma is None:
            continue
        else:
            if type(point) == Crime:
                new_data_lst.append(Crime(*point[:-1], puma = new_puma))
            elif type(point) == School:
                new_data_lst.append(School(*point[:-1], puma = new_puma))
    return new_data_lst

def assign_neighborhood_to_list(data_lst: list[Crime|School], quadtree_chi: Quadtree) -> list[Crime|School]:
    # NEED TO MODIFY THIS FUNCTION
    #  new_data_lst = []
    # for point in data_lst:
    #     new_puma = assign_puma(quadtree_chi, point)
    #     if new_puma is None:
    #         continue
    #     else:
    #         if type(point) == Crime:
    #             new_data_lst.append(Crime(*point[:-1], puma = new_puma))
    #         elif type(point) == School:
    #             new_data_lst.append(School(*point[:-1], puma = new_puma))
    # return new_data_lst
    pass

def data_list_to_dataframe(data_lst: list[Crime|School]) -> pd.DataFrame:
    return pd.DataFrame(data_lst)

def grouped_data_by(data_lst: list[Crime|School], quadtree_chi: Quadtree, group: str) -> pd.DataFrame:
    assert group in ("puma", 'neighborhood')
    if group == "puma":
        new_data_lst = assign_puma_to_list(data_lst, quadtree_chi)
    else:
        new_data_lst = assign_neighborhood_to_list(data_lst, quadtree_chi)
    
    data = data_list_to_dataframe(new_data_lst)

    if data_lst[0] is Crime:
        final_data = data.groupby([group, 'year', 'primary_type']).size().reset_index(name='Count')
    else:
        pass

    return final_data
    