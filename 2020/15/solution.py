"""
Advent of Code 2020
Day 15: Rambunctious Recitation
https://adventofcode.com/2020/day/15
"""
from pathlib import Path
from typing import List


def read_input_data(filepath: str = "input.txt") -> List[int]:
    """Read the starting numbers from the input file."""
    text = Path(filepath).read_text().strip()
    return [int(x) for x in text.split(",")]


def play_memory_game(starting_numbers: List[int], limit: int) -> int:
    """
    Play the memory game until the 'limit'-th number is spoken.
    Uses a dictionary to store the last turn each number was seen.
    Efficient enough for 30 million iterations.
    """
    # Map number -> last turn it was spoken
    last_seen = {num: i + 1 for i, num in enumerate(starting_numbers[:-1])}
    current = starting_numbers[-1]

    for turn in range(len(starting_numbers), limit):
        last_turn = last_seen.get(current)
        last_seen[current] = turn
        current = 0 if last_turn is None else turn - last_turn

    return current


def part_one(numbers: List[int]) -> int:
    """Find the 2020th number spoken."""
    return play_memory_game(numbers, 2020)


def part_two(numbers: List[int]) -> int:
    """Find the 30,000,000th number spoken (efficiently)."""
    return play_memory_game(numbers, 30_000_000)


if __name__ == "__main__":
    numbers = read_input_data()
    p1 = part_one(numbers)
    print("Part 1:", p1)
    p2 = part_two(numbers)
    print("Part 2:", p2)
