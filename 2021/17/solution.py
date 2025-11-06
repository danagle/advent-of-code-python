# Day 17: Trick Shot

from pathlib import Path
from typing import Tuple, Set


def read_input_file(filepath: str = "input.txt") -> Tuple[int, int, int, int]:
    """
    Reads the target area from the input file.
    
    Returns:
        Tuple of (x_min, x_max, y_min, y_max)
    """
    line = Path(filepath).read_text().strip()
    # Example: target area: x=20..30, y=-10..-5
    parts = line.replace("target area: ", "").split(", ")
    x_min, x_max = map(int, parts[0][2:].split(".."))
    y_min, y_max = map(int, parts[1][2:].split(".."))
    return x_min, x_max, y_min, y_max


def simulate_probe(vx: int, vy: int, target: Tuple[int, int, int, int]) -> bool:
    """
    Simulate the probe trajectory with initial velocity (vx, vy).
    
    Returns True if the probe reaches the target area.
    """
    x, y = 0, 0
    x_min, x_max, y_min, y_max = target
    while x <= x_max and y >= y_min:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
        x += vx
        y += vy
        vx = max(0, vx - 1)
        vy -= 1
    return False


def part_one(target: Tuple[int, int, int, int]) -> int:
    """
    Finds the highest y position for any initial velocity that hits the target.
    """
    _, _, y_min, _ = target
    # Optimal vy is -y_min - 1
    return (-y_min - 1) * (-y_min) // 2


def part_two(target: Tuple[int, int, int, int]) -> int:
    """
    Counts all initial velocity pairs (vx, vy) that hit the target area.
    """
    x_min, x_max, y_min, y_max = target
    valid_velocities: Set[Tuple[int, int]] = set()

    for vx in range(0, x_max + 1):
        for vy in range(y_min, -y_min + 1):
            if simulate_probe(vx, vy, target):
                valid_velocities.add((vx, vy))

    return len(valid_velocities)


if __name__ == "__main__":
    target = read_input_file()
    print(f"Part 1: {part_one(target)}")
    print(f"Part 2: {part_two(target)}")
