# Day 13: Transparent Origami

from pathlib import Path
from typing import List, Tuple, Set


def read_input_file(filepath: str = "input.txt") -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    """
    Reads the input file and returns a set of dots and a list of fold instructions.
    - Dots are represented as (x, y) coordinates.
    - Folds are tuples of ('x' or 'y', position).
    """
    dots: Set[Tuple[int, int]] = set()
    folds: List[Tuple[str, int]] = []

    for line in Path(filepath).read_text().strip().splitlines():
        if not line:
            continue
        if line.startswith("fold along"):
            axis, value = line.split()[-1].split("=")
            folds.append((axis, int(value)))
        else:
            x_str, y_str = line.split(",")
            dots.add((int(x_str), int(y_str)))

    return dots, folds


def fold_dots(dots: Set[Tuple[int, int]], axis: str, pos: int) -> Set[Tuple[int, int]]:
    """
    Fold the set of dots along the given axis and position.
    """
    new_dots: Set[Tuple[int, int]] = set()
    for x, y in dots:
        if axis == "x" and x > pos:
            x = pos - (x - pos)
        elif axis == "y" and y > pos:
            y = pos - (y - pos)
        new_dots.add((x, y))
    return new_dots


def part_one(dots: Set[Tuple[int, int]], folds: List[Tuple[str, int]]) -> int:
    """
    Perform the first fold and return the number of dots visible.
    """
    axis, pos = folds[0]
    return len(fold_dots(dots, axis, pos))


def part_two(dots: Set[Tuple[int, int]], folds: List[Tuple[str, int]]) -> List[str]:
    """
    Perform all folds and return the resulting pattern as a list of strings.
    """
    for axis, pos in folds:
        dots = fold_dots(dots, axis, pos)

    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    grid: List[str] = []

    for y in range(max_y + 1):
        row = "".join("#" if (x, y) in dots else " " for x in range(max_x + 1))
        grid.append(row)

    return grid


if __name__ == "__main__":
    dots, folds = read_input_file()
    print(f"Part 1: {part_one(dots, folds)}")
    print("Part 2:")
    for line in part_two(dots, folds):
        print(line)
