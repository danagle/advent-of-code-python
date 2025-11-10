# Day 1: Calorie Counting

from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[List[int]]:
    """
    Reads the input file and returns a list of lists of integers,
    where each inner list represents the calorie counts for one elf.
    """
    raw = Path(filepath).read_text().strip().split("\n\n")
    return [list(map(int, block.splitlines())) for block in raw]


def total_calories_per_elf(groups: List[List[int]]) -> List[int]:
    """
    Computes the total calories carried by each elf.
    """
    return [sum(group) for group in groups]


def part_one(calories: List[int]) -> int:
    """
    Returns the maximum total calories carried by a single elf.
    """
    return max(calories)


def part_two(calories: List[int]) -> int:
    """
    Returns the sum of the top three calorie totals among all elves.
    """
    return sum(sorted(calories, reverse=True)[:3])


def main() -> None:
    groups = read_input_file()
    totals = total_calories_per_elf(groups)

    print("Part 1:", part_one(totals))
    print("Part 2:", part_two(totals))


if __name__ == "__main__":
    main()
