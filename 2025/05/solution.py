"""
Advent of Code 2025
Day 5: Cafeteria
https://adventofcode.com/2025/day/5
"""
from pathlib import Path

def parse_input_file(filepath="input.txt"):
    """Parses input file into a list of ranges and ingredient IDs."""
    ranges_text, ingredients_text = Path(filepath).read_text(encoding="utf-8").strip().split("\n\n")

    ranges = sorted([tuple(map(int, r.split('-'))) for r in ranges_text.splitlines()])
    ingredient_ids = sorted([int(i) for i in ingredients_text.splitlines()])

    return ranges, ingredient_ids


def part_one(ranges, ids):
    """Count how many ingredient ids are found within the list of ranges."""
    not_spoiled = 0

    for id in ids:
        for r in ranges:
            if r[0] <= id <= r[1]:
                not_spoiled += 1
                break

    return not_spoiled


def part_two(ranges):
    """Count the total number of ids in the overlapping ranges."""
    merged = []

    for start, end in ranges:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return sum(end - start + 1 for start, end in merged)


if __name__ == "__main__":
    fresh_ranges, ingredient_ids = parse_input_file()
    print("Part 1:", part_one(fresh_ranges, ingredient_ids))
    print("Part 2:", part_two(fresh_ranges))
