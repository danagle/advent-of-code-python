"""
Advent of Code 2024
Day 8: Resonant Collinearity
https://adventofcode.com/2024/day/8
"""
from typing import Dict, List, Tuple, Set
from collections import defaultdict
from itertools import combinations
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


def read_input(file_path: str) -> Tuple[Dict[str, List[Tuple[int, int]]], int, int]:
    nodes = defaultdict(list)
    
    with open(file_path, "r") as f:
        grid = f.readlines()
    
    max_rows, max_cols = len(grid), len(grid[0].strip())
    
    for i, row in enumerate(grid):
        for j, char in enumerate(row.strip()):
            if char != ".":
                nodes[char].append((i, j))
    
    return (nodes, max_rows, max_cols)


def antinode_single(
    point_a: Tuple[int, int], 
    point_b: Tuple[int, int], 
    max_rows: int, 
    max_cols: int
) -> Set[Tuple[int, int]]:
    """
    Calculate a single antinode point with boundary checking.
    
    Args:
        point_a: First point coordinates
        point_b: Second point coordinates
        max_rows: Maximum number of rows in the grid
        max_cols: Maximum number of columns in the grid
    
    Returns:
        Set containing the antinode point if within bounds
    """
    x1, y1 = point_a
    x2, y2 = point_b
    
    # Calculate reflected point
    new_row = x2 + (x2 - x1)
    new_col = y2 + (y2 - y1)
    
    # Boundary check and point generation
    return {(new_row, new_col)} if 0 <= new_col < max_cols and 0 <= new_row < max_rows else set()


def antinode_trajectory(
    point_a: Tuple[int, int], 
    point_b: Tuple[int, int], 
    max_rows: int, 
    max_cols: int
) -> Set[Tuple[int, int]]:
    """
    Generate a trajectory of antinode points.
    
    Args:
        point_a: First point coordinates
        point_b: Second point coordinates
        max_rows: Maximum number of rows in the grid
        max_cols: Maximum number of columns in the grid
    
    Returns:
        Set of valid antinode points along the trajectory
    """
    x1, y1 = point_a
    x2, y2 = point_b
    
    # Calculate delta values
    dx = x2 - x1
    dy = y2 - y1
    
    # Initialize result set with starting point
    trajectory_points = {(x2, y2)}
    
    # Compute initial reflected point
    new_row = x2 + dx
    new_col = y2 + dy
    
    # Generate points along the trajectory
    while 0 <= new_col < max_cols and 0 <= new_row < max_rows:
        trajectory_points.add((new_row, new_col))
        new_row += dx
        new_col += dy
    
    return trajectory_points


def process_antinodes(
    data: Tuple[Dict[str, List[Tuple[int, int]]], int, int], 
    antinode_func: callable
) -> int:
    """
    Generic function to process antinodes using a specified antinode generation function.
    
    Args:
        data: Tuple containing nodes, max_rows, and max_cols
        antinode_func: Function to generate antinode points
    
    Returns:
        Number of unique antinode points
    """
    nodes, max_rows, max_cols = data
    antinodes = set()
    
    for node_list in nodes.values():
        # Use combinations to avoid duplicate and self-comparisons
        for node1, node2 in combinations(node_list, 2):
            antinodes.update(antinode_func(node1, node2, max_rows, max_cols))
            antinodes.update(antinode_func(node2, node1, max_rows, max_cols))
    
    return len(antinodes)


@performance_profiler
def part_one(data):
    """
    Process part one using single point antinode generation.
    
    Args:
        data: Input data containing nodes and grid dimensions
    """
    print(process_antinodes(data, antinode_single))


@performance_profiler
def part_two(data):
    """
    Process part two using trajectory antinode generation.
    
    Args:
        data: Input data containing nodes and grid dimensions
    """
    print(process_antinodes(data, antinode_trajectory))


if __name__ == "__main__":
    input_data = read_input("input.txt")
    part_one(input_data)
    part_two(input_data)
