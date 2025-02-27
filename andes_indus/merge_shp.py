from shapely.geometry import Polygon, MultiPolygon, Point
from quadtree import Quadtree, BBox
from crime_utils import Crime
from typing import NamedTuple
import pathlib
import shapefile
import csv

class Puma(NamedTuple):
    id : str
    name : str
    polygon: Polygon

class Neighborhood(NamedTuple):
    id : str
    name : str
    multi_polygon: MultiPolygon

class School(NamedTuple):
    id : str
    name : str
    latitude : float
    longitude : float
    student_count : float
    is_high_school : bool
    is_middle_school : bool
    is_pre_school : bool
    is_ele_school : bool
    attendance_rate : float
    graduation_rate : float
    add_street : str
    add_state : str
    add_zipcode : float
    puma: None | str

def load_pumas_shp(path: pathlib.Path) -> list[Puma]:
    pumas = []
    with shapefile.Reader(path) as sf:
        for shape_rec in sf.shapeRecords():
            if shape_rec.record[3].startswith("Chicago City"):
                pumas.append(Puma(
                    id = shape_rec.record[1],
                    name = shape_rec.record[3],
                    polygon = Polygon(shape_rec.shape.points))
                )
    return pumas

def load_neighborhood_shp(path: pathlib.Path) -> list[Neighborhood]:
    neighborhoods = []
    with open(path, 'r') as file:
        data = csv.DictReader(file)
        for row in data:
            neighborhoods.append(Neighborhood(
                id = row['AREA_NUMBE'],
                name = row['COMMUNITY'],
                multi_polygon = row['the_geom']
                ))
    return neighborhoods

def load_schools(path: pathlib.Path) -> list[School]:
    """
    Given a CSV containing facility data, return a list of Facility objects.
    """
    schools = []
    with open(path) as f:
        data = csv.DictReader(f)
        for row in data:
            schools.append(
                School(row["School ID"], row["School Name"], row["Latitude"], row["Longitude"],
                       row['Student Count'],row['Is High School'],row['Is Middle School'],
                       row['Is Pre School'],row['Is Elementarty School'],row['Atttendance Rate Current Year'],
                       row['Graduation Rate'],row['Address Street'],row['Address State'],row['Address Zip Code'],
                       None)
            )
    return schools

def gen_chi_bbox(pumas: list[Puma]):
    min_lon = min(p.polygon.bounds[0] for p in pumas)  # min x (longitude)
    min_lat = min(p.polygon.bounds[1] for p in pumas)  # min y (latitude)
    max_lon = max(p.polygon.bounds[2] for p in pumas)  # max x (longitude)
    max_lat = max(p.polygon.bounds[3] for p in pumas)  # max y (latitude)

    chi_bbox = BBox(min_lon, min_lat, max_lon, max_lat)

    return chi_bbox

def gen_quadtree(pumas: list[Puma], chi_bbox: BBox):
    '''
    Helper function to create a quadtree for the pumas o neighborhoods 
    '''
    capacity = 5
    quadtree = Quadtree(chi_bbox, capacity)

    for puma in pumas:
        quadtree.add_polygon(puma.id, puma.polygon)
    
    return quadtree

def assign_puma(quadtree: Quadtree, location: Crime|School) -> str:
    
    loc_point = Point(location.longitude, location.latitude)
    match_lst = quadtree.match(loc_point)

    if len(match_lst) == 0:
        return None
    return match_lst[0]

def assign_neighborhood(quadtree: Quadtree, location: Crime|School) -> str:
    loc_point = Point(location.longitude, location.latitude)
    match_lst = quadtree.match(loc_point)

    if len(match_lst) == 0:
        return None
    return match_lst[0]