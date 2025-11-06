"""
Advent of Code 2020
Day 24: Lobby Layout
https://adventofcode.com/2020/day/24
"""
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


# Hex grid using axial coordinates (q, r)
DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "e":  (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w":  (-1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
}


def parse_directions(line: str) -> List[str]:
    """Parse a line of movement instructions into individual directions."""
    directions: List[str] = []
    i = 0
    while i < len(line):
        if line[i] in {"e", "w"}:
            directions.append(line[i])
            i += 1
        else:
            directions.append(line[i:i+2])
            i += 2
    return directions


def read_input_file(filepath: str = "input.txt") -> List[List[str]]:
    """Read all lines and parse into lists of directions."""
    lines = Path(filepath).read_text().strip().splitlines()
    return [parse_directions(line.strip()) for line in lines]


def get_black_tiles(instructions: List[List[str]]) -> Set[Tuple[int, int]]:
    """Return the set of black tiles after all instructions."""
    black_tiles: Set[Tuple[int, int]] = set()

    for dirs in instructions:
        q, r = 0, 0
        for d in dirs:
            dq, dr = DIRECTIONS[d]
            q, r = q + dq, r + dr

        coord = (q, r)
        if coord in black_tiles:
            black_tiles.remove(coord)
        else:
            black_tiles.add(coord)

    return black_tiles


def neighbors(coord: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    """Generate all 6 adjacent hex coordinates."""
    q, r = coord
    for dq, dr in DIRECTIONS.values():
        yield (q + dq, r + dr)


def step(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Compute the next day's black tiles."""
    new_black: Set[Tuple[int, int]] = set()
    to_consider: Set[Tuple[int, int]] = set(black_tiles)

    # Include all neighbors of black tiles for possible flips
    for tile in black_tiles:
        to_consider.update(neighbors(tile))

    for tile in to_consider:
        black_neighbors = sum((n in black_tiles) for n in neighbors(tile))

        if tile in black_tiles:
            # Black tile rules
            if 1 <= black_neighbors <= 2:
                new_black.add(tile)
        else:
            # White tile rules
            if black_neighbors == 2:
                new_black.add(tile)

    return new_black


def simulate_days(black_tiles: Set[Tuple[int, int]], days: int = 100) -> Set[Tuple[int, int]]:
    """Simulate flipping tiles for a given number of days."""
    for _ in range(days):
        black_tiles = step(black_tiles)
    return black_tiles


def part_one(instructions: List[List[str]]) -> int:
    """Count black tiles after initialization."""
    black_tiles = get_black_tiles(instructions)
    return len(black_tiles)


def part_two(instructions: List[List[str]]) -> int:
    """Count black tiles after 100 days of flipping."""
    black_tiles = get_black_tiles(instructions)
    final = simulate_days(black_tiles, days=100)
    return len(final)


if __name__ == "__main__":
    instructions = read_input_file()
    p1 = part_one(instructions)
    print("Part 1:", p1)
    p2 = part_two(instructions)
    print("Part 2:", p2)
