"""
Advent of Code 2024
Day 11: Plutonian Pebbles
https://adventofcode.com/2024/day/11
"""
from collections import Counter


def parse_input(file_path):
    with open(file_path, "r") as f:
        stones = f.read().strip().split()
    return stones


def blink(stones):
    new_stones = Counter()
    for s, n in stones.items():
        if s == "0":
            # Rule 1:
            # If the stone is engraved with the number 0,
            # it is replaced by a stone engraved with the number 1.
            new_stones["1"] += n
        else:
            digits = len(s)
            if digits % 2 == 0:
                # Rule 2:
                # If the stone is engraved with a number that has an even number
                # of digits, it is replaced by two stones.
                # The left half of the digits are engraved on the new left stone,
                # and the right half of the digits are engraved on the new right stone.
                half = digits // 2
                left_part = str(int(s[:half]))
                right_part = str(int(s[half:]))
                new_stones[left_part] += n
                new_stones[right_part] += n
            else:
                # Rule3:
                # If none of the other rules apply, the stone is replaced by a new stone;
                # the old stone's number multiplied by 2024 is engraved on the new stone.
                val = int(s) * 2024
                new_stones[str(val)] += n
    return new_stones


def solve_day11(numbers):
    stones = Counter(numbers)

    # 75 blinks for both parts
    for i in range(75):
        stones = blink(stones)
        if i==25-1:
            # 25 blinks
            p1 = sum(stones.values())
        if i==75-1:
            # 75 blinks
            p2 = sum(stones.values())

    return p1, p2


if __name__ == "__main__":
    numbers = parse_input("input.txt")

    p1, p2 = solve_day11(numbers)

    print("Part 1:", p1)
    print("Part 2:", p2)
