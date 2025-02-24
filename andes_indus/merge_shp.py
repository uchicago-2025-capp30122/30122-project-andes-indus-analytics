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

class Education(NamedTuple):
    school_id : str
    school_name : str
    school_latitude : float
    school_longitude : float
    school_student_count : float
    school_is_high_school : bool
    school_is_middle_school : bool
    school_is_pre_school : bool
    school_is_ele_school : bool
    school_attendance_rate : float
    school_graduation_rate : float
    school_add_street : str
    school_add_state : str
    school_add_zipcode : float


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

def assign_puma(quadtree: Quadtree, crime: Crime) -> str:
    
    crime_shp = Point(crime.longitude, crime.latitude)
    match_lst = quadtree.match(crime_shp)

    if len(match_lst) == 0:
        return None
    return match_lst[0]