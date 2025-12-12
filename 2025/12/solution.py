"""
Advent of Code 2025
Day 12: Christmas Tree Farm
https://adventofcode.com/2025/day/12
"""
from math import prod
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """
    Load and parse the puzzle input.

    The file is expected to contain multiple shape blocks followed by a region
    description block, separated by a blank line.

    Shapes:
        - Each shape block is counted by the number of '#' characters it contains.

    Regions:
        - Each line has the form: "<dim_x>x<dim_y>...: <q1> <q2> <q3> ..."
        - The left side is multiplied together to get the area of the region.
        - The right side lists how many times each shape is allowed.

    Returns:
        tuple:
            - list[int]: number of units for each shape
            - list[tuple[int, list[int]]]: each region as (area, quantities)
    """
    content = Path(filepath).read_text(encoding="utf-8").strip()

    # All blocks before the final one are shapes; the last block describes regions.
    *shapes_str, regions_str = content.split("\n\n")

    # Each shape contributes units based on how many '#' characters it contains.
    shape_units = [s.count('#') for s in shapes_str]

    regions = []
    for region in regions_str.split('\n'):
        # Format: "widthxheight: q1 q2 q3 ..."
        dimensions_str, quantities_str = region.strip().split(": ")

        # Region area is the product of all dimensional values.
        area = prod(int(i) for i in dimensions_str.split('x'))

        # Convert the list of quantities into integers.
        quantities = [int(i) for i in quantities_str.split(' ')]

        regions.append((area, quantities))

    return shape_units, regions


def part_one(units, regions):
    """
    Count how many regions can accommodate the best-case usage of all shapes.

    The "best case" for a region is the sum of (shape_units[i] * quantity[i]).
    A region counts if its area is at least that total.

    Args:
        units (list[int]): unit counts for each shape.
        regions (list[tuple[int, list[int]]]): region definitions as (area, quantities).

    Returns:
        int: number of regions that meet or exceed their best-case requirement.
    """
    total = 0

    for area, quantities in regions:
        # Best-case usage is straightforward multiplication across shapes.
        best_case = sum(a * b for a, b in zip(units, quantities))
        if area >= best_case:
            total += 1

    return total


if __name__ == "__main__":
    shapes, regions = read_input_file()
    print("Part 1:", part_one(shapes, regions))
