# Day 5: Hydrothermal Venture

from collections import Counter
from pathlib import Path
from typing import List, Tuple


def read_input_file(filepath: str = "input.txt") -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Read line segments from input file.
    Returns a list of lines as ((x1, y1), (x2, y2)) tuples.
    """
    lines: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    for line in Path(filepath).read_text().strip().splitlines():
        start_str, end_str = line.split(" -> ")
        x1, y1 = map(int, start_str.split(","))
        x2, y2 = map(int, end_str.split(","))
        lines.append(((x1, y1), (x2, y2)))
    return lines


def points_on_line(start: Tuple[int, int], end: Tuple[int, int], include_diagonal: bool = False) -> List[Tuple[int, int]]:
    """
    Return all points (x, y) covered by a line.
    Only horizontal/vertical lines if include_diagonal=False.
    """
    x1, y1 = start
    x2, y2 = end

    if x1 == x2:  # vertical line
        step = 1 if y2 >= y1 else -1
        return [(x1, y) for y in range(y1, y2 + step, step)]
    elif y1 == y2:  # horizontal line
        step = 1 if x2 >= x1 else -1
        return [(x, y1) for x in range(x1, x2 + step, step)]
    elif include_diagonal and abs(x2 - x1) == abs(y2 - y1):  # diagonal 45°
        x_step = 1 if x2 > x1 else -1
        y_step = 1 if y2 > y1 else -1
        return [(x1 + i * x_step, y1 + i * y_step) for i in range(abs(x2 - x1) + 1)]
    else:
        return []


def count_overlaps(lines: List[Tuple[Tuple[int, int], Tuple[int, int]]], include_diagonal: bool = False) -> int:
    """
    Count points where at least two lines overlap.
    """
    counter: Counter[Tuple[int, int]] = Counter()
    for start, end in lines:
        for point in points_on_line(start, end, include_diagonal):
            counter[point] += 1
    return sum(1 for count in counter.values() if count >= 2)


if __name__ == "__main__":
    lines = read_input_file()
    print(f"Part 1: {count_overlaps(lines, include_diagonal=False)}")
    print(f"Part 2: {count_overlaps(lines, include_diagonal=True)}")
