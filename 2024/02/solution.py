# Advent of Code 2024 - Day 2: Red-Nosed Reports
# https://adventofcode.com/2024/day/2

def read_input(file_path):
    with open(file_path) as f:
        reports = [list(map(int, line.split())) for line in f]
    return reports


def is_sequence_safe(report):
    # Evaluates whether all adjacent pairs of elements in the list report 
    # satisfy two specific conditions.
    # Checks that the absolute difference between a and b is greater than 0
    # and less than 4.
    # The list has a consistent direction (all increasing or all decreasing).
    return all(0 < abs(b-a) < 4 and (b-a > 0) == (report[1] > report[0]) 
                    for a, b in zip(report, report[1:]))


def is_dampened_sequence_safe(report):
    if is_sequence_safe(report):
        return True
    for index, _ in enumerate(report):
        container = report[:]
        container.pop(index)
        if is_sequence_safe(container):
            return True
    return False


def part1(reports):
    return sum(is_sequence_safe(r) for r in reports)


def part2(reports):
    return sum(is_dampened_sequence_safe(r) for r in reports)


if __name__ == "__main__":
    input = read_input("input.txt")
    print("Part 1: ", part1(input))
    print("Part 2: ", part2(input))
