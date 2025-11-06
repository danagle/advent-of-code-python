"""
Advent of Code 2020
Day 3: Toboggan Trajectory
https://adventofcode.com/2020/day/3
"""

import numpy as np
from pathlib import Path

# Global variable holding the terrain grid
TREE_MAP = None


def read_input_file():
    """Read the input file and convert it to a 2D NumPy array of 1s (trees) and 0s (open spaces)."""
    with open("input.txt", "r") as f:
        lines = f.read().replace("\r", "").splitlines()

    grid = [[1 if char == "#" else 0 for char in line] for line in lines]
    return np.array(grid, dtype=np.uint32)


def get_cell(x, y):
    """Return the value at (x, y), wrapping horizontally."""
    return TREE_MAP[y, x % TREE_MAP.shape[1]]


def count_trees_on_slope(right, down):
    """Count how many trees are encountered when moving through the grid with the given slope."""
    global TREE_MAP
    TREE_MAP = read_input_file()

    position = np.array([0, 0], dtype=np.int64)
    movement = np.array([right, down], dtype=np.int64)

    tree_count = 0
    while True:
        position += movement
        if position[1] >= TREE_MAP.shape[0]:
            # Stop when you move beyond the bottom
            break
        tree_count += get_cell(*position)

    return tree_count


def part_one():
    """Single slope: right 3, down 1."""
    return count_trees_on_slope(3, 1)


def part_two():
    """Multiple slopes; multiply the tree counts for all."""
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    results = [count_trees_on_slope(r, d) for r, d in slopes]
    return np.prod(results)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
