"""
Advent of Code 2024
Day 13: Claw Contraption
https://adventofcode.com/2024/day/13
"""
from time import perf_counter as measure_time
from typing import Dict, Tuple

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


def parse_input(file_name):
    with open(file_name, "r") as f:
        lines = [line.strip() for line in f]
    return lines


@performance_profiler
def solve_day_13(lines, is_part2=False):
    tokens = 0
    offset = 10000000000000 if is_part2 else 0
    for line in lines:
        if line.startswith("Button"):
            line_parts = line.split(" ")
            a = line_parts[1].split(":")[0]
            if a == "A":
                a_x = int(line_parts[2][2:-1])
                a_y = int(line_parts[3][2:])
            else:
                b_x = int(line_parts[2][2:-1])
                b_y = int(line_parts[3][2:])
            
        elif line.startswith("Prize"):
            line_parts = line.split(" ")
            p_x = int(line_parts[1][2:-1]) + offset
            p_y = int(line_parts[2][2:]) + offset
            m = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)
            n = (p_y*a_x - p_x*a_y) / (a_x*b_y - a_y*b_x)
            if m == int(m) and n == int(n):
                tokens += int(3 * m + n)

    print(tokens)


if __name__ == "__main__":
    input_lines = parse_input("input.txt")
    solve_day_13(input_lines)
    solve_day_13(input_lines, True)
