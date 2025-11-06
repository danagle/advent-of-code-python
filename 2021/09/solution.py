# Day 9: Smoke Basin

from functools import reduce
import operator
from pathlib import Path
from typing import List, Tuple, Set


def read_input_file(filepath: str = "input.txt") -> List[List[int]]:
    """
    Read heightmap from input file and return as 2D list of integers.
    """
    return [[int(c) for c in line] for line in Path(filepath).read_text().strip().splitlines()]


def get_neighbors(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int, int]]:
    """
    Return coordinates of orthogonal neighbors within bounds.
    """
    neighbors: List[Tuple[int, int]] = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < max_x - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < max_y - 1:
        neighbors.append((x, y + 1))
    return neighbors


def find_low_points(heightmap: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Find coordinates of low points: cells lower than all orthogonal neighbors.
    """
    low_points: List[Tuple[int, int]] = []
    max_x, max_y = len(heightmap), len(heightmap[0])
    for x in range(max_x):
        for y in range(max_y):
            value = heightmap[x][y]
            if all(value < heightmap[nx][ny] for nx, ny in get_neighbors(x, y, max_x, max_y)):
                low_points.append((x, y))
    return low_points


def part_one(heightmap: List[List[int]]) -> int:
    """
    Sum of risk levels of all low points (height + 1).
    """
    return sum(heightmap[x][y] + 1 for x, y in find_low_points(heightmap))


def flood_fill_basin(x: int, y: int, heightmap: List[List[int]], visited: Set[Tuple[int, int]]) -> int:
    """
    Recursively explore a basin using flood-fill algorithm.
    Returns the size of the basin.
    """
    max_x, max_y = len(heightmap), len(heightmap[0])
    stack: List[Tuple[int, int]] = [(x, y)]
    size = 0
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited or heightmap[cx][cy] == 9:
            continue
        visited.add((cx, cy))
        size += 1
        for nx, ny in get_neighbors(cx, cy, max_x, max_y):
            if (nx, ny) not in visited and heightmap[nx][ny] != 9:
                stack.append((nx, ny))

    return size


def part_two(heightmap: List[List[int]]) -> int:
    """
    Multiply the sizes of the three largest basins.
    """
    visited: Set[Tuple[int, int]] = set()
    basin_sizes: List[int] = [
        flood_fill_basin(x, y, heightmap, visited)
        for x, y in find_low_points(heightmap)
    ]
    three_largest = sorted(basin_sizes, reverse=True)[:3]

    return reduce(operator.mul, three_largest)


if __name__ == "__main__":
    heightmap = read_input_file()
    print(f"Part 1: {part_one(heightmap)}")
    print(f"Part 2: {part_two(heightmap)}")
