"""
Advent of Code 2024
Day 6: Guard Gallivant
https://adventofcode.com/2024/day/6
"""
from typing import List, Tuple, Dict, Set
import concurrent.futures
import time
from dataclasses import dataclass

@dataclass
class DirectionVector:
    """Represents a 2D movement vector."""
    row: int
    col: int

def bounds_check_factory_2d(grid: List[List[str]]) -> callable:
    """
    Create a closure for checking if coordinates are within a 2D grid's boundaries.
    
    Args:
        grid (List[List[str]]): The 2D grid to check boundaries against.
    
    Returns:
        callable: A function that checks if given coordinates are within grid bounds.
    """
    max_y = len(grid)
    max_x = len(grid[0])
    
    def is_within_bounds(i: int, j: int) -> bool:
        """
        Check if the given coordinates are within the grid boundaries.
        
        Args:
            i (int): Row coordinate.
            j (int): Column coordinate.
        
        Returns:
            bool: True if coordinates are within bounds, False otherwise.
        """
        return 0 <= i < max_y and 0 <= j < max_x

    return is_within_bounds

def parse_input(filepath: str) -> Tuple[List[List[str]], Tuple[int, int]]:
    """
    Parse input text to create the grid and identify the start position.
    
    Args:
        filepath (str): Path to the input file.
    
    Returns:
        Tuple[List[List[str]], Tuple[int, int]]: Parsed grid and start position.
    """
    # Read input from file
    with open(filepath, 'r') as file:
        input_lines = file.read().strip().split('\n')
    
    # Initialize grid and start position
    grid = []
    start_pos = (0, 0)
    
    # Parse input grid, identify start position marked by '^'
    for i, line in enumerate(input_lines):
        row = []
        for j, char in enumerate(line):
            if char == '^':
                start_pos = (i, j)
            row.append(char)
        
        if row:
            grid.append(row)
    
    return grid, start_pos

def day06_part_one(grid: List[List[str]], start_pos: Tuple[int, int], 
                   is_within_bounds: callable) -> int:
    """
    Traverse the grid, marking unique tiles.
    
    Args:
        grid (List[List[str]]): The input grid.
        start_pos (Tuple[int, int]): Starting position.
        is_within_bounds (callable): Function to check grid boundaries.
    
    Returns:
        int: Number of unique tiles visited.
    """
    # Create a copy of the grid to avoid modifying the original
    grid_copy = [row.copy() for row in grid]
    
    # Initial direction is upward
    direction = DirectionVector(-1, 0)
    row, col = start_pos
    unique_tiles = 0
    
    while is_within_bounds(row, col):
        nrow, ncol = row + direction.row, col + direction.col
        
        # Change direction if hitting a wall '#'
        if is_within_bounds(nrow, ncol) and grid_copy[nrow][ncol] == '#':
            direction.row, direction.col = direction.col * -1, direction.row
        
        # Mark tile as visited if not already marked
        if grid_copy[row][col] != 'X':
            grid_copy[row][col] = 'X'
            unique_tiles += 1
        
        # Move to next position
        row += direction.row
        col += direction.col
    
    return unique_tiles

def day06_part_two(grid: List[List[str]], start_pos: Tuple[int, int], 
                   is_within_bounds: callable, seen_tiles: int) -> int:
    """
    Concurrent exploration of potential obstacles.
    
    Args:
        grid (List[List[str]]): The input grid.
        start_pos (Tuple[int, int]): Starting position.
        is_within_bounds (callable): Function to check grid boundaries.
        seen_tiles (int): Number of tiles seen in part one.
    
    Returns:
        int: Number of possible obstacle placements.
    """
    obstacles_possible = 0
    
    def explore_obstacle(i: int, j: int) -> bool:
        """
        Explore a potential obstacle placement.
        
        Args:
            i (int): Row of potential obstacle.
            j (int): Column of potential obstacle.
        
        Returns:
            bool: Whether an obstacle is possible at this location.
        """
        # Skip already visited or start tile
        if grid[i][j] != 'X' or (i == start_pos[0] and j == start_pos[1]):
            return False
        
        # Initial direction and state tracking
        direction = DirectionVector(-1, 0)
        seen: Set[Tuple[int, int, int, int]] = set()
        row, col = start_pos[0], start_pos[1]
        
        while is_within_bounds(row, col):
            # Detect cycle
            state = (row, col, direction.row, direction.col)
            if state in seen:
                return True
            
            nrow, ncol = row + direction.row, col + direction.col
            
            # Change direction on wall or reaching target tile
            if (nrow == i and ncol == j) or \
               (is_within_bounds(nrow, ncol) and grid[nrow][ncol] == '#'):
                direction.row, direction.col = -direction.col, direction.row
            else:
                # Track visited states to detect cycles
                seen.add(state)
                row += direction.row
                col += direction.col
        
        return False
    
    # Use ThreadPoolExecutor for concurrent exploration
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create futures for each grid cell
        futures = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                futures.append(executor.submit(explore_obstacle, i, j))
        
        # Count obstacles possible
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                obstacles_possible += 1
    
    return obstacles_possible

def main():
    """
    Main function to solve Day 6 challenge.
    """
    # Parse input file
    filepath = "input.txt"
    grid, start_pos = parse_input(filepath)
    
    # Create bounds checking function for the grid
    is_within_bounds = bounds_check_factory_2d(grid)
    
    # Part 1
    start_time = time.time()
    part1 = day06_part_one(grid, start_pos, is_within_bounds)
    print(f"Part 1 execution time: {time.time() - start_time:.4f} seconds")
    
    # Part 2
    start_time = time.time()
    part2 = day06_part_two(grid, start_pos, is_within_bounds, part1)
    print(f"Part 2 execution time: {time.time() - start_time:.4f} seconds")
    
    print(f"Solution Part One: {part1}")
    print(f"Solution Part Two: {part2}")

if __name__ == "__main__":
    main()
