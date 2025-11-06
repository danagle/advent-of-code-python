"""
Advent of Code 2020
Day 25: Combo Breaker
https://adventofcode.com/2020/day/25
"""
from pathlib import Path


MODULO = 20201227
SUBJECT_NUMBER = 7


def read_input_file(filepath: str = "input.txt") -> tuple[int, int]:
    """Read the public keys of the card and door."""
    lines = Path(filepath).read_text().strip().splitlines()
    card_key, door_key = map(int, lines)
    return card_key, door_key


def find_loop_size(public_key: int, subject_number: int = SUBJECT_NUMBER, modulo: int = MODULO) -> int:
    """
    Determine the loop size for a given public key by repeated modular multiplication.
    (Equivalent to solving for the discrete log base `subject_number`.)
    """
    value = 1
    loop_size = 0
    while value != public_key:
        value = (value * subject_number) % modulo
        loop_size += 1
    return loop_size


def transform(subject_number: int, loop_size: int, modulo: int = MODULO) -> int:
    """Perform the transformation given a subject number and loop size."""
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % modulo
    return value


def part_one(card_key: int, door_key: int) -> int:
    """Compute the shared encryption key."""
    card_loop = find_loop_size(card_key)
    encryption_key = transform(door_key, card_loop)
    return encryption_key


if __name__ == "__main__":
    card_key, door_key = read_input_file()
    p1 = part_one(card_key, door_key)
    print("Part 1:", p1)
