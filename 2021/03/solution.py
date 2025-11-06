# Advent of Code 2021
# Day 3: Binary Diagnostic

from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[str]:
    """Read binary numbers from input file."""
    return Path(filepath).read_text().strip().splitlines()


def part_one(numbers: List[str]) -> int:
    """
    Compute the gamma rate and epsilon rate from binary numbers
    and return their product.
    """
    bit_length = len(numbers[0])
    gamma_bits = []

    for i in range(bit_length):
        count_ones = sum(1 for number in numbers if number[i] == '1')
        if count_ones > len(numbers) / 2:
            gamma_bits.append('1')
        else:
            gamma_bits.append('0')

    gamma = int("".join(gamma_bits), 2)
    epsilon = gamma ^ (2 ** bit_length - 1)  # bitwise complement within bit length

    return gamma * epsilon


def filter_numbers(numbers: List[str], criteria: str) -> int:
    """
    Filter numbers by oxygen ('most') or CO2 ('least') bit criteria.
    Returns the final number as integer.
    """
    filtered = numbers[:]
    bit_length = len(numbers[0])

    for i in range(bit_length):
        if len(filtered) == 1:
            break
        count_ones = sum(1 for number in filtered if number[i] == '1')
        count_zeroes = len(filtered) - count_ones

        if criteria == 'most':
            keep_bit = '1' if count_ones >= count_zeroes else '0'
        elif criteria == 'least':
            keep_bit = '0' if count_ones >= count_zeroes else '1'
        else:
            raise ValueError("criteria must be 'most' or 'least'")

        filtered = [number for number in filtered if number[i] == keep_bit]

    return int(filtered[0], 2)


def part_two(numbers: List[str]) -> int:
    """Compute oxygen generator rating * CO2 scrubber rating."""
    oxygen = filter_numbers(numbers, 'most')
    co2 = filter_numbers(numbers, 'least')
    return oxygen * co2


if __name__ == "__main__":
    numbers = read_input_file()
    print(f"Part 1: {part_one(numbers)}")
    print(f"Part 2: {part_two(numbers)}")
