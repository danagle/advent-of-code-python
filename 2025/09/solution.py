"""
Advent of Code 2025
Day 9: Movie Theater
https://adventofcode.com/2025/day/9
"""
from itertools import combinations, pairwise
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """Creates a list of tuples (x, y) from the input text file."""
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    return [tuple(map(int, line.strip().split(','))) for line in lines]


def rect_area_and_box(p, q):
    """Compute the normalized bounding box and its area."""
    x1, y1 = p
    x2, y2 = q

    # Normalize so x1 <= x2, y1 <= y2
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1

    area = (x2 - x1 + 1) * (y2 - y1 + 1)

    return area, (x1, y1, x2, y2)


def bounding_box_overlaps(rect, segbox):
    """Check if bounding boxes overlap."""
    rx1, ry1, rx2, ry2 = rect
    sx1, sy1, sx2, sy2 = segbox
    return (rx1 < sx2 and rx2 > sx1 and ry1 < sy2 and ry2 > sy1)


def part_one_and_two(points):
    """
    part1 = largest area among all rectangles formed by any 2 points
    part2 = largest area among those rectangles that do NOT overlap
            ANY segment bounding box.
    """
    part1 = part2 = 0

    # Precompute all polygon edges as bounding boxes.
    edges = []
    for (x1, y1), (x2, y2) in pairwise(points + [points[0]]):
        # Normalize segment bounding box
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        edges.append((x1, y1, x2, y2))

    # For every pair of points, compute its rectangle.
    for p, q in combinations(points, 2):
        area, rect = rect_area_and_box(p, q)

        # Update largest rectangle
        part1 = max(part1, area)

        # Check whether the rectangle overlaps ANY edge bounding box.
        # If it does, skip it for Part 2.
        for segment_box in edges:
            if bounding_box_overlaps(rect, segment_box):
                break
        else:
            # If there's no break, this rectangle avoided every bounding box.
            part2 = max(part2, area)

    return part1, part2


if __name__ == "__main__":
    coordinates = read_input_file()
    p1, p2 = part_one_and_two(coordinates)
    print("Part 1:", p1)
    print("Part 2:", p2)
