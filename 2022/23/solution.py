# Day 23: Unstable Diffusion

from collections import defaultdict
from typing import Set, Tuple, Dict, List, Optional

# 8 neighbor offsets
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1),  (1, 0),  (1, 1)]

# Directions in the order North, South, West, East for proposals.
# Each entry is (move_delta, list_of_checks)
# move_delta is the resulting move if that direction is chosen.
# list_of_checks are relative offsets that must all be empty to allow that move.
DIRS = [
    ((-1, 0), [(-1, -1), (-1, 0), (-1, 1)]),  # North
    ((1, 0),  [(1, -1),  (1, 0),  (1, 1)]),   # South
    ((0, -1), [(-1, -1), (0, -1), (1, -1)]),  # West
    ((0, 1),  [(-1, 1),  (0, 1),  (1, 1)]),   # East
]


def read_input_file(filename: str = "input.txt") -> Set[Tuple[int, int]]:
    """Parse input into a set of (r, c) coordinates for elves (#)."""
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    elves = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '#':
                elves.add((r, c))

    return elves


def bounding_area(elves: Set[Tuple[int, int]]) -> int:
    """Return the number of empty ground tiles in the bounding rectangle."""
    if not elves:
        return 0
    rs = [r for r, _ in elves]
    cs = [c for _, c in elves]
    rmin, rmax = min(rs), max(rs)
    cmin, cmax = min(cs), max(cs)
    area = (rmax - rmin + 1) * (cmax - cmin + 1)
    return area - len(elves)


def simulate(elves: Set[Tuple[int, int]], rounds: Optional[int] = None) -> Tuple[Set[Tuple[int, int]], int]:
    """
    Simulate movement.
    - If rounds is an int: perform exactly that many rounds and return (elves_after, rounds_done).
    - If rounds is None: run until a round happens with no movement and return (final_elves, round_index_of_stop).
      round_index_of_stop is 1-based.
    """
    elves = set(elves)  # copy so original set is not mutated
    start_dir = 0  # index into DIRS for the priority in the first round
    round_idx = 0

    while True:
        round_idx += 1
        proposals: Dict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(list)

        # Phase 1: each elf proposes (or not)
        for (r, c) in elves:
            # if there are no neighbors, do not propose
            if all((r + dr, c + dc) not in elves for dr, dc in NEIGHBORS):
                continue

            # try directions in order starting at start_dir
            moved = False
            for k in range(4):
                dir_idx = (start_dir + k) % 4
                move_delta, checks = DIRS[dir_idx]
                if all((r + dr, c + dc) not in elves for dr, dc in checks):
                    # propose
                    nr, nc = r + move_delta[0], c + move_delta[1]
                    proposals[(nr, nc)].append((r, c))
                    moved = True
                    break
            # if no valid direction found -> no proposal

        # Phase 2: resolve proposals
        if not proposals:
            # no one proposed -> no movement this round
            # if we were asked exactly N rounds, this may be earlier than N
            if rounds is None:
                return elves, round_idx  # stopped at this round (1-based)
            else:
                # No proposals but we still need to continue (remaining rounds do nothing)
                start_dir = (start_dir + 1) % 4
                if round_idx >= rounds:
                    return elves, round_idx
                continue

        moved = False
        new_elves = set(elves)
        for target, proposers in proposals.items():
            if len(proposers) == 1:
                # move accepted
                mover = proposers[0]
                new_elves.remove(mover)
                new_elves.add(target)
                moved = True
            # otherwise blocked - no one moves to that target

        elves = new_elves
        start_dir = (start_dir + 1) % 4

        # If user wanted exactly 'rounds' rounds, stop when reached
        if rounds is not None and round_idx >= rounds:
            return elves, round_idx

        # If nobody moved this round -> finished
        if not moved:
            return elves, round_idx  # round_idx is the first round with no movement


if __name__ == "__main__":
    elves = read_input_file()

    # Part 1: run 10 rounds then compute area
    elves_after_10, _ = simulate(elves, rounds=10)
    p1 = bounding_area(elves_after_10)

    # Part 2: run until no movement and return the round index (1-based)
    _, p2 = simulate(elves, rounds=None)

    print("Part 1:", p1)
    print("Part 2:", p2)
