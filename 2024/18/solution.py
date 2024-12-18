"""
Advent of Code 2024
Day 18: RAM Run
https://adventofcode.com/2024/day/18
"""
import networkx as nx
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
    with open(file_path) as f:
        corrupt = list(tuple(map(int, line.split(","))) for line in f.read().strip().splitlines())
    return corrupt


@performance_profiler
def solve_day_18(corrupted_locations):
    memory = nx.grid_2d_graph(71, 71)

    for index, position in enumerate(corrupted_locations):
        memory.remove_node(position)
        if index == 1023:
            # Part 1
            print("Part 1:", nx.shortest_path_length(memory, (0, 0), (70, 70)))
        elif not nx.has_path(memory, (0, 0), (70, 70)):
            # Part 2
            print("Part 2:", position)
            break


if __name__ == "__main__":
    corrupted = read_input("input.txt")
    solve_day_18(corrupted)
