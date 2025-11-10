# Day 12: Hill Climbing Algorithm

from collections import deque
from pathlib import Path
from typing import List, Tuple, Optional


def read_input_file(filepath: str = "input.txt") -> Tuple[List[List[str]], complex, complex]:
    """Read and parse the grid from input, returning (grid, start, end)."""
    lines = Path(filepath).read_text().strip().splitlines()
    grid: List[List[str]] = []
    start = end = 0j

    for y, line in enumerate(lines):
        row = list(line.strip())
        if "S" in row:
            start = complex(row.index("S"), y)
        if "E" in row:
            end = complex(row.index("E"), y)
        grid.append(row)

    grid[int(start.imag)][int(start.real)] = "a"
    grid[int(end.imag)][int(end.real)] = "z"
    return grid, start, end


def bfs_shortest_path(grid: List[List[str]], start: complex, end: complex) -> Optional[int]:
    """Perform BFS to find the shortest path from start to end within elevation constraints."""
    height, width = len(grid), len(grid[0])
    visited = {start: 0}
    queue = deque([start])
    directions = [1, -1, 1j, -1j]  # Right, Left, Down, Up

    while queue:
        pos = queue.popleft()
        steps = visited[pos]

        for d in directions:
            nxt = pos + d
            x, y = int(nxt.real), int(nxt.imag)

            # Bounds check
            if not (0 <= x < width and 0 <= y < height):
                continue
            if nxt in visited:
                continue

            # Elevation rule: can move if next is at most +1 higher
            if ord(grid[y][x]) - ord(grid[int(pos.imag)][int(pos.real)]) <= 1:
                visited[nxt] = steps + 1
                if nxt == end:
                    return steps + 1
                queue.append(nxt)

    return None


def part_one(grid: List[List[str]], start: complex, end: complex) -> int:
    """Find shortest path from S to E."""
    return bfs_shortest_path(grid, start, end) or -1


def part_two(grid: List[List[str]], end: complex) -> int:
    """Find shortest path from any 'a' to E."""
    possible_starts = [
        complex(x, y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell == "a"
    ]

    distances = [bfs_shortest_path(grid, start, end) for start in possible_starts]
    valid_distances = [d for d in distances if d is not None]

    return min(valid_distances) if valid_distances else -1


if __name__ == "__main__":
    grid, start, end = read_input_file()
    print("Part 1:", part_one(grid, start, end))
    print("Part 2:", part_two(grid, end))
