# Day 2: Dive!
from pathlib import Path
from typing import List, Tuple


def read_input_file(filepath: str = "input.txt") -> List[Tuple[str, int]]:
    """Read commands from a file as a list of (direction, value) tuples."""
    commands: List[Tuple[str, int]] = []
    for line in Path(filepath).read_text().strip().splitlines():
        direction, value_str = line.split()
        commands.append((direction, int(value_str)))
    return commands


def part_one(commands: List[Tuple[str, int]]) -> int:
    """Compute final horizontal position multiplied by depth (Part 1 rules)."""
    horizontal = 0
    depth = 0

    for direction, value in commands:
        match direction:
            case "forward":
                horizontal += value
            case "down":
                depth += value
            case "up":
                depth -= value

    return horizontal * depth


def part_two(commands: List[Tuple[str, int]]) -> int:
    """Compute final horizontal position multiplied by depth with aim (Part 2 rules)."""
    horizontal = 0
    depth = 0
    aim = 0

    for direction, value in commands:
        match direction:
            case "forward":
                horizontal += value
                depth += aim * value
            case "down":
                aim += value
            case "up":
                aim -= value

    return horizontal * depth


if __name__ == "__main__":
    commands = read_input_file()
    print(f"Part 1: {part_one(commands)}")
    print(f"Part 2: {part_two(commands)}")
