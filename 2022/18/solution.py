# Day 18: Boiling Boulders

from collections import deque
from pathlib import Path
import re
from typing import Set, Tuple

# 6 directions in 3D space (adjacent cubes)
ADJACENT = ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1))

Coordinate = Tuple[int, int, int]

def parse_line(line: str) -> Coordinate:
    """Extract integers from a line as a 3D coordinate."""
    return tuple(int(x) for x in re.findall(r"-?\d+", line))


def load_cubes(filepath: str = "input.txt") -> Set[Coordinate]:
    """Load occupied cubes from input file."""
    return {parse_line(line) for line in Path(filepath).read_text().strip().splitlines()}


def count_exposed_sides(cubes: Set[Coordinate]) -> int:
    """Count sides of cubes not touching other cubes."""
    exposed_sides = 0
    for x, y, z in cubes:
        for dx, dy, dz in ADJACENT:
            if (x + dx, y + dy, z + dz) not in cubes:
                exposed_sides += 1
    return exposed_sides


def flood_fill_external_air(cubes: Set[Coordinate]) -> Set[Coordinate]:
    """Mark all external air cubes using BFS flood-fill."""
    min_coord = min(min(c[i] for c in cubes) for i in range(3)) - 1
    max_coord = max(max(c[i] for c in cubes) for i in range(3)) + 2

    external_air: Set[Coordinate] = set()
    queue = deque([(min_coord, min_coord, min_coord)])

    while queue:
        x, y, z = queue.popleft()
        if (x, y, z) in cubes or (x, y, z) in external_air:
            continue
        if not (min_coord <= x < max_coord and min_coord <= y < max_coord and min_coord <= z < max_coord):
            continue
        external_air.add((x, y, z))
        for dx, dy, dz in ADJACENT:
            queue.append((x + dx, y + dy, z + dz))

    return external_air


def count_exposed_to_external_air(cubes: Set[Coordinate], external_air: Set[Coordinate]) -> int:
    """Count cube sides that touch external air."""
    exposed_sides = 0
    for x, y, z in cubes:
        for dx, dy, dz in ADJACENT:
            if (x + dx, y + dy, z + dz) in external_air:
                exposed_sides += 1
    return exposed_sides


if __name__ == "__main__":
    cubes = load_cubes()
    part1 = count_exposed_sides(cubes)
    external_air = flood_fill_external_air(cubes)
    part2 = count_exposed_to_external_air(cubes, external_air)

    print("Part 1:", part1)
    print("Part 2:", part2)
