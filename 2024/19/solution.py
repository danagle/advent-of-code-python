"""
Advent of Code 2024
Day 19: Linen Layout
https://adventofcode.com/2024/day/19
"""
from time import perf_counter as measure_time

def performance_profiler(method):
    """
    A decorator that measures and prints the execution time of a method.
    
    This decorator wraps the given method and calculates its execution time,
    providing performance insights for the decorated function.
    
    Args:
        method (callable): The function to be timed
    
    Returns:
        callable: A wrapper function that measures the method's execution time
    """
    def timing_wrapper(*args, **kwargs):
        # Record the start time before method execution
        start_time = measure_time()
        
        # Execute the original method
        result = method(*args, **kwargs)
        
        # Print the execution time with high precision
        print(
            f"Method {method.__name__} took: "
            f"{measure_time() - start_time:2.5f} sec"
        )
        
        # Return the original method's result
        return result
    return timing_wrapper


def read_input(file_path):
    with open(file_path, "r") as file:
        input = file.read().split("\n\n")
    patterns = input[0].strip().split(", ")
    designs = input[1].split()
    return patterns, designs


def count_patterns(design, patterns, cache={}):
    if design == "":
        return 1
    if design in cache:
        return cache[design]

    total = 0
    for pattern in patterns:
        if design.startswith(pattern):
            remaining = design[len(pattern):]
            total += count_patterns(remaining, patterns, cache)

    cache[design] = total
    return total


@performance_profiler
def solve_day_19(patterns, designs):
    possible_designs = 0
    total_arrangements = 0

    for design in designs:
        total = count_patterns(design, patterns)
        if total > 0:
            possible_designs += 1
        total_arrangements += total

    return possible_designs, total_arrangements


if __name__ == "__main__":
    patterns, designs = read_input("input.txt")
    p1, p2 = solve_day_19(patterns, designs)
    print("Part 1:", p1)
    print("Part 2:", p2)
    