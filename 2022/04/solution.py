# Day 4: Camp Cleanup

from pathlib import Path
from typing import List, Tuple


Assignment = Tuple[range, range]


def read_input_file(filepath: str = "input.txt") -> List[Assignment]:
    """
    Reads the input file and parses each line into a pair of ranges.
    Example line: "2-4,6-8" -> (range(2, 5), range(6, 9))
    """
    lines = Path(filepath).read_text().strip().splitlines()
    assignments: List[Assignment] = []
    for line in lines:
        left, right = line.split(",")
        a1, a2 = map(int, left.split("-"))
        b1, b2 = map(int, right.split("-"))
        assignments.append((range(a1, a2 + 1), range(b1, b2 + 1)))
    return assignments


def fully_contains(r1: range, r2: range) -> bool:
    """
    Returns True if one range fully contains the other.
    """
    return (r1.start <= r2.start and r1.stop >= r2.stop) or (
        r2.start <= r1.start and r2.stop >= r1.stop
    )


def overlaps(r1: range, r2: range) -> bool:
    """
    Returns True if the two ranges overlap at all.
    """
    return r1.start <= r2.stop - 1 and r2.start <= r1.stop - 1


def part_one(assignments: List[Assignment]) -> int:
    """
    Counts how many assignment pairs have one range fully containing the other.
    """
    return sum(fully_contains(a, b) for a, b in assignments)


def part_two(assignments: List[Assignment]) -> int:
    """
    Counts how many assignment pairs overlap in any way.
    """
    return sum(overlaps(a, b) for a, b in assignments)


if __name__ == "__main__":
    assignments = read_input_file()
    print("Part 1:", part_one(assignments))
    print("Part 2:", part_two(assignments))
