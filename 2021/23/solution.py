# Day 23: Amphipod

from functools import cache
from math import inf
from pathlib import Path
from typing import Tuple, Optional


def read_input_file(filepath: str = "input.txt") -> Tuple[Tuple[Optional[str], ...], ...]:
    """Convert input string to initial hallway+rooms state."""
    text = Path(filepath).read_text().strip()
    letters = [c for c in text if c.isalpha()]
    room_rows = letters[:4], letters[4:]
    rooms = tuple(zip(*room_rows))
    hallway = tuple([None] * 11)
    return (hallway,) + rooms


def generate_moves(state: Tuple[Tuple[Optional[str], ...], ...]):
    """
    Generate all valid next states and associated move costs.
    state[0] is the hallway tuple
    state[1..4] are the room tuples
    """
    hallway, *rooms = state

    # Energy cost per step per amphipod
    energy_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    # Hallway positions corresponding to each room index
    room_hallways = {1: 2, 2: 4, 3: 6, 4: 8}
    room_doors = {2, 4, 6, 8}

    # Target room for each amphipod type
    target_rooms = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

    # Move amphipods from rooms to hallway
    for room_idx, room in enumerate(rooms, start=1):
        # Find the topmost amphipod in this room
        for top_index, amphipod in enumerate(room):
            if amphipod is not None:
                break
        else:
            continue  # Room empty

        # Skip if amphipod is already in correct room and all below are correct
        target_pos = room_hallways[room_idx]
        if target_rooms[amphipod] == target_pos and all(a == amphipod for a in room[top_index:]):
            continue

        # Steps to exit the room
        steps_out = top_index + 1
        # Try moving left and right in the hallway
        for direction in [-1, 1]:
            pos = target_pos
            while 0 <= pos + direction < 11:
                pos += direction
                if hallway[pos] is not None:
                    break
                if pos in room_doors:
                    continue
                # Valid hallway stop
                new_hallway = list(hallway)
                new_hallway[pos] = amphipod
                new_rooms = [list(r) for r in rooms]
                new_rooms[room_idx - 1][top_index] = None
                move_cost = (steps_out + abs(pos - target_pos)) * energy_cost[amphipod]
                yield (tuple(new_hallway), *(tuple(r) for r in new_rooms)), move_cost

    # Move amphipods from hallway to rooms
    for pos, amphipod in enumerate(hallway):
        if amphipod is None:
            continue
        target_room_idx = 'ABCD'.index(amphipod) + 1
        target_room_pos = room_hallways[target_room_idx]
        target_room = rooms[target_room_idx - 1]

        # Room must contain only correct amphipods or be empty
        if any(a is not None and a != amphipod for a in target_room):
            continue

        # Check if path from hallway to room is clear
        step = 1 if pos < target_room_pos else -1
        path_clear = all(hallway[i] is None for i in range(pos + step, target_room_pos + step, step))
        if not path_clear:
            continue

        # Find the deepest empty spot in the room
        for room_depth in reversed(range(len(target_room))):
            if target_room[room_depth] is None:
                break

        # Apply move
        new_hallway = list(hallway)
        new_hallway[pos] = None
        new_rooms = [list(r) for r in rooms]
        new_rooms[target_room_idx - 1][room_depth] = amphipod
        steps_taken = abs(pos - target_room_pos) + room_depth + 1
        yield (tuple(new_hallway), *(tuple(r) for r in new_rooms)), steps_taken * energy_cost[amphipod]


@cache
def min_energy_to_solve(state: Tuple[Tuple[Optional[str], ...], ...], 
                        target_state: Tuple[Tuple[Optional[str], ...], ...]) -> int:
    """Recursive memoized search to find minimal total energy to reach target state."""
    if state == target_state:
        return 0

    costs = [inf]
    for new_state, move_cost in generate_moves(state):
        costs.append(move_cost + min_energy_to_solve(new_state, target_state))
    return min(costs)


def part_one(state: Tuple[Tuple[Optional[str], ...], ...]) -> int:
    room_size = len(state[1])
    target_state = (
        tuple([None] * 11),
        *(tuple([amphipod] * room_size) for amphipod in "ABCD")
    )
    return min_energy_to_solve(state, target_state)


def part_two(first_state: Tuple[Tuple[Optional[str], ...], ...]) -> int:
    folded_page = (('D', 'D'), ('C', 'B'), ('B', 'A'), ('A', 'C'))
    rooms = tuple(tuple(a+b+c+d for (a,d),(b,c) in zip(first_state[1:], folded_page)))
    state = (tuple([None]*11),) + rooms
    room_size = len(state[1])
    target_state = (
        tuple([None]*11),
        *(tuple([amphipod]*room_size) for amphipod in "ABCD")
    )
    return min_energy_to_solve(state, target_state)


if __name__ == "__main__":
    state = read_input_file()

    p1 = part_one(state)
    print("Part 1:", p1)

    p2 = part_two(state)
    print("Part 2:", p2)
