"""
Advent of Code 2024
Day 12: Garden Groups
https://adventofcode.com/2024/day/12
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


def parse_input(file_path):
    """
    Parse the input file into a grid representation using complex numbers.
    
    Reads the input file and converts it into a dictionary where:
    - Keys are complex numbers representing grid coordinates (x + y*1j)
    - Values are the characters at those coordinates
    
    Args:
        file_path (str): Path to the input file
    
    Returns:
        dict: A dictionary representing the grid with complex number coordinates
    """
    # Read the file and strip any trailing whitespace
    with open(file_path, "r") as f:
        lines = f.read().strip().splitlines()

    # Create grid using complex number coordinates
    grid = {}
    for row, line in enumerate(lines):
        for col, tile in enumerate(line):
            # Use complex number (x + y*1j) as unique grid coordinate
            grid[col + row * 1j] = tile
    
    return grid


def flood_fill(grid, start):
    """
    Perform a flood fill algorithm to find a connected region in the grid.
    
    Explores and collects all connected positions with the same symbol 
    starting from the given start position.
    
    Args:
        grid (dict): The grid dictionary with complex number coordinates
        start (complex): Starting position for flood fill
    
    Returns:
        set: A set of all positions in the connected region
    """
    # Initialize the region with the start position
    region = set([start])
    
    # Get the symbol at the start position
    symbol = grid[start]
    
    # Queue for breadth-first search
    queue = [start]
    
    # Explore the region
    while queue:
        # Get current position from queue
        pos = queue.pop()
        
        # Check adjacent positions (right, left, down, up)
        for d in [1, -1, 1j, -1j]:
            # Calculate new position
            new_pos = pos + d
            
            # Check if new position is valid and not yet explored
            if (new_pos in grid and 
                new_pos not in region and 
                grid[new_pos] == symbol):
                # Add to region and queue for further exploration
                region.add(new_pos)
                queue.append(new_pos)
    
    return region


def get_area(region):
    """
    Calculate the area of a given region.
    
    Args:
        region (tuple): A tuple containing the region's symbol and positions
    
    Returns:
        int: Number of positions in the region
    """
    # Return the number of positions in the region
    return len(region[1])


def get_perimeter(region):
    """
    Calculate the perimeter of a given region.
    
    Args:
        region (tuple): A tuple containing the region's symbol and positions
    
    Returns:
        int: Number of boundary edges
    """
    perimeter = 0
    for pos in region[1]:
        # Check adjacent positions
        for d in [1, -1, 1j, -1j]:
            new_pos = pos + d
            # Count edges that are outside the region
            if new_pos not in region[1]:
                perimeter += 1
    return perimeter


@performance_profiler
def part_one(grid):
    """
    Identifies all regions in the grid and calculates a price 
    based on area and perimeter.
    
    Args:
        grid (dict): The grid dictionary with complex number coordinates
    
    Returns:
        list: List of identified regions
    """
    # List to store identified regions
    regions = []
    
    # Set of unexplored grid positions
    unexplored = set(grid.keys())
    
    # Explore and identify all regions
    while len(unexplored) > 0:
        # Pick a starting position
        start = unexplored.pop()
        
        # Perform flood fill to identify the region
        region = flood_fill(grid, start)
        
        # Remove explored positions from unexplored set
        unexplored -= region
        
        # Store region information
        regions.append((grid[start], region))

    # Calculate total price
    price = 0
    for region in regions:
        # Calculate area and perimeter for each region
        area, perimeter = get_area(region), get_perimeter(region)
        price += area * perimeter

    print("Part 1:", price)
    # Return regions for use in part 2
    return regions


def get_sides_count(region):
    """
    Count the number of distinct sides for a given region.
    
    Identify unique sides by tracking perimeter edges and their orientation.
    
    Args:
        region (tuple): A tuple containing the region's symbol and positions
    
    Returns:
        int: Number of distinct sides
    """
    # Set to track perimeter edges and directions
    perimeter_edges = set()
    
    # Collect perimeter edges
    for pos in region[1]:
        for direction in [1, -1, 1j, -1j]:
            new_pos = pos + direction
            if new_pos not in region[1]:
                perimeter_edges.add((new_pos, direction))
    
    # Count distinct sides
    distinct_sides = 0
    while len(perimeter_edges) > 0:
        # Pop a perimeter edge
        pos, direction = perimeter_edge.pop()
        distinct_sides += 1
        
        # Explore in current direction
        next_pos = pos + direction * 1j
        while (next_pos, direction) in perimeter_edges:
            perimeter_edges.remove((next_pos, direction))
            next_pos += direction * 1j
        
        # Explore in opposite direction
        next_pos = pos + direction * -1j
        while (next_pos, direction) in perimeter_edges:
            perimeter_edges.remove((next_pos, direction))
            next_pos += direction * -1j
    
    return distinct_sides


@performance_profiler
def part_two(regions):
    """
    Solve part two of the Advent of Code challenge.
    
    Calculates a price based on region areas and side counts.
    
    Args:
        regions (list): List of regions identified in part one
    """
    # Calculate total price
    price = 0
    for region in regions:
        # Calculate area and side count for each region
        area, sides = get_area(region), get_sides_count(region)
        price += area * sides
        
    print("Part 2:", price)


if __name__ == "__main__":
    grid = parse_input("input.txt")
    regions = part_one(grid)
    part_two(regions)