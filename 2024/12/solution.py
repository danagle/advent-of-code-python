"""
Advent of Code 2024
Day 12: Garden Groups
https://adventofcode.com/2024/day/12
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


def parse_input(file_name: str) -> Dict[Tuple[int, int], str]:
    """
    Parse input file into a grid representation.
    
    Args:
        file_name (str): Path to the input file
    
    Returns:
        Dict[Tuple[int, int], str]: Grid representation with (x,y) coordinates as keys
    """
    with open(file_name, "r") as file:
        content = file.read().strip().splitlines()
    
    grid = {}
    for y, line in enumerate(content):
        for x, tile in enumerate(line):
            grid[(x, y)] = tile
    
    return grid


@performance_profiler
def solve_day12(grid: Dict[Tuple[int, int], str]):
    """
    Solve AoC Day 12 challenge.
    
    Args:
        grid (Dict[Tuple[int, int], str]): Grid representation with (x,y) coordinates as keys
    
    Returns:
        Tuple[int, int, float]: Part 1 result, Part 2 result, and execution time
    """    
    # Track visited points to avoid reprocessing
    visited = set()
    
    # Variables for answers to part 1 and part 2
    part1, part2 = 0, 0
    
    # Directions: up, right, down, left
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    # Iterate through all points in the grid
    for point in grid:
        # Skip previously processed points
        if point in visited:
            continue
        
        visited.add(point)
        
        # Initialize region metrics
        area = 1        # Size of the current region (starts at 1)
        perimeter = 0   # Number of boundary edges
        sides = 0       # Number of distinct sides
        
        # Queue for breadth-first search of the region
        queue = [point]
        
        # Explore the connected region
        while queue:
            # Dequeue the current point
            current = queue.pop(0)
            
            # Check adjacent points
            for dx, dy in directions:
                # Calculate neighboring point
                neighbor = (current[0] + dx, current[1] + dy)
                
                # If neighbor has a different value, it's a boundary
                if grid.get(neighbor) != grid.get(current):
                    # Increment perimeter
                    perimeter += 1
                    
                    # Rotate 90-degrees to check adjacent regions
                    rotated = (current[0] - dy, current[1] + dx)
                    
                    # Determine if this is a distinct side
                    # Check if the rotated point is in a different region
                    # Verify if the point next to the rotated point is in the same original region
                    if (grid.get(rotated) != grid.get(current) or 
                        grid.get((rotated[0] + dx, rotated[1] + dy)) == grid.get(current)):
                        sides += 1
                
                # If neighbor is not visited and has same value, add to region
                elif neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    area += 1
        
        # Calculate part 1: area multiplied by perimeter
        part1 += area * perimeter
        
        # Calculate part 2: area multiplied by number of sides
        part2 += area * sides
    
    return part1, part2


if __name__ == "__main__":
    # Parse the input file into a grid representation
    grid = parse_input("input.txt")

    part1, part2 = solve_day12(grid)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
