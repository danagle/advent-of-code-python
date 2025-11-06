# Day 15: Chiton

import heapq
from pathlib import Path
from typing import List, Tuple, Dict


def read_input_file(filepath: str = "input.txt") -> List[List[int]]:
    """
    Reads the input file and returns a 2D grid of risk levels.
    """
    return [
        [int(char) for char in line.strip()]
        for line in Path(filepath).read_text().strip().splitlines()
    ]


def dijkstra(grid: List[List[int]]) -> int:
    """
    Compute the lowest total risk from the top-left to bottom-right using Dijkstra's algorithm.
    """
    rows, cols = len(grid), len(grid[0])
    start, end = (0, 0), (rows - 1, cols - 1)
    
    heap: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    visited: Dict[Tuple[int, int], int] = {}

    while heap:
        risk, (x, y) = heapq.heappop(heap)
        if (x, y) in visited:
            continue
        visited[(x, y)] = risk

        if (x, y) == end:
            return risk

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                heapq.heappush(heap, (risk + grid[nx][ny], (nx, ny)))

    raise ValueError("No path found")


def expand_grid(grid: List[List[int]], times: int = 5) -> List[List[int]]:
    """
    Expand the grid according to Part 2 rules: tile it times x times,
    incrementing risk levels and wrapping at 9.
    """
    original_rows, original_cols = len(grid), len(grid[0])
    new_rows, new_cols = original_rows * times, original_cols * times
    expanded: List[List[int]] = [[0] * new_cols for _ in range(new_rows)]

    for i in range(new_rows):
        for j in range(new_cols):
            add_risk = i // original_rows + j // original_cols
            expanded[i][j] = (grid[i % original_rows][j % original_cols] + add_risk - 1) % 9 + 1

    return expanded


if __name__ == "__main__":
    grid = read_input_file()
    
    # Part 1: original grid
    print(f"Part 1: {dijkstra(grid)}")
    
    # Part 2: expanded grid
    expanded = expand_grid(grid)
    print(f"Part 2: {dijkstra(expanded)}")
