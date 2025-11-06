"""
Advent of Code 2020
Day 17: Conway Cubes
https://adventofcode.com/2020/day/17
"""
from itertools import product
from pathlib import Path
from typing import Set, Tuple

Point = Tuple[int, ...]  # n-dimensional point

def read_input_file(filepath: str = "input.txt") -> Set[Tuple[int, int]]:
    """Read the 2D input and return a set of active (x, y) coordinates."""
    lines = Path(filepath).read_text().strip().splitlines()
    return {(x, y) for y, row in enumerate(lines) for x, ch in enumerate(row) if ch == "#"}


def make_initial_active(active2d: Set[Tuple[int, int]], dimensions: int) -> Set[Point]:
    """
    Convert the 2D active coordinates into N-dimensional coordinates.
    For dimensions==3 -> (x, y, 0)
    For dimensions==4 -> (x, y, 0, 0)
    """
    padding = (0,) * (dimensions - 2)
    return { (x, y) + padding for (x, y) in active2d }


def get_neighbors(point: Point) -> Set[Point]:
    """Return all neighbor coordinates of `point` (excluding the point itself)."""
    dims = len(point)
    deltas = list(product((-1, 0, 1), repeat=dims))
    deltas.remove((0,) * dims)
    return { tuple(p + d for p, d in zip(point, delta)) for delta in deltas }


def step(active: Set[Point]) -> Set[Point]:
    """
    Perform one cycle: count neighbors for all relevant positions and apply rules.
    Works for any dimensionality as long as `active` contains tuples of equal length.
    """
    neighbor_counts: dict[Point, int] = {}
    for p in active:
        for n in get_neighbors(p):
            neighbor_counts[n] = neighbor_counts.get(n, 0) + 1

    new_active: Set[Point] = set()
    for pos, cnt in neighbor_counts.items():
        if pos in active and cnt in (2, 3):
            new_active.add(pos)
        elif pos not in active and cnt == 3:
            new_active.add(pos)
    return new_active


def run_cycles(initial_active: Set[Point], cycles: int) -> Set[Point]:
    """Simulate the given number of cycles."""
    active = set(initial_active)
    for _ in range(cycles):
        active = step(active)
    return active


def part_one(active2d: Set[Tuple[int, int]]) -> int:
    """Solve Part 1: 3D Conway Cubes."""
    initial_3d = make_initial_active(active2d, dimensions=3)
    final = run_cycles(initial_3d, cycles=6)
    return len(final)


def part_two(active2d: Set[Tuple[int, int]]) -> int:
    """Solve Part 2: 4D Conway Cubes."""
    initial_4d = make_initial_active(active2d, dimensions=4)
    final = run_cycles(initial_4d, cycles=6)
    return len(final)


if __name__ == "__main__":
    initial_active = read_input_file()
    p1 = part_one(initial_active)
    print("Part 1:", p1)
    p2 = part_two(initial_active)
    print("Part 2:", p2)
