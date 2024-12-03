"""
Advent of Code 2020
Day 2: Password Philosophy
https://adventofcode.com/2020/day/2
"""

def read_input_file(filename):
    with open(filename, "r") as f:
        return f.read().strip().splitlines()


def part_one(input_file):
    total = 0
    for line in input_file:
        range_part, char_part, password = line.split()
        a, b = map(int, range_part.split("-"))
        ch = char_part[0]
        count = password.count(ch)
        if a <= count <= b:
            total += 1
    return total


def part_two(input_file):
    total = 0
    for line in input_file:
        range_part, password = line.split(":")
        ch = range_part[-1]
        a, b = map(int, range_part[:-2].split("-"))
        if (password[a] == ch) != (password[b] == ch):
            total += 1
    return total


if __name__ == "__main__":
    text = read_input_file("input.txt")
    print(part_one(text))
    print(part_two(text))
