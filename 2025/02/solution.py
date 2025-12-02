"""
Advent of Code 2025
Day 2: Gift Shop
https://adventofcode.com/2025/day/2
"""
from pathlib import Path

def read_input_file(filepath="input.txt"):
    """Returns list of (min, max) string tuples from input file."""
    ranges = Path(filepath).read_text(encoding="utf-8").strip().split(',')
    return [tuple(r.split('-')) for r in ranges]


def generate_repeated_number(i, base, repeats):
    """
    Build a number by repeating `i` (represented as a base `10**sub_len`)
    `repeats` times mathematically, without string operations.
    """
    # (base**repeats - 1) // (base - 1) produces 111... (repeats times)
    return i * ((base**repeats - 1) // (base - 1))


def total_invalid_ids(ranges):
    """Sums all the invalid IDs in the given ranges."""
    part1 = set()
    part2 = set()

    for min_str, max_str in ranges:
        minimum = int(min_str)
        maximum = int(max_str)

        # Pre-calc length boundaries
        len_min = len(min_str)
        len_max = len(max_str)

        for total_len in range(len_min, len_max + 1):

            # Try every divisor for repeat count
            for repeats in range(2, total_len + 1):

                # Must divide evenly
                if total_len % repeats != 0:
                    continue

                sub_len = total_len // repeats
                base = 10 ** sub_len

                # Lower bound for sub-number (avoid leading zeros and stay inside range)
                sub_lower = max(minimum // (base ** (repeats - 1)), base // 10)

                for i in range(sub_lower, base):
                    num = generate_repeated_number(i, base, repeats)

                    if num > maximum:
                        break
                    if num < minimum:
                        continue

                    if repeats == 2:
                        part1.add(num)
                    part2.add(num)

    return sum(part1), sum(part2)


if __name__ == "__main__":
    given = read_input_file()
    p1, p2 = total_invalid_ids(given)
    print("Part 1:", p1)
    print("Part 2:", p2)
