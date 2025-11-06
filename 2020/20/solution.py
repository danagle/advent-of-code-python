"""
Advent of Code 2020
Day 20: Jurassic Jigsaw
https://adventofcode.com/2020/day/20
"""
from __future__ import annotations
from math import isqrt
from pathlib import Path
from typing import Dict, List, Tuple, Iterator, Optional

TileGrid = List[str]
Position = Tuple[int, int]


def read_input_file(filepath: str = "input.txt") -> Dict[int, TileGrid]:
    """Parse the input file into {tile_id: tile_grid}."""
    sections = Path(filepath).read_text().strip().split("\n\n")
    tiles: Dict[int, TileGrid] = {}
    for section in sections:
        header, *body = section.splitlines()
        tile_id = int(header.removeprefix("Tile ").removesuffix(":"))
        tiles[tile_id] = body
    return tiles


def rotate(grid: TileGrid) -> TileGrid:
    """Rotate grid 90° clockwise."""
    return ["".join(row[i] for row in reversed(grid)) for i in range(len(grid[0]))]


def flip(grid: TileGrid) -> TileGrid:
    """Flip grid horizontally."""
    return [row[::-1] for row in grid]


def orientations(grid: TileGrid) -> Iterator[TileGrid]:
    """Generate all 8 orientations (4 rotations * flip)."""
    g = grid
    for _ in range(2):  # flip states
        for _ in range(4):  # rotations
            yield g
            g = rotate(g)
        g = flip(grid)


def edges(grid: TileGrid) -> Tuple[str, str, str, str]:
    """Return (top, right, bottom, left) edges of a grid."""
    top = grid[0]
    bottom = grid[-1]
    left = "".join(row[0] for row in grid)
    right = "".join(row[-1] for row in grid)
    return top, right, bottom, left


def assemble_grid(tiles: Dict[int, TileGrid]) -> Dict[Position, Tuple[int, TileGrid]]:
    """
    Assemble tiles into a dense NxN grid using backtracking.
    Returns mapping {(x, y): (tile_id, oriented_grid)} with (0,0) top-left.
    """
    n_tiles = len(tiles)
    side = int(isqrt(n_tiles))
    if side * side != n_tiles:
        raise ValueError("Number of tiles is not a perfect square.")

    tile_ids = list(tiles.keys())
    used: Dict[int, TileGrid] = {}
    placed: Dict[Position, Tuple[int, TileGrid]] = {}

    def fits(x: int, y: int, candidate: TileGrid) -> bool:
        """Check top and left neighbor edges if present."""
        top_c, _, _, left_c = edges(candidate)
        # check top neighbor
        if y > 0:
            neighbor = placed.get((x, y - 1))
            if neighbor is None:
                return False
            _, neighbor_grid = neighbor
            _, _, neighbor_bottom, _ = edges(neighbor_grid)
            if neighbor_bottom != top_c:
                return False
        # check left neighbor
        if x > 0:
            neighbor = placed.get((x - 1, y))
            if neighbor is None:
                return False
            _, neighbor_grid = neighbor
            _, neighbor_right, _, _ = edges(neighbor_grid)
            if neighbor_right != left_c:
                return False
        return True

    positions = [(x, y) for y in range(side) for x in range(side)]

    def backtrack(idx: int) -> bool:
        if idx == len(positions):
            return True
        x, y = positions[idx]
        for tid in tile_ids:
            if tid in used:
                continue
            for orient in orientations(tiles[tid]):
                if fits(x, y, orient):
                    placed[(x, y)] = (tid, orient)
                    used[tid] = orient
                    if backtrack(idx + 1):
                        return True
                    # undo
                    del placed[(x, y)]
                    del used[tid]
        return False

    # Start: try every tile in every orientation at (0,0)
    for tid in tile_ids:
        for orient in orientations(tiles[tid]):
            placed.clear()
            used.clear()
            placed[(0, 0)] = (tid, orient)
            used[tid] = orient
            if backtrack(1):
                # placed is filled
                return dict(placed)


def remove_borders(grid: TileGrid) -> TileGrid:
    """Remove outermost border rows and columns."""
    return [row[1:-1] for row in grid[1:-1]]


def stitch_image(placed: Dict[Position, Tuple[int, TileGrid]]) -> TileGrid:
    """Combine placed tiles (without borders) into one large image.
    Assumes placed keys form a dense rectangle starting from (0,0)."""
    xs = [x for x, _ in placed]
    ys = [y for _, y in placed]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    tile_size = len(next(iter(placed.values()))[1]) - 2  # minus borders
    rows: List[str] = []

    for y in range(min_y, max_y + 1):
        tile_row_blocks: List[List[str]] = []
        for x in range(min_x, max_x + 1):
            _, tile = placed[(x, y)]
            tile_row_blocks.append(remove_borders(tile))
        for i in range(tile_size):
            rows.append("".join(block[i] for block in tile_row_blocks))
    return rows


SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


def count_hashes(grid: TileGrid) -> int:
    return sum(row.count("#") for row in grid)


def find_sea_monsters(grid: TileGrid) -> int:
    """Return number of sea monsters found in the grid."""
    monster_coords = [
        (dx, dy)
        for dy, row in enumerate(SEA_MONSTER)
        for dx, c in enumerate(row)
        if c == "#"
    ]
    height, width = len(grid), len(grid[0])
    m_height, m_width = len(SEA_MONSTER), len(SEA_MONSTER[0])
    count = 0

    for y in range(height - m_height + 1):
        for x in range(width - m_width + 1):
            if all(grid[y + dy][x + dx] == "#" for dx, dy in monster_coords):
                count += 1
    return count


def roughness(image: TileGrid) -> int:
    """Compute water roughness (hashes not part of any sea monster)."""
    monster_hashes = sum(row.count("#") for row in SEA_MONSTER)
    for orient in orientations(image):
        monsters = find_sea_monsters(orient)
        if monsters:
            return count_hashes(orient) - monsters * monster_hashes
    return count_hashes(image)


def main(filepath: str = "input.txt") -> None:
    tiles = read_input_file(filepath)
    placed = assemble_grid(tiles)

    # Compute corner IDs (top-left, top-right, bottom-left, bottom-right)
    xs = [x for x, _ in placed]
    ys = [y for _, y in placed]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    corners = [
        placed[(min_x, min_y)][0],
        placed[(max_x, min_y)][0],
        placed[(min_x, max_y)][0],
        placed[(max_x, max_y)][0],
    ]
    part1 = 1
    for cid in corners:
        part1 *= cid

    image = stitch_image(placed)
    part2 = roughness(image)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
