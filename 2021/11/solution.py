# Day 11: Dumbo Octopus

from pathlib import Path
from typing import List, Tuple


def read_input_file(filepath: str = "input.txt") -> List[List[int]]:
    """
    Read the octopus energy levels from input file as a 2D list of integers.
    """
    return [[int(c) for c in line] for line in Path(filepath).read_text().strip().splitlines()]


def get_neighbors(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int, int]]:
    """
    Return all neighbors (including diagonals) of a cell within bounds.
    """
    neighbors: List[Tuple[int, int]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and 0 <= nx < max_x and 0 <= ny < max_y:
                neighbors.append((nx, ny))
    return neighbors


def step(grid: List[List[int]]) -> int:
    """
    Perform one step of energy increase and flashing.
    Returns the number of flashes that occurred in this step.
    """
    max_x, max_y = len(grid), len(grid[0])
    flashed: List[List[bool]] = [[False] * max_y for _ in range(max_x)]

    # Increase all energy levels by 1
    for x in range(max_x):
        for y in range(max_y):
            grid[x][y] += 1

    # Process flashes
    flash_occurred = True
    while flash_occurred:
        flash_occurred = False
        for x in range(max_x):
            for y in range(max_y):
                if grid[x][y] > 9 and not flashed[x][y]:
                    flashed[x][y] = True
                    flash_occurred = True
                    for nx, ny in get_neighbors(x, y, max_x, max_y):
                        if not flashed[nx][ny]:
                            grid[nx][ny] += 1

    # Reset energy for flashed octopuses and count flashes
    flashes = 0
    for x in range(max_x):
        for y in range(max_y):
            if flashed[x][y]:
                grid[x][y] = 0
                flashes += 1
    return flashes


def part_one(grid: List[List[int]], steps: int = 100) -> int:
    """
    Return total flashes after given number of steps.
    """
    # Make a copy to avoid mutating the original grid
    grid_copy = [row[:] for row in grid]
    return sum(step(grid_copy) for _ in range(steps))


def part_two(grid: List[List[int]]) -> int:
    """
    Return the first step during which all octopuses flash simultaneously.
    """
    grid_copy = [row[:] for row in grid]
    step_count = 0
    total_octopuses = len(grid_copy) * len(grid_copy[0])
    while True:
        step_count += 1
        flashes = step(grid_copy)
        if flashes == total_octopuses:
            return step_count


if __name__ == "__main__":
    grid = read_input_file()
    print(f"Part 1: {part_one(grid)}")
    print(f"Part 2: {part_two(grid)}")
