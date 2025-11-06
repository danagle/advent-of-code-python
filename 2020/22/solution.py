"""
Advent of Code 2020
Day 22: Crab Combat
https://adventofcode.com/2020/day/22
"""
from __future__ import annotations
from collections import deque
from pathlib import Path
from typing import Deque, List, Set, Tuple


Deck = Deque[int]


def read_input_file(filepath: str = "input.txt") -> Tuple[Deck, Deck]:
    """Parse the input file into two decks."""
    sections = Path(filepath).read_text().strip().split("\n\n")
    deck1_lines = sections[0].splitlines()[1:]
    deck2_lines = sections[1].splitlines()[1:]
    return deque(map(int, deck1_lines)), deque(map(int, deck2_lines))


def play_combat(deck1: Deck, deck2: Deck) -> Deck:
    """Simulate the simple combat game and return the winning deck."""
    deck1, deck2 = deque(deck1), deque(deck2)  # work on copies
    while deck1 and deck2:
        c1, c2 = deck1.popleft(), deck2.popleft()
        if c1 > c2:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])
    return deck1 if deck1 else deck2


def score(deck: Deck) -> int:
    """Compute final score from bottom card (position 1) upwards."""
    return sum(mult * card for mult, card in enumerate(reversed(deck), start=1))


def play_recursive_combat(deck1: Deck, deck2: Deck) -> Tuple[int, Deck]:
    """
    Play a game of recursive combat.
    Returns (winner_id, winning_deck) where winner_id is 1 or 2.
    """
    deck1, deck2 = deque(deck1), deque(deck2)
    previous_rounds: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]] = set()

    while deck1 and deck2:
        config = (tuple(deck1), tuple(deck2))
        if config in previous_rounds:
            # Prevent infinite loops — player 1 wins instantly
            return 1, deck1
        previous_rounds.add(config)

        c1, c2 = deck1.popleft(), deck2.popleft()

        if len(deck1) >= c1 and len(deck2) >= c2:
            # Recurse with copies of the next c1 / c2 cards
            winner, _ = play_recursive_combat(
                deque(list(deck1)[:c1]),
                deque(list(deck2)[:c2]),
            )
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])

    return (1, deck1) if deck1 else (2, deck2)


def main(filepath: str = "input.txt") -> None:
    deck1, deck2 = read_input_file(filepath)

    # Part 1
    winner_deck = play_combat(deck1, deck2)
    print(f"Part 1: {score(winner_deck)}")

    # Part 2
    _, recursive_winner_deck = play_recursive_combat(deck1, deck2)
    print(f"Part 2: {score(recursive_winner_deck)}")


if __name__ == "__main__":
    main()
