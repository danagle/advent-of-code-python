# Day 25: Sea Cucumber

from pathlib import Path
from typing import List, Set, Tuple


def read_input_file(filepath: str = "input.txt") -> List[str]:
    """
    Read the input file and return the grid as a list of strings.
    """
    return Path(filepath).read_text().strip().splitlines()


def part_one(grid: List[str]) -> int:
    """
    Simulate the sea cucumber movement until no cucumbers can move.
    Returns the number of steps until the first standstill.
    """
    east_cucumbers: Set[Tuple[int, int]] = set()
    south_cucumbers: Set[Tuple[int, int]] = set()
    max_y, max_x = len(grid), len(grid[0])

    # Initialize positions of east and south-moving cucumbers
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == ">":
                east_cucumbers.add((x, y))
            elif char == "v":
                south_cucumbers.add((x, y))

    steps = 0
    while True:
        # Move east-facing cucumbers
        new_east: Set[Tuple[int, int]] = set()
        for x, y in east_cucumbers:
            next_pos = ((x + 1) % max_x, y)
            if next_pos not in east_cucumbers and next_pos not in south_cucumbers:
                new_east.add(next_pos)
            else:
                new_east.add((x, y))

        # Move south-facing cucumbers
        new_south: Set[Tuple[int, int]] = set()
        for x, y in south_cucumbers:
            next_pos = (x, (y + 1) % max_y)
            if next_pos not in south_cucumbers and next_pos not in new_east:
                new_south.add(next_pos)
            else:
                new_south.add((x, y))

        steps += 1

        # If no cucumbers moved, stop
        if new_east == east_cucumbers and new_south == south_cucumbers:
            break

        east_cucumbers, south_cucumbers = new_east, new_south

    return steps


if __name__ == "__main__":
    grid_data = read_input_file()
    result = part_one(grid_data)
    print("Part 1:", result)
