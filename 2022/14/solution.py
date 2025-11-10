# Day 14: Regolith Reservoir (with complex coordinates)
from pathlib import Path
from typing import List, Dict


def load_input_file(filepath: str = "input.txt") -> List[List[complex]]:
    """Parse the input file into a list of rock paths using complex coordinates."""
    paths = []
    for line in Path(filepath).read_text().strip().splitlines():
        coords = [complex(*map(int, point.split(","))) for point in line.split(" -> ")]
        paths.append(coords)
    return paths


# Movement directions as complex numbers
DOWN = 1j
DIAG_LEFT = -1 + 1j
DIAG_RIGHT = 1 + 1j


def draw_rocks(paths: List[List[complex]]) -> Dict[complex, str]:
    """Convert rock paths into a dictionary of occupied coordinates."""
    particles: Dict[complex, str] = {}
    for path in paths:
        for start, end in zip(path, path[1:]):
            if start.real == end.real:  # vertical line
                step = 1 if end.imag >= start.imag else -1
                for y in range(int(start.imag), int(end.imag) + step, step):
                    particles[complex(start.real, y)] = "#"
            elif start.imag == end.imag:  # horizontal line
                step = 1 if end.real >= start.real else -1
                for x in range(int(start.real), int(end.real) + step, step):
                    particles[complex(x, start.imag)] = "#"
            else:
                raise ValueError(f"Non-axis-aligned rock segment: {start} -> {end}")
    return particles


def simulate_sand(paths: List[List[complex]], has_floor: bool = False) -> int:
    """Simulate sand falling until abyss (part 1) or source blocked (part 2)."""
    particles = draw_rocks(paths)
    source = complex(500, 0)
    max_y = max(int(p.imag) for p in particles)
    count = 0

    while True:
        pos = source
        count += 1
        while True:
            for move in (DOWN, DIAG_LEFT, DIAG_RIGHT):
                next_pos = pos + move
                if next_pos not in particles:
                    pos = next_pos
                    break
            else:  # no available move
                particles[pos] = "o"
                if has_floor and pos == source:
                    return count
                break

            # stop conditions
            if not has_floor and pos.imag > max_y:
                return count - 1
            if has_floor and pos.imag == max_y + 1:
                particles[pos] = "o"
                break


def part_one(paths: List[List[complex]]) -> int:
    return simulate_sand(paths, has_floor=False)


def part_two(paths: List[List[complex]]) -> int:
    return simulate_sand(paths, has_floor=True)


if __name__ == "__main__":
    paths = load_input_file()
    print("Part 1:", part_one(paths))
    print("Part 2:", part_two(paths))
