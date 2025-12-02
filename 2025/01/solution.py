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


def rotate_dial(rotations, dial=50):
    """
    Simulate the rotations while counting the number of instances that
    it passes zero or stops at the zero position.
    """
    stops_at_zero = passes_zero = 0

    for direction, distance in rotations:
        # Steps until you hit the wrap point (0 -> 99 when moving left) is 
        # (100 - dial) % 100
        # Add the distance and count how many full 100-step blocks occur.
        passes_zero += ((100 + direction * dial) % 100 + distance) // 100
        dial = (dial + direction * distance) % 100
        stops_at_zero += dial == 0

    return stops_at_zero, passes_zero


if __name__ == "__main__":
    instructions = read_input_file()
    p1, p2 = rotate_dial(instructions)
    print("Part 1:", p1)
    print("Part 2:", p2)
