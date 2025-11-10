# Day 3: Rucksack Reorganization

from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[str]:
    """
    Reads the input file and returns a list of rucksack strings.
    Each line represents one rucksack.
    """
    return Path(filepath).read_text().strip().splitlines()


def priority(item: str) -> int:
    """
    Returns the priority of a given item (a-z → 1–26, A-Z → 27–52).
    """
    if "a" <= item <= "z":
        return ord(item) - ord("a") + 1
    return ord(item) - ord("A") + 27


def part_one(rucksacks: List[str]) -> int:
    """
    For each rucksack, finds the common item between the two compartments
    and sums their priorities.
    """
    total = 0
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        left, right = set(rucksack[:half]), set(rucksack[half:])
        common = left & right
        total += sum(priority(item) for item in common)
    return total


def part_two(rucksacks: List[str]) -> int:
    """
    Groups rucksacks into triples (elf groups) and finds the common badge item.
    Sums their priorities.
    """
    total = 0
    for i in range(0, len(rucksacks), 3):
        group = rucksacks[i : i + 3]
        common = set(group[0]) & set(group[1]) & set(group[2])
        total += sum(priority(item) for item in common)
    return total


if __name__ == "__main__":
    rucksacks = read_input_file()
    print("Part 1:", part_one(rucksacks))
    print("Part 2:", part_two(rucksacks))
