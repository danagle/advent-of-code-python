# Day 7: The Treachery of Whales

from pathlib import Path
import statistics
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[int]:
    """
    Read initial horizontal positions of crabs from input file.
    Returns a list of integers.
    """
    return [int(x) for x in Path(filepath).read_text().strip().split(",")]


def fuel_cost_linear(positions: List[int], target: int) -> int:
    """
    Compute total fuel cost to move all crabs to `target` position
    with linear fuel cost (1 fuel per step).
    """
    return sum(abs(p - target) for p in positions)


def fuel_cost_incremental(positions: List[int], target: int) -> int:
    """
    Compute total fuel cost to move all crabs to `target` position
    with incremental fuel cost: 1 + 2 + ... + n = n*(n+1)//2 per distance n.
    """
    return sum((distance := abs(p - target)) * (distance + 1) // 2 for p in positions)


def part_one(positions: List[int]) -> int:
    """
    Solve Part 1: minimum fuel with linear cost.
    Optimal position is the median.
    """
    median_pos = int(statistics.median(positions))
    return fuel_cost_linear(positions, median_pos)


def part_two(positions: List[int]) -> int:
    """
    Solve Part 2: minimum fuel with incremental cost.
    Check both floor and ceil of the mean for minimum fuel.
    """
    mean_pos = sum(positions) / len(positions)
    floor_pos, ceil_pos = int(mean_pos), int(mean_pos) + 1
    return min(fuel_cost_incremental(positions, floor_pos),
               fuel_cost_incremental(positions, ceil_pos))


if __name__ == "__main__":
    positions = read_input_file()
    print(f"Part 1: {part_one(positions)}")
    print(f"Part 2: {part_two(positions)}")
