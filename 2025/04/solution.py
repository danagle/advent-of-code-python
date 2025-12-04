"""
Advent of Code 2025
Day 4: Printing Department
https://adventofcode.com/2025/day/4
"""
from pathlib import Path

NEIGHBOURS = [
    (-1, -1), (-1, 0), (-1, 1), (0, 1),
    (1, 1), (1, 0), (1, -1), (0, -1)
]


def read_input_file(filepath="input.txt"):
    """Reads a 2D grid from the input file."""
    rows = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    return [list(row) for row in rows]


def rolls_to_remove(grid):
    """Get rolls of paper that can be removed by a forklift."""
    height = len(grid)
    width = len(grid[0])
    remove = []

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != '@':
                continue
            num_rolls = 0
            for dr, dc in NEIGHBOURS:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < height and 0 <= nc < width:
                    num_rolls += grid[nr][nc] == '@'
            if num_rolls < 4:
                remove.append((r, c))

    return remove


def optimize_rolls(grid):
    """Remove rolls of paper that are accessible by a forklift."""
    rolls_removed = 0  # How many rolls of paper in total can be removed

    while True:
        to_remove = rolls_to_remove(grid)
        if rolls_removed == 0:
            # How many rolls of paper can be accessed by a forklift
            part1 = len(to_remove) 
        if len(to_remove) > 0:
            rolls_removed += len(to_remove)
            for r, c in to_remove:
                grid[r][c] = '.'
        else:
            break

    return part1, rolls_removed


if __name__ == "__main__":
    diagram = read_input_file()
    p1, p2 = optimize_rolls(diagram)
    print("Part 1:", p1)
    print("Part 2:", p2)
