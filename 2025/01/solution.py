"""
Advent of Code 2025
Day 1: Secret Entrance
https://adventofcode.com/2025/day/1
"""
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """Parse list of rotations from the input file."""
    return [(1 if s[0] == 'R' else -1, int(s[1:]))
            for s in Path(filepath).read_text(encoding="utf-8").strip().splitlines()]


def part_one(rotations, dial=50):
    """The rotations stop at zero how many times?"""
    stops_at_zero = 0

    for direction, distance in rotations:
        dial = (dial + direction * distance) % 100
        stops_at_zero += dial == 0

    print("Part 1:", stops_at_zero)


def part_two(rotations, dial=50):
    """The rotations pass zero how many times?"""
    passes = 0

    for direction, distance in rotations:
        # Steps until you hit the wrap point (0 -> 99 when moving left) is 
        # (100 - dial) % 100
        # Add the distance and count how many full 100-step blocks occur.
        passes += ((100 + direction * dial) % 100 + distance) // 100
        dial = (dial + direction * distance) % 100

    print("Part 2:", passes)


if __name__ == "__main__":
    instructions = read_input_file()
    part_one(instructions)
    part_two(instructions)
