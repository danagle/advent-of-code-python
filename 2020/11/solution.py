"""
Advent of Code 2020
Day 11: Seating System
https://adventofcode.com/2020/day/11
"""
from itertools import product
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional


def read_input_file(filepath: str = "input.txt") -> np.ndarray:
    """
    Read the input file into a padded NumPy array.
    Padding with 0 (floor) around the grid makes neighbor logic simpler.
    """
    # map characters to integers for compact representation
    LOOKUP = {".": 0, "L": 1, "#": 2}

    text = Path(filepath).read_text().strip().replace("\r", "")
    grid = [[LOOKUP[c] for c in line] for line in text.splitlines()]

    padded = [[0] + row + [0] for row in grid]
    pad_row = [0] * len(padded[0])
    padded = [pad_row] + padded + [pad_row]
    return np.array(padded, dtype=np.uint8)


def create_visibility_mask(grid: np.ndarray) -> List[List[Tuple[Tuple[int, ...], Tuple[int, ...]]]]:
    """
    Precompute, for each seat, the coordinates (as tuple-of-rows, tuple-of-cols)
    of the first visible seat in each of the 8 directions (if any).
    Returns a 2D list mask such that mask[i][j] is (rows_tuple, cols_tuple)
    which can be used to index the grid: grid[rows_tuple, cols_tuple].
    """
    directions = [(dx, dy) for dx, dy in product([-1, 0, 1], repeat=2) if (dx, dy) != (0, 0)]
    rows, cols = grid.shape
    mask = [[[] for _ in range(cols)] for _ in range(rows)]

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            for dx, dy in directions:
                x, y = i + dx, j + dy
                # step until we find a non-floor seat or exit the interior
                while 0 < x < rows - 1 and 0 < y < cols - 1 and grid[x, y] == 0:
                    x += dx
                    y += dy
                if 0 < x < rows - 1 and 0 < y < cols - 1:
                    mask[i][j].append((x, y))

    # convert lists of (x,y) to tuple-of-rows, tuple-of-cols for fast numpy indexing
    converted = []
    for row in mask:
        conv_row = []
        for coords in row:
            if coords:
                rows_t, cols_t = tuple(zip(*coords))
                conv_row.append((rows_t, cols_t))
            else:
                conv_row.append(((), ()))
        converted.append(conv_row)
    return converted


def count_adjacent_neighbors(grid: np.ndarray, i: int, j: int) -> int:
    """
    Count occupied neighbors adjacent to (i,j), excluding the center seat itself.
    """
    region = grid[i - 1 : i + 2, j - 1 : j + 2]
    total_occupied = np.count_nonzero(region == 2)
    # exclude the center if it is occupied
    if grid[i, j] == 2:
        total_occupied -= 1
    return int(total_occupied)


def count_visible_neighbors(grid: np.ndarray, i: int, j: int, mask) -> int:
    """
    Count occupied seats visible from (i,j) using the precomputed mask.
    Mask entry is (rows_tuple, cols_tuple); indexing returns an array of values.
    """
    rows_t, cols_t = mask[i][j]
    if not rows_t:
        return 0
    visible = grid[rows_t, cols_t]
    return int(np.count_nonzero(visible == 2))


def simulate(
    grid: np.ndarray,
    neighbor_fn,
    mask: Optional[List[List[Tuple[Tuple[int, ...], Tuple[int, ...]]]]] = None,
    tolerance: int = 4,
) -> int:
    """
    Simulate seating until stable.
    neighbor_fn: function to count neighbors (adjacent or visible)
    mask: precomputed visibility mask (only needed for visible counting)
    tolerance: number of occupied neighbors (excluding center) that causes an occupied seat to become empty
               (4 for adjacent rules in part 1, 5 for visible rules in part 2)
    Returns the number of occupied seats at equilibrium.
    """
    grid = grid.copy()
    rows, cols = grid.shape
    changed = True

    while changed:
        changed = False
        prev = grid.copy()

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if prev[i, j] == 0:  # floor
                    continue

                if mask is None:
                    neighbors = neighbor_fn(prev, i, j)
                else:
                    neighbors = neighbor_fn(prev, i, j, mask)

                if prev[i, j] == 1 and neighbors == 0:
                    # empty seat with no occupied neighbors -> becomes occupied
                    grid[i, j] = 2
                    changed = True
                elif prev[i, j] == 2 and neighbors >= tolerance:
                    # occupied seat with too many neighbors -> becomes empty
                    grid[i, j] = 1
                    changed = True

    return int(np.count_nonzero(grid == 2))


def part_one(grid: np.ndarray) -> int:
    """Part 1: adjacent seats rule (occupied -> empty if 4+ adjacent occupied)."""
    return simulate(grid, neighbor_fn=count_adjacent_neighbors, mask=None, tolerance=4)


def part_two(grid: np.ndarray) -> int:
    """Part 2: visible seats rule (occupied -> empty if 5+ visible occupied)."""
    mask = create_visibility_mask(grid)
    return simulate(grid, neighbor_fn=count_visible_neighbors, mask=mask, tolerance=5)


if __name__ == "__main__":
    grid = read_input_file()
    p1 = part_one(grid)
    print("Part 1:", p1)
    p2 = part_two(grid)
    print("Part 2:", p2)
