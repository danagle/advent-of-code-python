"""
Advent of Code 2024
Day 25: Code Chronicle
https://adventofcode.com/2024/day/25
"""
import itertools
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


def parse_input(file_path):
    with open(file_path, "r") as f:
        locks = [schematic.splitlines() for schematic in f.read().split("\n\n")]
        
    return [{(col, row) for col, line in enumerate(lock) 
                        for row, tile in enumerate(line) if tile == "#"} 
                        for lock in locks]


@performance_profiler
def part_one(locks):
    pairs = 0
    for pattern_a, pattern_b in itertools.combinations(locks, 2):
        if not set.intersection(pattern_a, pattern_b):
            pairs += 1
    return pairs


if __name__ == "__main__":
    locks = parse_input("input.txt")
    p1 = part_one(locks)
    print("Part 1:", p1)
