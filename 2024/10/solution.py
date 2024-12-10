"""
Advent of Code 2024
Day 10: Hoof It
https://adventofcode.com/2024/day/10
"""
from collections import defaultdict
from time import perf_counter as measure_time

def performance_profiler(method):
    """
    A decorator that measures and prints the execution time of a method.
    
    Args:
        method (callable): The function to be timed
    
    Returns:
        callable: A wrapper function that measures the method's execution time
    """
    def timing_wrapper(*args, **kwargs):
        start_time = measure_time()
        result = method(*args, **kwargs)
        print(
            f"Method {method.__name__} took: "
            f"{measure_time() - start_time:2.5f} sec"
        )
        return result
    return timing_wrapper


def parse_input(file_path):
    """
    Parse the input file and convert it into a topographic map.
    
    Args:
        file_path (str): Path to the input file
    
    Returns:
        tuple: A tuple containing:
            - topographic_map (defaultdict): A mapping of (x, y) coordinates to elevation
            - trail_heads (list): List of starting points with elevation 0
    """
    # Read the file and split into lines
    with open(file_path, "r") as f:
        lines = f.read().strip().splitlines()

    # Create a defaultdict to store the topographic map
    # Each coordinate maps to its elevation value
    topographic_map = defaultdict(int)
    for row, line in enumerate(lines):
        for col, elevation in enumerate(line):
            topographic_map[(col, row)] = int(elevation)

    # Identify trail heads (positions with elevation 0)
    trail_heads = [k for k, v in topographic_map.items() if v == 0]

    return (topographic_map, trail_heads)


@performance_profiler
def solve_day_10(data):
    """
    Args:
        data (tuple): A tuple containing the topographic map and trail heads
    """
    # Unpack the topographic map and trail heads
    tm, th = data

    def dfs(pos):
        """
        Perform a depth-first search to trace a trail from a given starting point.
        
        Args:
            pos (tuple): Starting position coordinates
        
        Returns:
            list: Positions along the trail
        """
        s = []
        # Explore adjacent positions in four directions (left, right, up, down)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            # Calculate the new position
            new_pos = (pos[0] + dx, pos[1] + dy)
            
            # Get the elevation of the new position
            new_value = tm.get(new_pos)
            
            # Check if the new position is a valid next step 
            # (elevation increases by exactly 1)
            if tm[pos] + 1 == new_value:
                # If the trail reaches elevation 9, add the position
                # Otherwise, continue exploring the trail recursively
                s += [new_pos] if new_value == 9 else dfs(new_pos)
        
        return s

    # Trace trails from each trail head
    ts = [dfs(h) for h in th]
    
    # Calculate:
    # 1. Total sum of the scores of all trailheads on the topographic map
    # 2. Total sum of the ratings of all trailheads
    return (sum(len(set(t)) for t in ts), sum(len(t) for t in ts))


if __name__ == "__main__":
    input_data = parse_input("input.txt")

    p1, p2 = solve_day_10(input_data)

    print("Part 1:", p1)
    print("Part 2:", p2)
