"""
Advent of Code 2025
Day 9: Movie Theater
https://adventofcode.com/2025/day/9
"""
from itertools import combinations
from pathlib import Path

# Type aliases for clarity
# Coord: (x, y) - 2D point with integer coordinates
Coord = tuple[int, int]

# Edge: (fixed_coord, range_start, range_end)
# For vertical edges: (x, min_y, max_y)
# For horizontal edges: (y, min_x, max_x)
Edge = tuple[int, int, int]


def find_max_bounding_box_area(coords):
    """
    Compute the maximum area of any axis-aligned bounding box formed by
    selecting two points from the input coordinates.
    """
    max_area = 0
    
    # Test all pairs of points
    for point_a, point_b in combinations(coords, 2):
        # Calculate bounding box area (adding 1 to include both boundary points)
        width = abs(point_a[0] - point_b[0] + 1)
        height = abs(point_a[1] - point_b[1] + 1)
        area = width * height
        
        max_area = max(max_area, area)
    
    return max_area


def remove_collinear_points(coords):
    """
    Filter out redundant corners where three consecutive points form a straight
    line (either horizontal or vertical). This simplifies the polygon by keeping
    only the true corners.
    """
    n = len(coords)
    if n <= 2:
        return coords.copy()
    
    corners = []
    
    for i in range(n):
        prev_point = coords[(i - 1 + n) % n]
        curr_point = coords[i]
        next_point = coords[(i + 1) % n]
        
        # Check if three consecutive points are collinear
        is_vertical_line = (prev_point[0] == curr_point[0] == next_point[0])
        is_horizontal_line = (prev_point[1] == curr_point[1] == next_point[1])
        
        # Keep the point only if it's a true corner (not collinear)
        if not (is_vertical_line or is_horizontal_line):
            corners.append(curr_point)
    
    return corners


def separate_polygon_edges(polygon):
    """
    Classify polygon edges into vertical and horizontal segments for efficient
    intersection testing.
    """
    vertical_edges = []
    horizontal_edges = []
    
    # Iterate through consecutive pairs of vertices
    for i in range(len(polygon) - 1):
        vertex1 = polygon[i]
        vertex2 = polygon[i + 1]
        
        if vertex1[0] == vertex2[0]:
            # Vertical edge: x is fixed, y varies
            vertical_edges.append((
                vertex1[0],
                min(vertex1[1], vertex2[1]),
                max(vertex1[1], vertex2[1])
            ))
        else:
            # Horizontal edge: y is fixed, x varies
            horizontal_edges.append((
                vertex1[1],
                min(vertex1[0], vertex2[0]),
                max(vertex1[0], vertex2[0])
            ))
    
    return vertical_edges, horizontal_edges


def rectangle_intersects_polygon_interior(
    rect_min_x: int,
    rect_max_x: int,
    rect_min_y: int,
    rect_max_y: int,
    vertical_edges: list[Edge],
    horizontal_edges: list[Edge],
) -> bool:
    """
    Check if a rectangle's interior is crossed by any polygon edges.
    
    Edges touching the rectangle boundary are allowed; only interior
    crossings invalidate the rectangle.
    """
    # Check vertical edges crossing through the rectangle's interior
    for edge in vertical_edges:
        edge_x, edge_y_start, edge_y_end = edge
        
        # Edge must be strictly between left and right bounds (not on boundary)
        if rect_min_x < edge_x < rect_max_x:
            # Check if edge's y-range overlaps with rectangle's y-range
            overlap_start = max(edge_y_start, rect_min_y)
            overlap_end = min(edge_y_end, rect_max_y)
            
            if overlap_start < overlap_end:
                return True
    
    # Check horizontal edges crossing through the rectangle's interior
    for edge in horizontal_edges:
        edge_y, edge_x_start, edge_x_end = edge
        
        # Edge must be strictly between bottom and top bounds (not on boundary)
        if rect_min_y < edge_y < rect_max_y:
            # Check if edge's x-range overlaps with rectangle's x-range
            overlap_start = max(edge_x_start, rect_min_x)
            overlap_end = min(edge_x_end, rect_max_x)
            
            if overlap_start < overlap_end:
                return True
    
    return False


def point_inside_polygon(test_x: float, test_y: float, polygon: list[Coord]) -> bool:
    """
    Use the ray casting algorithm to determine if a point lies inside a polygon.
    
    Works by casting a ray from the test point to infinity and counting edge
    crossings: odd number of crossings = inside, even = outside.
    """
    inside = False
    
    # Test ray intersection with each polygon edge
    for i in range(len(polygon) - 1):
        vertex1 = polygon[i]
        vertex2 = polygon[i + 1]
        x1, y1 = float(vertex1[0]), float(vertex1[1])
        x2, y2 = float(vertex2[0]), float(vertex2[1])
        
        # Check if horizontal ray from test point crosses this edge
        if (y1 > test_y) != (y2 > test_y):
            # Calculate x-coordinate where ray intersects the edge
            intersection_x = (x2 - x1) * (test_y - y1) / (y2 - y1) + x1
            
            # If intersection is to the right of test point, toggle inside/outside
            if test_x < intersection_x:
                inside = not inside
    
    return inside


def find_max_interior_rectangle(coords: list[Coord]) -> int:
    """
    Find the largest axis-aligned rectangle that fits completely inside the
    given polygon. Uses exhaustive search with pruning optimizations.
    """
    # Simplify polygon by removing collinear points
    corners = remove_collinear_points(coords)
    
    # Create closed polygon by appending first corner to end
    polygon = corners + [corners[0]]
    
    # Classify edges for efficient intersection testing
    vertical_edges, horizontal_edges = separate_polygon_edges(polygon)
    
    max_area = 0
    
    # Test all pairs of corners as potential rectangle diagonals
    for corner_a, corner_b in combinations(corners, 2):
        # Compute axis-aligned bounding box
        rect_min_x = min(corner_a[0], corner_b[0])
        rect_max_x = max(corner_a[0], corner_b[0])
        rect_min_y = min(corner_a[1], corner_b[1])
        rect_max_y = max(corner_a[1], corner_b[1])
        
        width = rect_max_x - rect_min_x + 1
        height = rect_max_y - rect_min_y + 1
        area = width * height
        
        # Pruning: skip if this rectangle can't beat current maximum
        if area <= max_area:
            continue
        
        # Ensure no polygon edges cross through rectangle interior
        if rectangle_intersects_polygon_interior(
            rect_min_x, rect_max_x, rect_min_y, rect_max_y,
            vertical_edges, horizontal_edges
        ):
            continue
        
        # Ensure rectangle center is inside the polygon
        # Using center point with 0.5 offset to avoid edge cases
        center_x = rect_min_x + 0.5
        center_y = rect_min_y + 0.5
        if not point_inside_polygon(center_x, center_y, polygon):
            continue
        
        # This rectangle is valid and larger than previous maximum
        max_area = area
    
    return max_area


def read_input_file(filepath="input.txt"):
    """Creates a list of tuples (x, y) from the input text file."""
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    return [tuple(map(int, line.strip().split(','))) for line in lines]


if __name__ == "__main__":
    coordinates = read_input_file()
    
    print("Part 1:", find_max_bounding_box_area(coordinates))
    print("Part 2:", find_max_interior_rectangle(coordinates))
