# Day 9: Rope Bridge

from pathlib import Path


def read_input_file(filepath: str = "input.txt") -> list[tuple[str, int]]:
    """Parse the input file into a list of (direction, distance) tuples."""
    motions = []
    for line in Path(filepath).read_text().strip().splitlines():
        direction, distance = line.split()
        motions.append((direction, int(distance)))
    return motions


def follow(head: complex, tail: complex) -> complex:
    """Move the tail toward the head if needed, maintaining rope adjacency."""
    diff = head - tail
    dx, dy = diff.real, diff.imag

    if abs(dx) > 1 and dy == 0 or abs(dy) > 1 and dx == 0:
        # Straight line move
        tail += complex(dx // 2, dy // 2)
    elif abs(dx) > 1 or abs(dy) > 1:
        # Diagonal move
        tail += complex((1 if dx > 0 else -1), (1 if dy > 0 else -1))
    return tail


def part_one(motions: list[tuple[str, int]]) -> int:
    """Simulate a 2-knot rope and count unique tail positions."""
    head = tail = 0 + 0j
    visited = {tail}
    deltas = {"R": 1, "L": -1, "U": 1j, "D": -1j}

    for direction, distance in motions:
        delta = deltas[direction]
        for _ in range(distance):
            head += delta
            tail = follow(head, tail)
            visited.add(tail)
    return len(visited)


def part_two(motions: list[tuple[str, int]]) -> int:
    """Simulate a 10-knot rope and count unique tail positions."""
    rope = [0 + 0j for _ in range(10)]
    visited = {rope[-1]}
    deltas = {"R": 1, "L": -1, "U": 1j, "D": -1j}

    for direction, distance in motions:
        delta = deltas[direction]
        for _ in range(distance):
            rope[0] += delta
            for i in range(1, len(rope)):
                rope[i] = follow(rope[i - 1], rope[i])
            visited.add(rope[-1])
    return len(visited)


if __name__ == "__main__":
    motions = read_input_file()
    print("Part 1:", part_one(motions))
    print("Part 2:", part_two(motions))
