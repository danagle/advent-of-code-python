# Day 24: Arithmetic Logic Unit

from pathlib import Path
from typing import List, Dict, Tuple


def read_input_file(filepath: str = "input.txt") -> List[List[str]]:
    """
    Parse the input file into chunks corresponding to each 'inp w' instruction block.
    Returns a list of instruction blocks (lists of strings).
    """
    content = Path(filepath).read_text().strip()
    blocks = content.split("inp w")[1:]  # Skip the first empty split
    return [block.strip().splitlines() for block in blocks]


def build_constraints(blocks: List[List[str]]) -> Dict[Tuple[int, int], Tuple[int, int]]:
    """
    Analyze the instruction blocks to determine the dependencies between digits.
    Returns a mapping of (current_idx, p2) -> (previous_idx, p3).
    """
    stack = []
    mapping = {}

    for idx, block in enumerate(blocks):
        # Extract parameters p1, p2, p3 from fixed lines
        p1: int = int(block[3].split()[2])
        p2: int = int(block[4].split()[2])
        p3: int = int(block[14].split()[2])

        if p1 == 1:
            stack.append((idx, p3))
        elif p1 == 26:
            mapping[(idx, p2)] = stack.pop()
        else:
            raise ValueError(f"Unexpected p1 value: {p1}")

    return mapping


def solve_monad(mapping: Dict[Tuple[int, int], Tuple[int, int]],
                maximize: bool = True,
                num_blocks: int = 14) -> str:
    """
    Solve the ALU problem using the mapping of constraints.
    `maximize=True` for part 1, `False` for part 2.
    """
    digits = [9 if maximize else 1] * num_blocks

    for (current_idx, p2), (prev_idx, p3) in mapping.items():
        delta = p3 + p2
        if maximize:
            if delta < 0:
                digits[current_idx] = 9 + delta
            else:
                digits[prev_idx] = 9 - delta
        else:
            if delta < 0:
                digits[prev_idx] = 1 - delta
            else:
                digits[current_idx] = 1 + delta

    return "".join(map(str, digits))


def part_one(blocks: List[List[str]]) -> str:
    mapping = build_constraints(blocks)
    return solve_monad(mapping, maximize=True, num_blocks=len(blocks))


def part_two(blocks: List[List[str]]) -> str:
    mapping = build_constraints(blocks)
    return solve_monad(mapping, maximize=False, num_blocks=len(blocks))


if __name__ == "__main__":
    blocks = read_input_file()
    p1 = part_one(blocks)
    print("Part 1:", p1)
    p2 = part_two(blocks)
    print("Part 2:", p2)
