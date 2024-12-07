"""
Advent of Code 2024
Day 7: Bridge Repair
https://adventofcode.com/2024/day/7
"""
import re
from collections import deque
from time import perf_counter as measure_time

def performance_profiler(method):
    def timing_wrapper(*args, **kwargs):
        start_time = measure_time()
        result = method(*args, **kwargs)
        print(
            f"Method {method.__name__} took: "
            f"{measure_time() - start_time:2.5f} sec"
        )
        return result
    return timing_wrapper


def read_input(filename: str) -> list[tuple[int, int, deque[int]]]:
    number_pattern = re.compile(r"\d+")
    input_data = []

    with open("input.txt", "r") as input_file:
        lines = input_file.read().splitlines()

    for line in lines:
        numbers = [int(x) for x in re.findall(number_pattern, line)]
        input_data.append((numbers[0], numbers[1], deque(reversed(numbers[2:]))))

    return input_data


def reached_target(target: int, current: int, operands: deque[int], concat: bool) -> bool:
    """
    Determines whether a target value (target) can be reached using a series
    of operations on a deque of integers (operands) and a current value (curr).

    Args:
        target: The target value to reach.
        current: The current value in the calculation.
        operands: A deque (double-ended queue) of integers to process.
        concat: A boolean flag indicating whether concatenation of numbers (joining digits) is allowed.
    """
    # The base case where there are no operands remaining. Target achieved?
    if len(operands) == 0:
        return target == current
    else:
        # Remove the last element
        next = operands.pop()
        # Recursively call the function with addition and multiplication operations
        valid = (reached_target(target, current + next, operands, concat)
                 or reached_target(target, current * next, operands, concat))
        # Attempt to concatenate only if not already valid
        if concat and not valid:
            valid = reached_target(target, int(str(current) + str(next)), operands, concat)
        # Restore the state
        operands.append(next)
        # Return boolean result
        return valid


@performance_profiler
def part1(data):
    return sum(x[0] for x in data if reached_target(x[0], x[1], x[2], False))


@performance_profiler
def part2(data):
    return sum(x[0] for x in data if reached_target(x[0], x[1], x[2], True))


if __name__ == "__main__":
    parsed_data = read_input("input.txt")

    print("Part 1:", part1(parsed_data))
    print("Part 2:", part2(parsed_data))
