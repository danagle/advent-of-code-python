# Advent of Code 2024 - Day 1: Historian Hysteria
# https://adventofcode.com/2024/day/1

from collections import Counter

def read_input(file_path):
    with open(file_path) as f:
        left, right = zip(*(map(int, line.split()) for line in f))
    return sorted(left), sorted(right)


def part1(a, b):
    return sum(abs(num_a - num_b) for num_a, num_b in zip(sorted(a), sorted(b)))


def part2(a, b):
    b_counter = Counter(b)
    return sum(num_a * b_counter.get(num_a, 0) for num_a in a)


if __name__ == "__main__":
    list_A, list_B = read_input("input.txt")
    print("Part 1: ", part1(list_A, list_B))
    print("Part 2: ", part2(list_A, list_B))
