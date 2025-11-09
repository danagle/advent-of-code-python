# Day 20: Trench Map

from functools import cache
from pathlib import Path
from typing import Set, Tuple


def read_input_file(filepath: str = "input.txt") -> Tuple[dict[str, bool], Set[complex]]:
    """Parse the input into the enhancement algorithm and the initial set of lit pixels."""
    raw_algorithm, raw_image = Path(filepath).read_text().strip().split("\n\n")

    # Map 9-bit binary patterns to True (lit) or False (dark)
    enhancement_algorithm = {f"{i:09b}": (char == "#") for i, char in enumerate(raw_algorithm)}

    # Represent lit pixels as complex coordinates (row + col*j)
    lit_pixels = {
        complex(row, col)
        for row, line in enumerate(raw_image.splitlines())
        for col, ch in enumerate(line)
        if ch == "#"
    }

    return enhancement_algorithm, lit_pixels


@cache
def neighbors(pixel: complex) -> Tuple[complex, ...]:
    """Return the 3x3 neighborhood around a pixel in reading order."""
    return tuple(pixel + complex(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1))


def count_lit_pixels(lit_pixels: Set[complex], enhancement_algorithm: dict[str, bool], steps: int) -> int:
    """Apply the enhancement algorithm to the image for the given number of steps."""
    # Detect if the infinite background flips each iteration
    background_flips = enhancement_algorithm["000000000"] and not enhancement_algorithm["111111111"]

    bool_to_bit = {True: "1", False: "0"}

    current_pixels = lit_pixels
    candidate_region = lit_pixels

    for step in range(steps):
        previous_pixels = current_pixels

        # Expand the region to include all pixels that could change this round
        candidate_region = set().union(*(neighbors(pixel) for pixel in candidate_region)) - previous_pixels
        current_pixels = current_pixels | candidate_region

        # Handle toggling background state
        if background_flips and step % 2:
            is_lit = lambda p: (p not in previous_pixels) or (p in lit_pixels)
        else:
            is_lit = lambda p: p in lit_pixels

        # Compute new lit pixels
        lit_pixels = {
            pixel
            for pixel in current_pixels
            if enhancement_algorithm["".join(bool_to_bit[is_lit(n)] for n in neighbors(pixel))]
        }

    return len(lit_pixels)


if __name__ == "__main__":
    enhancement_algorithm, lit_pixels = read_input_file()

    p1 = count_lit_pixels(lit_pixels, enhancement_algorithm, 2)
    print("Part 1:", p1)

    p2 = count_lit_pixels(lit_pixels, enhancement_algorithm, 50)
    print("Part 2:", p2)
