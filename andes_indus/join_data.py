from crime_utils import Crime
from merge_shp import assign_puma, School
import pandas as pd
from quadtree import Quadtree

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

    if type(data_lst[0]) is Crime:
        final_data = data.groupby([group, 'year', 'primary_type']).size().reset_index(name='Count')
        final_data = final_data.pivot_table(index=['puma', 'year'], columns='primary_type', values='Count', fill_value=0)
        final_data = final_data.reset_index()
    else:
        numeric_cols = ['student_count', 'graduation_rate']
        boolean_cols = ['is_high_school', 'is_middle_school', 'is_ele_school', 'is_pre_school']
        data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
        data[boolean_cols] = data[boolean_cols].astype(bool)
        final_data = data.groupby('puma').agg(
            num_schools=('id', 'count'),
            num_high_schools=('is_high_school', 'sum'),
            num_middle_schools=('is_middle_school', 'sum'),
            num_ele_schools=('is_ele_school', 'sum'),
            num_pre_schools=('is_pre_school', 'sum'),
            total_students=('student_count', 'sum')
            ).reset_index()
        grad_rate = data[data['is_high_school']].groupby('puma').apply(
            lambda x: (x['graduation_rate'] * x['student_count']).sum() / x['student_count'].sum()
            if x['graduation_rate'].notna().any() else None
            ).reset_index(name='weighted_hs_grad_rate')
        final_data = final_data.merge(grad_rate, on='puma', how='left')
    return final_data
    