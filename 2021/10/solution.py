# Day 10: Syntax Scoring

from pathlib import Path
from typing import List, Tuple, Optional


# Maps for bracket pairs and scoring
OPENING = "([{<"
CLOSING = ")]}>"
PAIR = dict(zip(CLOSING, OPENING))
SCORE_CORRUPT = {")": 3, "]": 57, "}": 1197, ">": 25137}
SCORE_INCOMPLETE = {")": 1, "]": 2, "}": 3, ">": 4}


def read_input_file(filepath: str = "input.txt") -> List[str]:
    """
    Read the input lines containing bracket sequences.
    """
    return Path(filepath).read_text().strip().splitlines()


def check_line(line: str) -> Tuple[Optional[str], List[str]]:
    """
    Check a single line for corruption or incomplete brackets.
    Returns a tuple (illegal_character, remaining_stack).
    - illegal_character: the first incorrect closing character, or None if incomplete.
    - remaining_stack: stack of expected closing brackets for incomplete lines.
    """
    stack: List[str] = []
    for c in line:
        if c in OPENING:
            stack.append(c)
        elif c in CLOSING:
            if not stack or stack[-1] != PAIR[c]:
                return c, stack  # Corrupted line
            stack.pop()
    return None, stack  # Incomplete or valid


def part_one(lines: List[str]) -> int:
    """
    Calculate total syntax error score for corrupted lines.
    """
    total_score = 0
    for line in lines:
        illegal, _ = check_line(line)
        if illegal:
            total_score += SCORE_CORRUPT[illegal]
    return total_score


def part_two(lines: List[str]) -> int:
    """
    Calculate the middle score for incomplete lines.
    """
    incomplete_scores: List[int] = []
    for line in lines:
        illegal, stack = check_line(line)
        if illegal:
            continue  # Skip corrupted lines
        score = 0
        for c in reversed(stack):
            # Find the corresponding closing character
            closing = next(k for k, v in PAIR.items() if v == c)
            score = score * 5 + SCORE_INCOMPLETE[closing]
        incomplete_scores.append(score)
    incomplete_scores.sort()
    return incomplete_scores[len(incomplete_scores) // 2]


if __name__ == "__main__":
    lines = read_input_file()
    print(f"Part 1: {part_one(lines)}")
    print(f"Part 2: {part_two(lines)}")
