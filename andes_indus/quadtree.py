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

    def subdivide(self) -> None:
        """
        Subdivide this node into 4 children.
        A child for quadrant of this node's bounding box.
        """
        # Current bounding box
        minx, miny, maxx, maxy = self.bbox

        # Midpoints
        midx = (minx + maxx) / 2.0
        midy = (miny + maxy) / 2.0

        # four child bounding boxes: NW, NE, SE, SW
        bbox_nw = BBox(minx, midy, midx, maxy)  # northwest
        bbox_ne = BBox(midx, midy, maxx, maxy)  # northeast
        bbox_se = BBox(midx, miny, maxx, midy)  # southeast
        bbox_sw = BBox(minx, miny, midx, midy)  # southwest

        # Create child Quadtrees at the next depth
        self.children = [
            Quadtree(bbox_nw, self.capacity, self.depth + 1),
            Quadtree(bbox_ne, self.capacity, self.depth + 1),
            Quadtree(bbox_se, self.capacity, self.depth + 1),
            Quadtree(bbox_sw, self.capacity, self.depth + 1),
        ]

    def __repr__(self) -> str:
        """
        Return a view of the interior of the node.

        It is not tested, feel free to modify this function however you like.
        """
        if self.is_split():
            return f"Quadtree{list(self.children)}"
        else:
            return f"Quadtree(polygons={len(self.polygons)})"

    def add_polygon(self, id: str, polygon: Polygon) -> bool:
        # 1) Check if polygon intersects the bounding box of this node
        node_box = box(
            self.bbox.min_x, self.bbox.min_y, self.bbox.max_x, self.bbox.max_y
        )

        if not polygon.intersects(node_box):
            return False

        # 2) If this node is already split, pass polygon to the children
        if self.is_split():
            added = False
            for child in self.children:
                child_box = box(
                    child.bbox.min_x,
                    child.bbox.min_y,
                    child.bbox.max_x,
                    child.bbox.max_y,
                )
                if polygon.intersects(child_box):
                    child.add_polygon(id, polygon)
                    added = True
            return added

        # 3) If not split: check capacity
        if len(self.polygons) >= self.capacity and self.depth < MAX_DEPTH:
            # subdivide
            self.subdivide()

            # move existing polygons to children
            old_polygons = self.polygons
            self.polygons = {}  # Clear them from this node

            for pid, poly in old_polygons.items():
                for child in self.children:
                    child_box = box(
                        child.bbox.min_x,
                        child.bbox.min_y,
                        child.bbox.max_x,
                        child.bbox.max_y,
                    )
                    if poly.intersects(child_box):
                        child.add_polygon(pid, poly)

            # Now add the new polygon similarly
            added = False
            for child in self.children:
                child_box = box(
                    child.bbox.min_x,
                    child.bbox.min_y,
                    child.bbox.max_x,
                    child.bbox.max_y,
                )
                if polygon.intersects(child_box):
                    child.add_polygon(id, polygon)
                    added = True
            return added
        else:
            # either capacity not exceeded, or we're at MAX_DEPTH
            self.polygons[id] = polygon
            return True

    def match(self, point: Point) -> list[str]:
        """
        This method takes a point and finds the id of all polygons
        that it falls within that are within this node or its children.
        """

        results = []
        # 1) check bounding-box containment
        node_box = box(
            self.bbox.min_x, self.bbox.min_y, self.bbox.max_x, self.bbox.max_y
        )
        if not node_box.contains(point):
            return results

        # 2) If split, recurse to children.
        if self.is_split():
            for child in self.children:
                # Double-check child's bbox
                child_box = box(
                    child.bbox.min_x,
                    child.bbox.min_y,
                    child.bbox.max_x,
                    child.bbox.max_y,
                )
                if child_box.contains(point):
                    results.extend(child.match(point))
        else:
            # Unsplitted node: check all polygons it holds
            for pid, poly in self.polygons.items():
                if poly.contains(point):
                    results.append(pid)

        return results
