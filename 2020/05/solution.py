"""
Advent of Code 2020
Day 5: Binary Boarding
https://adventofcode.com/2020/day/5
"""

from pathlib import Path


def parse_boarding_pass(code: str) -> int:
    """
    Convert a boarding pass string (e.g. 'FBFBBFFRLR') into a seat ID.
    The first 7 characters determine the row (F=0, B=1).
    The last 3 characters determine the column (L=0, R=1).
    Seat ID = row * 8 + column.
    """
    # Translate boarding pass into binary representation
    binary = (
        code.strip()
        .replace("F", "0")
        .replace("B", "1")
        .replace("L", "0")
        .replace("R", "1")
    )
    row = int(binary[:7], 2)
    col = int(binary[7:], 2)
    return row * 8 + col


def load_boarding_passes(filename: str) -> list[int]:
    """Load boarding pass strings from the input file."""
    data = Path(filename).read_text().strip().splitlines()
    return [line.strip() for line in data if line.strip()]


def part_one() -> list[int]:
    """Find the highest seat ID."""
    seat_ids = [parse_boarding_pass(code) for code in load_boarding_passes("input.txt")]
    print(f"Part 1 answer: {max(seat_ids)}")
    return seat_ids


def part_two(seat_ids: list[int]):
    """Find your seat ID (the missing one that isn’t at the front or back)."""
    seat_ids.sort()
    for prev, curr in zip(seat_ids, seat_ids[1:]):
        if curr - prev == 2:
            print(f"Part 2 answer: {curr - 1}")
            break


if __name__ == "__main__":
    seat_ids = part_one()
    part_two(seat_ids)
