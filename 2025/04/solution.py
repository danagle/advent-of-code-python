"""
Advent of Code 2025
Day 4: Printing Department
https://adventofcode.com/2025/day/4
"""
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """
    Reads the input file as a string of text.
    Determines the line length and indexes of all rolls '@' in the string.
    """
    text = Path(filepath).read_text(encoding="utf-8")
    width = text.index('\n') + 1
    indexes = {i for i, c in enumerate(text) if c == '@'}
    return indexes, width


def can_be_removed(indexes, width, i):
    """A roll can be removed if it has less than 4 rolls adjacent to it."""
    return len(indexes.intersection({i-width-1, i-width, i-width+1, i-1, i+1, i+width-1, i+width, i+width+1})) < 4


def part_one(roll_indexes, diagram_width):
    """Get number of rolls of paper that can be removed by a forklift."""
    return sum(can_be_removed(roll_indexes, diagram_width, i) for i in roll_indexes)


def part_two(roll_indexes, diagram_width):
    """Remove rolls of paper that are accessible by a forklift."""
    rolls_removed = 0

    while True:
        some_removed = False
        for i in list(roll_indexes):
            if can_be_removed(roll_indexes, diagram_width, i):
                roll_indexes.discard(i)
                rolls_removed += 1
                some_removed = True
        if not some_removed:
            break

    return rolls_removed


if __name__ == "__main__":
    diagram_rolls, line_width = read_input_file()
    print("part 1:", part_one(diagram_rolls, line_width))
    print("part 2:", part_two(diagram_rolls, line_width))
