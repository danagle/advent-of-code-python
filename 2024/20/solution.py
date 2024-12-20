"""
Advent of Code 2024
Day 20: Race Condition
https://adventofcode.com/2024/day/20
"""
import networkx as nx
from itertools import product
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


def parse_input(filepath):
    with open(filepath, "r") as f:
        grid = [list(line.strip()) for line in f]

    start = (-1, -1)
    end = (-1, -1)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)
    if start == (-1, -1) or end == (-1, -1):
        raise ValueError("Start or end position not found in grid")
    return grid, start, end


def build_graph(grid, allow_walls = False):
    """Build a graph representation of the grid."""
    G = nx.Graph()
    height, width = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for y, x in product(range(height), range(width)):
        if not allow_walls and grid[y][x] == '#':
            continue
        pos = (y, x)
        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            if (0 <= new_y < height and 
                0 <= new_x < width and 
                (allow_walls or grid[new_y][new_x] in '.SE')):
                G.add_edge(pos, (new_y, new_x), weight=1)
    
    return G


def find_all_cheats(grid, start, end, max_cheat_steps):
    G = build_graph(grid)
    try:
        normal_time = nx.shortest_path_length(G, start, end, weight='weight')
    except nx.NetworkXNoPath:
        return []
    
    # Build graph that includes wall passages
    G_walls = build_graph(grid, allow_walls=True)
    
    # Pre-calculate all shortest paths from start and to end
    start_distances = nx.single_source_dijkstra_path_length(G, start, weight='weight')
    end_distances = nx.single_source_dijkstra_path_length(G, end, weight='weight')
    
    saved_times = []
    height, width = len(grid), len(grid[0])
    max_end_dist = normal_time - 100  # Maximum distance from cheat end to end
    
    # For each valid path position
    for y, x in product(range(height), range(width)):
        if grid[y][x] not in '.SE':
            continue
        start_pos = (y, x)
        if start_pos not in start_distances:
            continue
            
        start_dist = start_distances[start_pos]
        
        # Find all reachable positions within max_cheat_steps
        cheat_ends = nx.single_source_dijkstra_path_length(G_walls, start_pos, cutoff=max_cheat_steps)
        
        # Check each possible cheat end
        for end_pos, cheat_steps in cheat_ends.items():
            if grid[end_pos[0]][end_pos[1]] not in '.SE':
                continue
            if end_pos not in end_distances:
                continue
                
            end_dist = end_distances[end_pos]
            if end_dist > max_end_dist:
                continue
                
            # Calculate total time with cheat
            cheat_time = start_dist + cheat_steps + end_dist
            time_saved = normal_time - cheat_time
            
            if time_saved >= 100:
                saved_times.append(time_saved)
    
    return saved_times


@performance_profiler
def part_one(grid, start, end):
    return len(find_all_cheats(grid, start, end, max_cheat_steps=2))


@performance_profiler
def part_two(grid, start, end):
    return len(find_all_cheats(grid, start, end, max_cheat_steps=20))


if __name__ == "__main__":
    grid, start, end = parse_input("input.txt")
    p1 = part_one(grid, start, end)
    p2 = part_two(grid, start, end)
    print("Part 1:", p1)
    print("Part 2:", p2)
