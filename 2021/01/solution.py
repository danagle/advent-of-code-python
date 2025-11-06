from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[int]:
    """Read depth measurements from a file."""
    return [int(line) for line in Path(filepath).read_text().strip().splitlines()]


def count_increases(depths: List[int]) -> int:
    """Count how many times a depth measurement increases from the previous one."""
    return sum(curr > prev for prev, curr in zip(depths, depths[1:]))


def count_window_increases(depths: List[int], window_size: int = 3) -> int:
    """Count increases in the sum of sliding windows of a given size."""
    return sum(
        sum(depths[i+1:i+1+window_size]) > sum(depths[i:i+window_size])
        for i in range(len(depths) - window_size)
    )


if __name__ == "__main__":
    depths = read_input_file()
    print(f"Part 1: {count_increases(depths)}")
    print(f"Part 2: {count_window_increases(depths)}")
