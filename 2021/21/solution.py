# Day 21: Dirac Dice

from functools import cache
from itertools import product
from pathlib import Path
import re

def read_input_file(filepath: str = "input.txt") -> list[int, int]:
    """Extract starting position values from the input file."""
    text = Path(filepath).read_text()
    return list(map(int, re.findall(r'starting position:\s*(\d+)', text)))


def part_one(start_positions):
    """Simulate the deterministic dice game and return the result."""
    positions = start_positions[:]  # [p1_pos, p2_pos]
    scores = [0, 0]
    die_value = 1
    rolls = 0
    player = 1  # start with player 2 after xor flip in loop

    def roll() -> int:
        nonlocal die_value, rolls
        value = die_value
        die_value = die_value % 100 + 1
        rolls += 1
        return value

    while True:
        # Switch active player (xor toggle 0 ↔ 1)
        player ^= 1

        # Each turn: roll three times and move forward the total amount
        move = roll() + roll() + roll()
        positions[player] = (positions[player] + move - 1) % 10 + 1
        scores[player] += positions[player]

        # Check for win condition
        if scores[player] >= 1000:
            losing_score = scores[1 - player]
            return rolls * losing_score


def part_two(start_positions: list[int]) -> int:
    """Simulate the quantum Dirac dice game and return the max number of wins."""

    # Precompute all possible sums of three 3-sided dice (27 combinations)
    roll_sums = [sum(roll) for roll in product([1, 2, 3], repeat=3)]

    @cache
    def count_wins(pos_a: int, pos_b: int, score_a: int = 0, score_b: int = 0) -> tuple[int, int]:
        """
        Returns (wins_for_player_a, wins_for_player_b) for the given state of the game.
        """
        wins_a, wins_b = 0, 0

        for roll_total in roll_sums:
            new_pos_a = (pos_a + roll_total - 1) % 10 + 1
            new_score_a = score_a + new_pos_a

            # If player A reaches 21, that universe ends with A winning
            if new_score_a >= 21:
                wins_a += 1
            else:
                # Otherwise, it's now player B's turn — swap perspectives
                sub_b_wins, sub_a_wins = count_wins(pos_b, new_pos_a, score_b, new_score_a)
                wins_a += sub_a_wins
                wins_b += sub_b_wins

        return wins_a, wins_b

    # Return the maximum number of wins between the two players
    return max(count_wins(*start_positions))


if __name__ == "__main__":
    start_positions = read_input_file()
    
    p1 = part_one(start_positions)
    print("Part 1:", p1)
    
    p2 = part_two(start_positions)
    print("Part 2:", p2)
