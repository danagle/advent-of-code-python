"""
Advent of Code 2020
Day 13: Shuttle Search
https://adventofcode.com/2020/day/13
"""
from pathlib import Path


def read_input_data(filepath: str = "input.txt"):
    """Read and parse the input file."""
    lines = Path(filepath).read_text().strip().splitlines()
    earliest_departure = int(lines[0])
    buses = [
        int(x) if x != "x" else None
        for x in lines[1].split(",")
    ]
    return earliest_departure, buses


def part_one(earliest: int, buses: list[int | None]) -> int:
    """Find the earliest bus you can take multiplied by the waiting time."""
    valid_buses = [b for b in buses if b is not None]
    wait_times = {b: b - (earliest % b) for b in valid_buses}
    best_bus = min(wait_times, key=wait_times.get)
    return best_bus * wait_times[best_bus]


def part_two(buses: list[int | None]) -> int:
    """
    Find the earliest timestamp such that:
        (t + offset) % bus_id == 0 for each bus.
    Chinese Remainder Theorem (CRT).
    """
    timestamp = 0
    step = 1

    for offset, bus_id in enumerate(buses):
        if bus_id is None:
            continue

        # Increment timestamp until the bus fits the required offset
        while (timestamp + offset) % bus_id != 0:
            timestamp += step

        # Once aligned, multiply step by bus_id to preserve all previous alignments
        step *= bus_id

    return timestamp


if __name__ == "__main__":
    earliest, buses = read_input_data()
    p1 = part_one(earliest, buses)
    print("Part 1:", p1)
    p2 = part_two(buses)
    print("Part 2:", p2)
