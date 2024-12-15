"""
Advent of Code 2024
Day 15: Warehouse Woes
https://adventofcode.com/2024/day/15
"""
from collections import defaultdict
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
    Parse the input file into grid and moves sections.

    Args:
        file_path (str): Path to the input file

    Returns:
        tuple: A tuple containing the raw grid and raw moves sections
    """
    with open(file_path, "r") as f:
        parts = f.read().strip().split("\n\n")

    return parts[0], parts[1]


def create_grid(raw_grid):
    """
    Convert raw grid text into a dictionary-based grid representation.

    Args:
        raw_grid (str): Raw grid text from input file

    Returns:
        tuple: A defaultdict grid and the starting position
    """
    grid = defaultdict(lambda: "#")
    for y, line in enumerate(raw_grid.split("\n")):
        for x, tile in enumerate(line):
            grid[(x, y)] = tile
            if tile == "@":
                start = (x, y)
    return grid, start


def scale_up_grid_text(raw_grid):
    """
    Scale up the grid text by replacing tiles with larger representations.

    This method is used for Part Two to increase grid complexity.
    
    Args:
        raw_grid (str): Raw grid text

    Returns:
        str: Scaled-up grid text
    """
    scaled_up = []
    for line in raw_grid.split("\n"):
        scaled_up.append(line.replace("O", "[]").replace(".", "..").replace("#", "##").replace("@", "@."))
    return "\n".join(scaled_up)


def move_direction(symbol):
    """
    Convert movement symbols to coordinate deltas.

    Args:
        symbol (str): Movement direction symbol (^, v, <, >)

    Returns:
        tuple: Coordinate delta for the given movement
    """
    movements = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
    return movements[symbol]


def next_position(position, move):
    """
    Calculate the next position given current position and move.

    Args:
        position (tuple): Current (x, y) coordinates
        move (tuple): Movement delta

    Returns:
        tuple: New (x, y) coordinates after moving
    """
    px, py = position
    dx, dy = move
    return (px + dx, py + dy)


def sum_gps_coordinates(grid):
    """
    Calculate the sum of GPS coordinates for specific grid tiles.

    Args:
        grid (dict): Grid representation

    Returns:
        int: Sum of GPS coordinates
    """
    return sum((100 * y + x) for (x, y) in grid if grid[(x, y)] in "O[")


@performance_profiler
def part_one(current_pos, grid, moves):
    """
    Solve Part One: Navigate the grid and move boxes.

    Args:
        current_pos (tuple): Starting player position
        grid (dict): Grid representation
        moves (list): List of movement deltas

    Returns:
        int: Sum of GPS coordinates after movements
    """
    for move in moves:
        new_pos = next_position(current_pos, move)
        # Skip if new position is a wall
        if grid[new_pos] == "#":
            continue
        # Handle box movement
        elif grid[new_pos] == "O":
            # Find end of current box sequence
            end_box = new_pos
            while grid[end_box] == "O":
                end_box = next_position(end_box, move)

            # Cannot move if blocked by wall
            if grid[end_box] == "#":
                continue
            else:
                grid[end_box] = "O"
                grid[new_pos] = "@"
                grid[current_pos] = "."
                current_pos = new_pos

        # Simple movement
        elif grid[new_pos] == ".":
            grid[new_pos] = "@"
            grid[current_pos] = "."
            current_pos = new_pos

    return sum_gps_coordinates(grid)


@performance_profiler
def part_two(current_pos, grid, moves):
    """
    Solve Part Two: Navigate a scaled-up grid with more complex box movements.

    Args:
        current_pos (tuple): Starting player position
        grid (dict): Grid representation
        moves (list): List of movement deltas

    Returns:
        int: Sum of GPS coordinates after movements
    """

    def can_move(box_pos, move, boxes):
        """
        Recursively check if boxes can be moved without hitting walls.

        Args:
            box_pos (tuple): Current box position
            move (tuple): Movement delta
            boxes (set): Set to track moved boxes

        Returns:
            bool: Whether boxes can be moved
        """
        checked = set()
        # Handle different box sides
        if grid[box_pos] == "[":
            checked = set([box_pos, next_position(box_pos, move_direction(">"))])
        elif grid[box_pos] == "]":
            checked = set([box_pos, next_position(box_pos, move_direction("<"))])

        new_positions = set([next_position(p, move) for p in checked]) - checked

        # Fail if new positions would hit a wall
        if any(grid[p] == "#" for p in new_positions):
            return False

        # Recursively check if all new positions are valid
        valid = all(grid[p] == "." or can_move(p, move, boxes) for p in new_positions)

        if valid:
            for c in checked:
                boxes.add(c)
            return valid

        return False

    for move in moves:
        new_pos = next_position(current_pos, move)
        if grid[new_pos] == "#":
            continue
        elif grid[new_pos] in "[]":
            boxes = set()
            if can_move(new_pos, move, boxes):
                # Move boxes and update grid
                new_boxes = {}
                for box_pos in boxes:
                    new_boxes[next_position(box_pos, move)] = grid[box_pos]
                    grid[box_pos] = "."
                for box_pos in new_boxes:
                    grid[box_pos] = new_boxes[box_pos]
                grid[new_pos] = "@"
                grid[current_pos] = "."
                current_pos = new_pos
        elif grid[new_pos] == ".":
            grid[new_pos] = "@"
            grid[current_pos] = "."
            current_pos = new_pos

    return sum_gps_coordinates(grid)


if __name__ == "__main__":
    raw_grid, raw_moves = parse_input("input.txt")

    moves = list(map(lambda d: move_direction(d), "".join(raw_moves.split("\n"))))

    grid, start = create_grid(raw_grid)

    p1 = part_one(start, grid, moves)
    print(f"Part 1: {p1}")

    scaled_text = scale_up_grid_text(raw_grid)
    grid, start = create_grid(scaled_text)

    p2 = part_two(start, grid, moves)
    print(f"Part 2: {p2}")
