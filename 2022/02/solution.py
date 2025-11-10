# Day 2: Rock Paper Scissors

from pathlib import Path
from typing import List, Tuple

# Type alias for clarity
Round = Tuple[str, str]


def read_input_file(filepath: str = "input.txt") -> List[Round]:
    """
    Reads the input file and returns a list of (opponent, player) symbol pairs.
    Each line contains two letters, e.g., "A Y".
    """
    lines = Path(filepath).read_text().strip().splitlines()
    return [tuple(line.split()) for line in lines]


# Mappings for part one interpretation
MOVE_SCORES = {"X": 1, "Y": 2, "Z": 3}
OUTCOME_SCORES = {
    ("A", "X"): 3,  # Rock vs Rock = Draw
    ("A", "Y"): 6,  # Rock vs Paper = Win
    ("A", "Z"): 0,  # Rock vs Scissors = Lose
    ("B", "X"): 0,  # Paper vs Rock = Lose
    ("B", "Y"): 3,  # Paper vs Paper = Draw
    ("B", "Z"): 6,  # Paper vs Scissors = Win
    ("C", "X"): 6,  # Scissors vs Rock = Win
    ("C", "Y"): 0,  # Scissors vs Paper = Lose
    ("C", "Z"): 3,  # Scissors vs Scissors = Draw
}


def part_one(rounds: List[Round]) -> int:
    """
    Computes the total score according to the direct move interpretation.
    """
    total = 0
    for opp, me in rounds:
        total += MOVE_SCORES[me] + OUTCOME_SCORES[(opp, me)]
    return total


# Part two mappings (player letter means desired outcome)
OUTCOME_TARGET = {"X": 0, "Y": 3, "Z": 6}
CHOOSE_MOVE = {
    ("A", 0): "Z",  # Rock -> must lose -> play Scissors
    ("A", 3): "X",  # Rock -> draw -> play Rock
    ("A", 6): "Y",  # Rock -> win -> play Paper
    ("B", 0): "X",  # Paper -> lose -> Rock
    ("B", 3): "Y",  # Paper -> draw -> Paper
    ("B", 6): "Z",  # Paper -> win -> Scissors
    ("C", 0): "Y",  # Scissors -> lose -> Paper
    ("C", 3): "Z",  # Scissors -> draw -> Scissors
    ("C", 6): "X",  # Scissors -> win -> Rock
}


def part_two(rounds: List[Round]) -> int:
    """
    Computes the total score where the second column means desired outcome (X=lose, Y=draw, Z=win).
    """
    total = 0
    for opp, outcome_letter in rounds:
        outcome_score = OUTCOME_TARGET[outcome_letter]
        my_move = CHOOSE_MOVE[(opp, outcome_score)]
        total += outcome_score + MOVE_SCORES[my_move]
    return total


def main() -> None:
    rounds = read_input_file()
    print("Part 1:", part_one(rounds))
    print("Part 2:", part_two(rounds))


if __name__ == "__main__":
    main()
