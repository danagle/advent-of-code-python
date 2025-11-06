"""
Advent of Code 2020
Day 10: Adapter Array
https://adventofcode.com/2020/day/10
"""
from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[int]:
    """Read adapter joltages from the input file."""
    return [int(line) for line in Path(filepath).read_text().splitlines()]


def count_joltage_differences(adapters: List[int]) -> int:
    """
    Count the number of 1-jolt and 3-jolt differences between
    consecutive adapters, then return their product.
    """
    adapters = sorted(adapters)
    adapters = [0] + adapters + [max(adapters) + 3]  # add outlet (0) and device (+3)

    diffs = [adapters[i] - adapters[i - 1] for i in range(1, len(adapters))]
    ones = diffs.count(1)
    threes = diffs.count(3)

    return ones * threes


def count_arrangements(adapters: List[int]) -> int:
    """
    Count the total number of distinct ways to arrange adapters
    while satisfying the 1–3 joltage difference rule.
    """
    adapters = sorted(adapters)
    adapters = [0] + adapters + [max(adapters) + 3]

    ways = [0] * len(adapters)
    ways[0] = 1  # base case: one way to start at outlet (0)

    for i in range(1, len(adapters)):
        for j in range(i):
            if adapters[i] - adapters[j] <= 3:
                ways[i] += ways[j]

    return ways[-1]


if __name__ == "__main__":
    adapters = read_input_file()
    p1 = count_joltage_differences(adapters)
    print("Part 1:", p1)
    p2 = count_arrangements(adapters)
    print("Part 2:", p2)

