"""
Advent of Code 2025
Day 3: Lobby
https://adventofcode.com/2025/day/3
"""
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """Parse list of battery banks from the input file."""
    return [b for b in Path(filepath).read_text(encoding="utf-8").strip().splitlines()]


def max_joltage_batteries(battery_bank, n):
    """
    Find the n largest batteries in the the battery bank.
    Greedily extracts the largest n digit number possible by keeping digits in order.
    """
    batteries_selected = []
    start = 0

    for i in range(n):
        # Last possible start so we have enough characters left to pick n total
        end = len(battery_bank) - (n - i) + 1

        # Pick the index of the maximum digit in battery_bank[start:end]
        best_index = max(range(start, end), key=lambda idx: battery_bank[idx])

        batteries_selected.append(battery_bank[best_index])
        start = best_index + 1

    return int("".join(batteries_selected))


def part_one(battery_banks, num_batteries=2):
    """Using exactly two batteries from each battery bank what is the total output joltage?"""
    print("Part 1:", sum(max_joltage_batteries(bank, num_batteries) for bank in battery_banks))


def part_two(battery_banks, num_batteries=12):
    """Using exactly twelve batteries from each battery bank what is the total output joltage?"""
    print("Part 2:", sum(max_joltage_batteries(bank, num_batteries) for bank in battery_banks))


if __name__ == "__main__":
    banks = read_input_file()
    part_one(banks)
    part_two(banks)
