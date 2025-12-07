"""
Advent of Code 2025
Day 7: Laboratories
https://adventofcode.com/2025/day/7
"""
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """Reads input text file and converts it into a 2D grid (list of lists of characters)."""
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    return [list(l) for l in lines]


def part_one_and_two(manifold):
    """
    Simulates tachyon beams traveling through the tachyon manifold,
    tracking splits and final beam counts.
    """
    beam_counts = [c == 'S' for c in manifold[0]]
    splits = 0

    # splitters appear on every second line
    splitters = manifold[2::2]

    for row in splitters:
        beam_positions = [x for x, beams in enumerate(beam_counts) if beams > 0]
        for x in beam_positions:
            if row[x] == '^':
                splits += 1
                beams = beam_counts[x]
                # tachyon beam splits left (x - 1) and right (x + 1)
                beam_counts[x-1] += beams
                beam_counts[x+1] += beams
                beam_counts[x] = 0

    return splits, sum(beam_counts)


if __name__ == "__main__":
    tachyon_manifold = read_input_file()
    p1, p2 = part_one_and_two(tachyon_manifold)
    print("Part 1:", p1)
    print("Part 2:", p2)
