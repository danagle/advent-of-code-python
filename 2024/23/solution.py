"""
Advent of Code 2024
Day 23: LAN Party
https://adventofcode.com/2024/day/23
"""
import networkx
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
        lines = f.read().strip().splitlines()

    graph = networkx.Graph(line.strip().split('-') for line in lines)
    cliques = list(networkx.enumerate_all_cliques(graph))

    return cliques


@performance_profiler
def part_one(lan_cliques):
    count = 0
    for clique in lan_cliques:
        if len(clique) != 3:
            continue
            
        has_t_node = False
        for node in clique:
            if node.startswith('t'):
                has_t_node = True
                break
                
        if has_t_node:
            count += 1
            
    return count


@performance_profiler
def part_two(lan_cliques):
    max_length = 0
    max_clique_str = ''
    
    for clique in lan_cliques:
        # Sort the nodes within the clique
        sorted_nodes = sorted(clique)
        # Join them with commas
        clique_str = ','.join(sorted_nodes)
        
        if len(clique_str) > max_length:
            max_length = len(clique_str)
            max_clique_str = clique_str
            
    return max_clique_str


if __name__ == "__main__":
    cliques = parse_input("input.txt")

    p1 = part_one(cliques)
    print("Part 1:", p1)
    p2 = part_two(cliques)
    print("Part 2:", p2)
