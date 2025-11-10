# Day 6: Tuning Trouble

from pathlib import Path


def read_input_file(filepath: str = "input.txt") -> str:
    """
    Reads the input file and returns the datastream buffer as a string.
    """
    return Path(filepath).read_text().strip()


def find_marker(buffer: str, marker_length: int) -> int:
    """
    Finds the first position in the buffer where a sequence of `marker_length`
    distinct characters appears. Returns the index (1-based position) where
    that marker ends.
    """
    for i in range(marker_length, len(buffer) + 1):
        window = buffer[i - marker_length : i]
        if len(set(window)) == marker_length:
            return i
    raise ValueError("No marker found in buffer.")


def part_one(buffer: str) -> int:
    """
    Returns the number of characters processed before the first start-of-packet marker.
    """
    return find_marker(buffer, 4)


def part_two(buffer: str) -> int:
    """
    Returns the number of characters processed before the first start-of-message marker.
    """
    return find_marker(buffer, 14)


if __name__ == "__main__":
    buffer = read_input_file()
    print("Part 1:", part_one(buffer))
    print("Part 2:", part_two(buffer))
