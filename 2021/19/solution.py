# Day 19: Beacon Scanner

from itertools import combinations, product
import numpy as np
from pathlib import Path
from typing import List, Tuple, Set

Point = Tuple[int, int, int]


def read_input_file(filepath: str = "input.txt") -> List[List[Point]]:
    """
    Reads the input file and parses the scanner reports.
    Returns a list of scanners, each with a list of points (x, y, z).
    """
    raw = Path(filepath).read_text().strip().split("\n\n")
    scanners: List[List[Point]] = []
    for block in raw:
        lines = block.strip().splitlines()[1:]
        scanner_points = [tuple(map(int, line.split(','))) for line in lines]
        scanners.append(scanner_points)
    return scanners


def all_rotations() -> List[np.ndarray]:
    """
    Returns all 24 rotation matrices in 3D that preserve right-handed coordinate system.
    """
    rotations = []
    axes = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    for signs in product((1, -1), repeat=3):
        for perm in product((0, 1, 2), repeat=3):
            if len(set(perm)) != 3:
                continue
            matrix = np.zeros((3, 3), dtype=int)
            for i, p in enumerate(perm):
                matrix[i, p] = signs[i]
            if np.linalg.det(matrix) == 1:
                rotations.append(matrix)
    return rotations


def translate(points: List[Point], offset: Point) -> List[Point]:
    ox, oy, oz = offset
    return [(x + ox, y + oy, z + oz) for x, y, z in points]


def find_overlap(scanner_a: Set[Point], scanner_b: List[Point], rotations: List[np.ndarray]) -> Tuple[bool, List[Point], Point]:
    """
    Tries to find an overlap of at least 12 points between scanner_a and scanner_b.
    Returns (found, transformed points, translation offset)
    """
    for rot in rotations:
        rotated_b = [tuple(rot @ np.array(p)) for p in scanner_b]
        offsets_count = {}
        for pa in scanner_a:
            for pb in rotated_b:
                offset = (pa[0]-pb[0], pa[1]-pb[1], pa[2]-pb[2])
                offsets_count[offset] = offsets_count.get(offset, 0) + 1
                if offsets_count[offset] >= 12:
                    transformed_b = translate(rotated_b, offset)
                    return True, transformed_b, offset
    return False, [], (0, 0, 0)


def align_scanners(scanners: List[List[Point]]) -> Tuple[Set[Point], List[Point]]:
    """
    Aligns all scanners to the coordinate system of scanner 0.
    Returns the set of all beacons and positions of all scanners.
    """
    rotations = all_rotations()
    aligned: Set[Point] = set(scanners[0])
    remaining = scanners[1:]
    scanner_positions: List[Point] = [(0, 0, 0)]

    while remaining:
        for i, scanner in enumerate(remaining):
            found, transformed, pos = find_overlap(aligned, scanner, rotations)
            if found:
                aligned.update(transformed)
                scanner_positions.append(pos)
                remaining.pop(i)
                break

    return aligned, scanner_positions


def manhattan_distance(p1: Point, p2: Point) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))


def main() -> None:
    scanners = read_input_file()

    # Align all scanners
    beacons, scanner_positions = align_scanners(scanners)

    # Part 1: number of beacons
    print("Part 1:", len(beacons))

    # Part 2: largest Manhattan distance between any two scanners
    max_dist = max(manhattan_distance(a, b) for a, b in combinations(scanner_positions, 2))
    print("Part 2:", max_dist)


if __name__ == "__main__":
    main()
