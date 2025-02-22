from shapely.geometry import Polygon, MultiPolygon, Point
from .quadtree import Quadtree, BBox
from typing import NamedTuple
import pathlib
import shapefile
import csv

class Crime(NamedTuple):
    case_number : str
    latitude: float
    longitude: float

class Puma(NamedTuple):
    id : str
    name : str
    polygon: Polygon

class Neighborhood(NamedTuple):
    id : str
    name : str
    multi_polygon: MultiPolygon

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

def assign_puma(pumas: list[Puma], chi_bbox: BBox, crime: Crime) -> list:

    capacity = 5
    quadtree = Quadtree(chi_bbox, capacity)

    for puma in pumas:
        quadtree.add_polygon(puma.id, puma.polygon)
    
    crime_shp = Point(crime.longitude, crime.latitude)
    match_lst = quadtree.match(crime_shp)

    return match_lst    