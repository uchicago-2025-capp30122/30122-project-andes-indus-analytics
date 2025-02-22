from typing import NamedTuple
from shapely.geometry import Polygon, box, Point


class QuadtreeError(Exception):
    """Exception used within Quadtree for unexpected cases"""


class BBox(NamedTuple):
    """Named tuple for storing bounding box data."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float


# Maximum depth of a quadtree.
# Do not subdivide nodes if depth exceeds this value.
MAX_DEPTH = 8


class Quadtree:
    """
    Class that represents a node in the quadtree.

    Each node has:
        - bounding box (bbox)
        - capacity
        - depth (first node is depth=0, children would be depth=1, etc.)
        - either children OR polygons
    """

    def __init__(self, bbox: BBox, capacity: int, depth: int = 0):
        self.bbox = bbox
        self.capacity = capacity
        self.depth = depth
        self.polygons = {}
        self.children = []

    def is_split(self) -> bool:
        """
        Check if this node in the quadtree is split.

        Returns:
            True if split, False otherwise.
        """
        if self.children and self.polygons:
            raise QuadtreeError("polygons and children on same node")
        if len(self.children) not in (4, 0):
            raise QuadtreeError("a node must always have 0 or 4 children")
        return bool(self.children)

    def __repr__(self) -> str:
        """
        Return a view of the interior of the node.

        It is not tested, feel free to modify this function however you like.
        """
        if self.is_split():
            return f"Quadtree{list(self.children)}"
        else:
            return f"Quadtree(polygons={len(self.polygons)})"

    def split_quad(self, parent: BBox, capacity: int, depth: int):
        """
        Helper function to compute the split only if exceeded capacity and max
        depth not reached.

        Args:
            - parent: BBox class with parent coordinates
            - capacity: capacity from the parent
            - depth: depth level of the parent
        """
        # Computing mid points from parent's coordinates
        minx, miny, maxx, maxy = parent
        midx, midy = (maxx + minx) / 2, (maxy + miny) / 2

        # Generating the list of children with midpoints
        self.children = [
            Quadtree(BBox(minx, miny, midx, midy), capacity, depth + 1),
            Quadtree(BBox(minx, midy, midx, maxy), capacity, depth + 1),
            Quadtree(BBox(midx, miny, maxx, midy), capacity, depth + 1),
            Quadtree(BBox(midx, midy, maxx, maxy), capacity, depth + 1),
        ]

    def add_to_children(self, id: str, polygon: Polygon):
        """
        Helper function to add polygons to a Quadtree's children when it's already
        splitted.
        """
        for child in self.children:
            # Only computing add_polygon if polygon is inside the box
            if box(*child.bbox).intersects(polygon):
                child.add_polygon(id, polygon)

    def add_polygon(self, id: str, polygon: Polygon) -> bool:
        # Conditional to verify if the Polygon intersects with our Quadtree
        if not box(*self.bbox).intersects(polygon):
            return False

        if not self.is_split():
            # Base case 1: Capacity not reached
            if self.capacity > len(self.polygons):
                self.polygons[id] = polygon
                return True
            # Base case 2: Max depth reached
            elif self.depth >= MAX_DEPTH:
                self.polygons[id] = polygon
                return True
            else:
                # Splitting the quad
                self.split_quad(self.bbox, self.capacity, self.depth)
                # Storing existent polygons
                parent_polygons = list(self.polygons.items()) + [(id, polygon)]
                self.polygons = {}
                # Recursive case 1: Adding one polygon and splitting a quadtree
                for key, val in parent_polygons:
                    self.add_to_children(key, val)
        else:
            # Recursive case 2: Adding one polygon to the childs of an already
            # splitted quadtree
            self.add_to_children(id, polygon)

        return True

    def match(self, point: Point) -> list[str]:
        if not box(*self.bbox).contains(point):
            # Base case 1: Point not inside the BBox
            return []

        # Recursive case: Splitted Quadtree --> Do search on its children
        if self.is_split():
            lst = []
            for child in self.children:
                if box(*child.bbox).contains(point):
                    lst.extend(child.match(point))
            return lst
        else:
            # Base case 2: Not splitted Quadtree --> find ids on self.polygons
            return [
                key for key, value in self.polygons.items() if value.contains(point)
            ]