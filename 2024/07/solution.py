"""
Advent of Code 2024
Day 7: Bridge Repair
https://adventofcode.com/2024/day/7
"""
import re
from collections import deque
from functools import partial
from multiprocessing import Pool
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
    of operations on a deque of integers (operands) and a current value (current).

    Args:
        target: The target value to reach.
        current: The current value in the calculation.
        operands: A deque (double-ended queue) of integers to process.
        concat: A boolean flag indicating whether concatenation of numbers (joining digits) is allowed.
    """
    # The base case where there are no operands remaining. Target achieved?
    if len(operands) == 0 or current > target:
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


def process_entry(entry, concat=False):
    """
    Process a single entry for parallelization.
    
    Args:
        entry: A tuple containing (target, current, operands)
        concat: A boolean flag for concatenation
    
    Returns:
        A tuple of (target, is_valid)
    """
    target, current, operands = entry
    is_valid = reached_target(target, current, operands, concat)
    return (target, is_valid)


@performance_profiler
def part1_parallel(data, num_processes=None):
    """
    Parallel implementation of part1 function.
    
    Args:
        data: List of entries to process
        num_processes: Number of processes to use (None uses all available cores)
    
    Returns:
        Tuple of (total, failures)
    """
    # Use a process pool
    with Pool(processes=num_processes) as pool:
        # Process all entries in parallel
        results = pool.map(partial(process_entry, concat=False), data)
    
    # Aggregate results
    total = 0
    failures = []
    for target, is_valid in results:
        if is_valid:
            total += target
        else:
            # Find the original entry to add to failures
            original_entry = next(entry for entry in data if entry[0] == target)
            failures.append(original_entry)
    
    return total, failures


@performance_profiler
def part1(data):
    total = 0
    failures = []
    for x in data:
        if reached_target(x[0], x[1], x[2], False):
            total += x[0]
        else:
            failures.append(x)
    return total, failures


@performance_profiler
def part2_parallel(data, num_processes=None):
    """
    Parallel implementation of part2 function.
    
    Args:
        data: List of entries to process
        num_processes: Number of processes to use (None uses all available cores)
    
    Returns:
        Sum of targets that can be reached with concatenation
    """
    # Use a process pool
    with Pool(processes=num_processes) as pool:
        # Process all entries in parallel with concatenation enabled
        results = pool.map(partial(process_entry, concat=True), data)
    
    # Sum the targets that are valid
    return sum(target for target, is_valid in results if is_valid)
    

@performance_profiler
def part2(data):
    return sum(x[0] for x in data if reached_target(x[0], x[1], x[2], True))


if __name__ == "__main__":
    NUM_PROCS = 4
    parsed_data = read_input("input.txt")

    p1_total, p2_input = part1(parsed_data)
    p1p_total, p2p_input = part1_parallel(parsed_data, NUM_PROCS)

    p2_total = p1_total + part2(p2_input)
    p2p_total = p1p_total + part2_parallel(p2p_input, NUM_PROCS)

    print("Part 1:", p1_total, p1p_total)
    print("Part 2:", p2_total, p2p_total)
