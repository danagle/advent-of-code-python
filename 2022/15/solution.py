# Day 15: Beacon Exclusion Zone

from pathlib import Path
import re
from typing import List, Tuple


def read_input_file(filepath: str = "input.txt") -> List[Tuple[complex, complex]]:
    """Parse input file into a list of (sensor, beacon) complex coordinate pairs."""
    pairs = []
    for line in Path(filepath).read_text().strip().splitlines():
        x1, y1, x2, y2 = map(int, re.findall(r"-?\d+", line))
        sensor = complex(x1, y1)
        beacon = complex(x2, y2)
        pairs.append((sensor, beacon))
    return pairs


def manhattan_distance(p1: complex, p2: complex) -> int:
    """Compute Manhattan distance between two complex coordinates."""
    return int(abs(p1.real - p2.real) + abs(p1.imag - p2.imag))


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Combine overlapping or contiguous ranges into non-overlapping ranges."""
    if not ranges:
        return []
    ranges.sort()
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        if start > last_end:
            merged.append((start, end))
        else:
            merged[-1] = (last_start, max(last_end, end))
    return merged


def part_one(sensor_beacon_pairs: List[Tuple[complex, complex]], target_y: int = 2_000_000) -> int:
    """Count positions on the target row that cannot contain a beacon."""
    blocked_ranges = []

    for sensor, beacon in sensor_beacon_pairs:
        distance = manhattan_distance(sensor, beacon)
        vertical_offset = abs(sensor.imag - target_y)
        if vertical_offset <= distance:
            horizontal_offset = distance - vertical_offset
            start = int(sensor.real - horizontal_offset)
            end = int(sensor.real + horizontal_offset)
            blocked_ranges.append((start, end))

    merged_ranges = merge_ranges(blocked_ranges)

    # Count all positions in merged ranges
    total_blocked = sum(end - start for start, end in merged_ranges)
    return total_blocked


def part_two(sensor_beacon_pairs: List[Tuple[complex, complex]], max_coord: int = 4_000_000) -> int:
    """Find the only possible gap for a beacon and compute its tuning frequency using complex arithmetic."""
    for y in range(max_coord + 1):
        blocked_ranges = []

        for sensor, beacon in sensor_beacon_pairs:
            distance = manhattan_distance(sensor, beacon)
            vertical_offset = abs(sensor.imag - y)
            if vertical_offset <= distance:
                horizontal_offset = distance - vertical_offset
                start = max(int(sensor.real - horizontal_offset), 0)
                end = min(int(sensor.real + horizontal_offset), max_coord)
                blocked_ranges.append((start, end))

        merged_ranges = merge_ranges(blocked_ranges)

        if len(merged_ranges) > 1 or merged_ranges[0][0] > 0 or merged_ranges[0][1] < max_coord:
            # There is a gap
            if len(merged_ranges) == 1:
                x = 0 if merged_ranges[0][0] > 0 else max_coord
            else:
                x = merged_ranges[0][1] + 1

            gap = complex(x, y)
            return int(gap.real * max_coord + gap.imag)


if __name__ == "__main__":
    sensor_beacon_pairs = read_input_file()
    print("Part 1:", part_one(sensor_beacon_pairs))
    print("Part 2:", part_two(sensor_beacon_pairs))
