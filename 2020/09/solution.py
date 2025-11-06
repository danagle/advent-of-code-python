"""
Advent of Code 2020
Day 9: Encoding Error
https://adventofcode.com/2020/day/9
"""
from pathlib import Path
from typing import List, Optional


def read_input(filepath: str = "input.txt") -> List[int]:
    """Read the input file and return a list of integers."""
    return [int(line) for line in Path(filepath).read_text().splitlines()]


def find_invalid_number(numbers: List[int], preamble: int = 25) -> Optional[int]:
    """
    Find the first number in the list (after the preamble)
    that is not the sum of two of the previous `preamble` numbers.
    """
    for i in range(preamble, len(numbers)):
        current = numbers[i]
        window = numbers[i - preamble : i]
        valid = any(
            (current - a in window and current - a != a)
            for a in window
        )

        if not valid:
            print("Part 1:", current)
            return current
    return None


def find_encryption_weakness(numbers: List[int], target: int) -> Optional[int]:
    """
    Find a contiguous set of numbers that sum to `target`.
    Return the sum of the smallest and largest number in that set.
    """
    for start in range(len(numbers)):
        total = 0
        smallest = float("inf")
        largest = float("-inf")

        for end in range(start, len(numbers)):
            value = numbers[end]
            total += value
            smallest = min(smallest, value)
            largest = max(largest, value)

            if total == target:
                print("Part 2:", smallest + largest)
                return smallest + largest
            if total > target:
                break

    return None


if __name__ == "__main__":
    numbers = read_input()
    invalid_number = find_invalid_number(numbers)
    if invalid_number is not None:
        find_encryption_weakness(numbers, invalid_number)
