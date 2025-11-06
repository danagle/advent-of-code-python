"""
Advent of Code 2020
Day 23: Crab Cups
https://adventofcode.com/2020/day/23
"""
from pathlib import Path
from typing import Dict, List


def read_input_file(filepath: str = "input.txt") -> List[int]:
    """Read the cup labels as a list of integers."""
    line = Path(filepath).read_text().strip()
    return [int(c) for c in line]


def play_cups(labels: List[int], moves: int, total_cups: int | None = None) -> Dict[int, int]:
    """
    Simulate the crab cups game efficiently using a dict as a linked list.
    Returns a mapping {cup_label -> next_cup_label}.
    """
    # Extend cup labels for Part 2
    if total_cups and total_cups > len(labels):
        labels = labels + list(range(max(labels) + 1, total_cups + 1))

    # Build linked list mapping
    next_cup: Dict[int, int] = {}
    for a, b in zip(labels, labels[1:]):
        next_cup[a] = b
    next_cup[labels[-1]] = labels[0]  # wrap around

    current = labels[0]
    max_label = max(labels)

    for _ in range(moves):
        # Pick up 3 cups
        pick1 = next_cup[current]
        pick2 = next_cup[pick1]
        pick3 = next_cup[pick2]
        picked = {pick1, pick2, pick3}

        # Remove picked cups from circle
        next_cup[current] = next_cup[pick3]

        # Select destination cup
        dest = current - 1 or max_label
        while dest in picked:
            dest = dest - 1 or max_label

        # Reinsert picked cups
        next_cup[pick3] = next_cup[dest]
        next_cup[dest] = pick1

        # Move to next current
        current = next_cup[current]

    return next_cup


def cups_after_one(next_cup: Dict[int, int]) -> str:
    """Return labels after cup 1 in order."""
    result: List[str] = []
    x = next_cup[1]
    while x != 1:
        result.append(str(x))
        x = next_cup[x]
    return "".join(result)


def part_one(labels: List[int]) -> str:
    next_cup = play_cups(labels, moves=100)
    return cups_after_one(next_cup)


def part_two(labels: List[int]) -> int:
    next_cup = play_cups(labels, moves=10_000_000, total_cups=1_000_000)
    first = next_cup[1]
    second = next_cup[first]
    return first * second


if __name__ == "__main__":
    labels = read_input_file()
    p1 = part_one(labels)
    print("Part 1:", p1)
    p2 = part_two(labels)
    print("Part 2:", p2)
