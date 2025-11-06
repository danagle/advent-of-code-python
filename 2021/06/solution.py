# Day 6: Lanternfish

from collections import Counter
from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[int]:
    """
    Read initial lanternfish timers from input file.
    Returns a list of integers representing each fish's timer.
    """
    return [int(x) for x in Path(filepath).read_text().strip().split(",")]


def simulate_fish_population(initial_timers: List[int], days: int) -> int:
    """
    Simulate lanternfish population growth for a given number of days.
    Returns total number of fish after the simulation.
    """
    # Use a counter to track number of fish at each timer value (0-8)
    timer_counts = Counter(initial_timers)

    for _ in range(days):
        new_counts: Counter[int] = Counter()
        for timer in range(9):
            if timer == 0:
                # Fish with timer 0 create new fish with timer 8
                new_counts[8] += timer_counts[0]
                # Existing fish reset to timer 6
                new_counts[6] += timer_counts[0]
            else:
                # Decrease timer for other fish
                new_counts[timer - 1] += timer_counts[timer]
        timer_counts = new_counts

    return sum(timer_counts.values())


if __name__ == "__main__":
    initial_timers = read_input_file()
    print(f"Part 1: {simulate_fish_population(initial_timers, 80)}")
    print(f"Part 2: {simulate_fish_population(initial_timers, 256)}")
