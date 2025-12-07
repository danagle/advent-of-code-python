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
    beams = {manifold[0].index('S'): 1}
    splits = 0

    for row in manifold[1:]:
        beam_copy = [(position, beam_count) for position, beam_count in beams.items()]
        for position, beam_count in beam_copy:
            if row[position] == '^':
                splits += 1
                # tachyon beam splits left (position - 1) and right (position + 1)
                for side in [position - 1, position + 1]:
                    if side in beams:
                        beams[side] += beam_count
                    else:
                        beams[side] = beam_count

                beams.pop(position)

    return splits, sum(beams.values())


if __name__ == "__main__":
    tachyon_manifold = read_input_file()
    p1, p2 = part_one_and_two(tachyon_manifold)
    print("Part 1:", p1)
    print("Part 2:", p2)
