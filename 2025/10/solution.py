"""
Advent of Code 2025
Day 10: Factory
https://adventofcode.com/2025/day/10
"""
from collections import deque
from pathlib import Path
from scipy.optimize import linprog
import re


def read_input_file(filepath="input.txt"):
    """
    Parse the input file describing each machine.

    Each line of the file contains:
      - A bracketed light pattern: "[.#..#]" where '#' means lit and '.' means off.
      - One or more button definitions in parentheses: "(0,2,3)"
      - A joltage requirement in braces: "{3,5,4,7}"
    """
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()

    machines = []

    for line in lines:
        buttons = []
        # Grab everything inside [], (), and {}
        tokens = re.findall(r"\[.*?\]|\(.*?\)|\{.*?\}", line)
        for tok in tokens:
            if tok.startswith('['):    # e.g. [.##.]
                lights = [c == '#' for c in tok[1:-1]]
            elif tok.startswith('('):  # e.g. (1,3)
                buttons.append(tuple(map(int, tok[1:-1].strip().split(','))))
            elif tok.startswith('{'):  # e.g. {3,5,4,7}
                joltages = tuple(int(x) for x in tok[1:-1].strip().split(','))

        machines.append([lights, buttons, joltages])

    return machines


def part_one(machines_list):
    """
    Compute the total number of button presses needed to reach each machine's
    target light pattern.

    For each machine:
        - Start with all lights off.
        - Use BFS to find the minimum number of button presses required
          to match the target light configuration.
        - A button toggles the indices listed in its tuple.
    """
    total = 0

    for lights, buttons, _ in machines_list:
        state = [False] * len(lights)
        q = deque(((state, 0),))
        visited = set(str(state))
        while q:
            curr_state, depth = q.popleft()
            if curr_state == lights:
                total += depth
                break
            for button in buttons:
                new_state = curr_state[:]
                for press in button:
                    new_state[press] = not new_state[press]
                to_add = new_state
                if str(to_add) not in visited:
                    visited.add(str(to_add))
                    q.append((to_add, depth + 1))

    return total


def part_two(machines_list):
    """
    Solve a linear system for each machine to determine the optimal number of
    presses for each button under integer constraints.

    For each machine:
        - costs is simply 1 per button.
        - eqs[i][b] is True if button b contributes to joltage element i.
        - Solve min(costs · x) subject to A_eq * x = joltages, x integer.
    """
    total = 0

    for _, buttons, joltages in machines_list:
        costs = [1 for b in buttons]
        eqs = [[i in b for b in buttons] for i in range(len(joltages))]
        total += linprog(costs, A_eq=eqs, b_eq=joltages, integrality=1).fun
    
    return int(total)


if __name__ == "__main__":
    machines = read_input_file()
    print("Part 1:", part_one(machines))
    print("Part 2:", part_two(machines))
