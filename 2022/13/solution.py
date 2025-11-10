# Day 13: Distress Signal
import json
from functools import cmp_to_key
from itertools import chain
from pathlib import Path
from typing import Any, List


def read_input_file(filepath: str = "input.txt") -> List[List[str]]:
    """Return packet pairs."""
    text = Path(filepath).read_text().strip()
    return [pair.splitlines() for pair in text.split("\n\n")]


def compare_packets(left: Any, right: Any) -> int:
    """
    Compare two packet structures recursively.
    Returns:
        -1 → left < right
         0 → equal
         1 → left > right
    """
    for i in range(min(len(left), len(right))):
        a, b = left[i], right[i]

        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                return -1
            elif a > b:
                return 1
            continue

        # Normalize to lists for recursive comparison
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]

        result = compare_packets(a, b)
        if result != 0:
            return result

    # If equal so far, shorter list is "smaller"
    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1
    return 0


def part_one(pairs: List[List[str]]) -> int:
    """Sum indices of correctly ordered packet pairs."""
    total = 0
    for idx, (a_str, b_str) in enumerate(pairs, start=1):
        left, right = json.loads(a_str), json.loads(b_str)
        if compare_packets(left, right) == -1:
            total += idx
    return total


def part_two(pairs: List[List[str]]) -> int:
    """Find the product of decoder key positions for divider packets."""
    packets = [
        json.loads(line)
        for line in chain.from_iterable(pairs)
    ]
    # Additional divider packets
    divider_1, divider_2  = [[2]], [[6]]

    packets.extend([divider_1, divider_2])

    # Sort packets using the custom comparator
    packets.sort(key=cmp_to_key(compare_packets))

    # Find 1-based indices of divider packets
    idx_1 = packets.index(divider_1) + 1
    idx_2 = packets.index(divider_2) + 1

    return idx_1 * idx_2


if __name__ == "__main__":
    packet_pairs = read_input_file()
    print("Part 1:", part_one(packet_pairs))
    print("Part 2:", part_two(packet_pairs))
