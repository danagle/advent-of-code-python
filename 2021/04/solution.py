# Day 4: Giant Squid

from pathlib import Path
from typing import List, Tuple, Optional


def read_input_file(filepath: str = "input.txt") -> Tuple[List[int], List[List[List[int]]]]:
    """
    Read bingo numbers and boards from input file.
    Returns a tuple of:
      - numbers to draw
      - list of boards (each board is a list of rows, each row is a list of ints)
    """
    lines = Path(filepath).read_text().strip().splitlines()
    numbers = list(map(int, lines[0].split(",")))
    boards: List[List[List[int]]] = []

    current_board: List[List[int]] = []
    for line in lines[1:]:
        if line.strip() == "":
            if current_board:
                boards.append(current_board)
                current_board = []
        else:
            current_board.append([int(x) for x in line.split()])
    if current_board:
        boards.append(current_board)

    return numbers, boards


def mark_number(board: List[List[int]], number: int) -> None:
    """Mark a number on the board by replacing it with None."""
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if val == number:
                row[c] = None


def is_winner(board: List[List[Optional[int]]]) -> bool:
    """Check if the board has a complete row or column of marked numbers (None)."""
    # Check rows
    if any(all(val is None for val in row) for row in board):
        return True
    # Check columns
    for c in range(len(board[0])):
        if all(row[c] is None for row in board):
            return True
    return False


def board_score(board: List[List[Optional[int]]], last_number: int) -> int:
    """Compute score of the board: sum of unmarked numbers * last number drawn."""
    unmarked_sum = sum(val for row in board for val in row if val is not None)
    return unmarked_sum * last_number


def play_bingo(numbers: List[int], boards: List[List[List[int]]], win_last: bool = False) -> int:
    """
    Simulate the bingo game.
    If win_last is False, returns score of first winning board (Part 1).
    If win_last is True, returns score of last winning board (Part 2).
    """
    boards_in_play = boards[:]
    completed_boards: set[int] = set()
    last_score = 0

    for number in numbers:
        for i, board in enumerate(boards_in_play):
            if i in completed_boards:
                continue
            mark_number(board, number)
            if is_winner(board):
                completed_boards.add(i)
                last_score = board_score(board, number)
                if not win_last:
                    return last_score

    return last_score  # for Part 2: last board to win


if __name__ == "__main__":
    numbers, boards = read_input_file()
    print(f"Part 1: {play_bingo(numbers, boards, win_last=False)}")
    print(f"Part 2: {play_bingo(numbers, boards, win_last=True)}")
