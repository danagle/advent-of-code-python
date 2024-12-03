"""
Advent of Code 2020
Day 1: Report Repair
https://adventofcode.com/2020/day/1
"""


def read_input_list(filename):
    with open(filename, "r") as f:
        values = f.read().strip().splitlines()
    return list(map(int, values))


def part_one(numbers):
    previous_values = set()
    for value in numbers:
        target = 2020 - value
        if target in previous_values:
            break
        previous_values.add(value)
    return target * value


def part_two(numbers):
    # Sort the numbers to enable the two-pointer technique
    numbers.sort()
    # Iterate over the numbers
    for i in range(len(numbers) - 2):
        # Use two-pointer technique to find the other two numbers
        left, right = i + 1, len(numbers) - 1
        while left < right:
            current_sum = numbers[i] + numbers[left] + numbers[right]
            if current_sum == 2020:
                return numbers[i] * numbers[left] * numbers[right]
            elif current_sum < 2020:
                left += 1
            else:
                right -= 1
    # If no triplet is found, return None
    return None


if __name__ == "__main__":
    numbers_list = read_input_list("input.txt")
    print(part_one(numbers_list))
    print(part_two(numbers_list))
