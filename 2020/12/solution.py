"""
Advent of Code 2020
Day 12: Rain Risk
https://adventofcode.com/2020/day/12
"""
from pathlib import Path
from typing import List, Tuple


def read_input_file(filepath: str = "input.txt") -> List[Tuple[str, int]]:
    """Parse instructions like 'F10' -> ('F', 10)."""
    text = Path(filepath).read_text().strip().splitlines()
    return [(line[0], int(line[1:])) for line in text]


def rotate_right(east: int, north: int, steps: int) -> Tuple[int, int]:
    """
    Rotate the point (east, north) clockwise by 90° * steps.
    steps must be an integer (can be 0..3). Returns new (east, north).
    """
    steps = steps % 4
    x, y = east, north
    for _ in range(steps):
        # clockwise 90°: (x, y) -> (y, -x)
        x, y = y, -x
    return x, y


def part_one(instructions: List[Tuple[str, int]]) -> int:
    """
    Move the ship according to facing-direction rules.
    Returns the Manhattan distance from origin.
    """
    # Ship position: (east, north)
    x, y = 0, 0
    # facing index in order ['E','S','W','N'], start facing East
    directions = ["E", "S", "W", "N"]
    facing_idx = 0

    for action, value in instructions:
        if action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "E":
            x += value
        elif action == "W":
            x -= value
        elif action == "L":
            # left is counter-clockwise: subtract steps
            steps = (value // 90) % 4
            facing_idx = (facing_idx - steps) % 4
        elif action == "R":
            steps = (value // 90) % 4
            facing_idx = (facing_idx + steps) % 4
        elif action == "F":
            facing = directions[facing_idx]
            if facing == "N":
                y += value
            elif facing == "S":
                y -= value
            elif facing == "E":
                x += value
            elif facing == "W":
                x -= value
        else:
            raise ValueError(f"Unknown action {action}")

    return abs(x) + abs(y)


def part_two(instructions: List[Tuple[str, int]]) -> int:
    """
    Move the ship using a waypoint. The waypoint is relative to the ship.
    Waypoint starts 10 units east and 1 unit north.
    """
    # Ship position
    sx, sy = 0, 0
    # Waypoint relative position (east, north)
    wx, wy = 10, 1

    for action, value in instructions:
        if action == "N":
            wy += value
        elif action == "S":
            wy -= value
        elif action == "E":
            wx += value
        elif action == "W":
            wx -= value
        elif action == "L":
            # Convert left rotation into equivalent right rotation
            steps_right = (-value // 90) % 4
            wx, wy = rotate_right(wx, wy, steps_right)
        elif action == "R":
            steps_right = (value // 90) % 4
            wx, wy = rotate_right(wx, wy, steps_right)
        elif action == "F":
            sx += wx * value
            sy += wy * value
        else:
            raise ValueError(f"Unknown action {action}")

    return abs(sx) + abs(sy)


if __name__ == "__main__":
    instructions = read_input_file()
    p1 = part_one(instructions)
    print("Part 1:", p1)
    p2 = part_two(instructions)
    print("Part 2:", p2)
