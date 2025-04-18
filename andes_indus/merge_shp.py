from shapely.geometry import Polygon, MultiPolygon, Point
from .quadtree import Quadtree, BBox
from .crime_utils import Crime
from typing import NamedTuple, Optional
import pathlib
import shapefile
import csv
import pandas as pd


class Puma(NamedTuple):
    id: str
    name: str
    polygon: Polygon


class Neighborhood(NamedTuple):
    id: str
    name: str
    polygon: Polygon


class School(NamedTuple):
    id: str
    name: str
    latitude: float
    longitude: float
    student_count: float
    is_high_school: bool
    is_middle_school: bool
    is_pre_school: bool
    is_ele_school: bool
    attendance_rate: float
    graduation_rate: float
    add_street: str
    add_state: str
    add_zipcode: float
    status_as_of_2024: Optional[str]
    year: int
    dropout_rate: Optional[float]
    num_dropouts: Optional[int]
    total_students_dropout: Optional[int]
    adjusted_students: Optional[int]
    puma: None | str
    neighborhood: None | str


def load_pumas_shp(path: pathlib.Path, pumas_year: int) -> list[Puma]:
    """
    Creates a list of Pumas objects

    Inputs: 
        - path: path from a shapefile
        - pumas_year: year from the correspondent shapefile
    """
    name_dict = {2010: 4, 2020: 3}

    pumas = []
    with shapefile.Reader(path) as sf:
        for shape_rec in sf.shapeRecords():
            if shape_rec.record[name_dict[pumas_year]].startswith("Chicago City"):
                pumas.append(
                    Puma(
                        id=shape_rec.record[1],
                        name=shape_rec.record[name_dict[pumas_year]],
                        polygon=Polygon(shape_rec.shape.points),
                    )
                )
    return pumas


def load_neighborhood_shp(path: pathlib.Path) -> list[Neighborhood]:
    '''
    Creates a list of Neighborhood objects

    Inputs:
        - path: path from a shapefile
    '''
    neighborhood = []
    with shapefile.Reader(path) as sf:
        for shape_rec in sf.shapeRecords():
            neighborhood.append(
                Neighborhood(
                    id=shape_rec.record[0],
                    name=shape_rec.record[2],
                    polygon=Polygon(shape_rec.shape.points),
                )
            )
    return neighborhood


def load_schools(path: pathlib.Path) -> list[School]:
    """
    Given a CSV containing facility data, return a list of School objects.
    """
    schools = []
    with open(path) as f:
        data = csv.DictReader(f)
        for row in data:
            schools.append(
                School(
                    row["School ID"],
                    row["School Name_x"],
                    row["Latitude"],
                    row["Longitude"],
                    row["Student Count"],
                    row["Is High School"],
                    row["Is Middle School"],
                    row["Is Pre School"],
                    row["Is Elementarty School"],
                    row["Atttendance Rate Current Year"],
                    row["Graduation Rate"],
                    row["Address Street"],
                    row["Address State"],
                    row["Address Zip Code"],
                    row["Status as of 2024"],
                    row["Year"],
                    row["DropoutRate"],
                    row["NumDropouts"],
                    row["TotalStudents"],
                    row["AdjustedStudents"],
                    None,
                    None,
                )
            )
    return schools


def gen_chi_bbox(division: list[Puma | Neighborhood]):
    '''
    Helper function to create a Chicago BBox object from a given list of Puma or 
    Neighborhood
    '''
    min_lon = min(p.polygon.bounds[0] for p in division)  # min x (longitude)
    min_lat = min(p.polygon.bounds[1] for p in division)  # min y (latitude)
    max_lon = max(p.polygon.bounds[2] for p in division)  # max x (longitude)
    max_lat = max(p.polygon.bounds[3] for p in division)  # max y (latitude)

    chi_bbox = BBox(min_lon, min_lat, max_lon, max_lat)

    return chi_bbox


def gen_quadtree(division: list[Puma | Neighborhood], chi_bbox: BBox):
    """
    Helper function to create a quadtree for the Pumas o Neighborhoods
    """
    capacity = 5
    quadtree = Quadtree(chi_bbox, capacity)

    for div in division:
        quadtree.add_polygon(div.id, div.polygon)

    return quadtree


def assign_division(quadtree: Quadtree, location: Crime | School) -> str:
    '''
    Helper function to assign a Puma or Neighborhood to a specified Crime or 
    School object.
    '''
    if (location.longitude == "") or (location.latitude == ""):
        return None
    else:
        loc_point = Point(float(location.longitude), float(location.latitude))
        match_lst = quadtree.match(loc_point)
        if len(match_lst) == 0:
            return None
        return match_lst[0]


def assign_puma_to_list(
    data_lst: list[Crime | School], quadtree_chi: Quadtree
) -> list[Crime | School]:
    '''
    Helper function to assign a Puma to a list of Crime or School objects
    '''
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
    '''
    Helper function to assign a Neigborhood to a list of Crime or School objects
    '''
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


def assign_puma_neighborhood(
    data_lst: list[Crime | School], quadtree_chi: Quadtree, group: str
) -> pd.DataFrame:
    '''
    Final function that creates a pd.DataFrame at Crime or School level with the 
    information of the correspondent Puma or Neighborhood.
    '''
    assert group in ("puma", "neighborhood")
    if group == "puma":
        new_data_lst = assign_puma_to_list(data_lst, quadtree_chi)
    else:
        new_data_lst = assign_neighborhood_to_list(data_lst, quadtree_chi)

    return pd.DataFrame(new_data_lst)
