"""
Advent of Code 2020
Day 6: Custom Customs
https://adventofcode.com/2020/day/6
"""
from pathlib import Path


def read_input_file(filename: str):
    """Read the input file and split it into groups of answers."""
    data = Path(filename).read_text().strip()
    return [group.split("\n") for group in data.split("\n\n")]


def count_any_yes(group: list[str]) -> int:
    """
    Count how many unique questions anyone in the group answered 'yes' to.
    Equivalent to the union of all group members' answers.
    """
    return len(set("".join(group)))


def count_all_yes(group: list[str]) -> int:
    """
    Count how many questions everyone in the group answered 'yes' to.
    Equivalent to the intersection of all group members' answers.
    """
    common_answers = set(group[0])
    for person in group[1:]:
        common_answers &= set(person)
    return len(common_answers)


def part_one(groups):
    """Sum of questions where anyone answered 'yes'."""
    return sum(count_any_yes(g) for g in groups)


def part_two(groups):
    """Sum of questions where everyone answered 'yes'."""
    return sum(count_all_yes(g) for g in groups)


if __name__ == "__main__":
    text = read_input_file("input.txt")
    print(part_one(text))
    print(part_two(text))
