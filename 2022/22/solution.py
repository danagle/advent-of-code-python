# Day 22: Monkey Map

import math
import re
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass(frozen=True)
class CubeFace:
    value: int
    rotation: int


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
NUM_DIRECTIONS = 4

# Edges mapping (bi-directional)
CUBE_EDGES: Dict[CubeFace, CubeFace] = {
    CubeFace(1, 0): CubeFace(2, 3),
    CubeFace(1, 1): CubeFace(4, 2),
    CubeFace(1, 2): CubeFace(5, 3),
    CubeFace(2, 0): CubeFace(3, 3),
    CubeFace(2, 1): CubeFace(6, 2),
    CubeFace(3, 0): CubeFace(1, 3),
    CubeFace(3, 1): CubeFace(5, 2),
    CubeFace(3, 2): CubeFace(6, 3),
    CubeFace(4, 0): CubeFace(6, 1),
    CubeFace(4, 3): CubeFace(2, 2),
    CubeFace(5, 0): CubeFace(4, 1),
    CubeFace(5, 1): CubeFace(6, 0),
}
# Make mapping bi-directional
CUBE_EDGES |= {v: k for k, v in CUBE_EDGES.items()}


def read_input_file(filename: str = "input.txt") -> Tuple[List, List[str]]:
    with open(filename) as f:
        txt = f.read().split("\n\n")
    grid = txt[0].splitlines()
    max_len = max(len(row) for row in grid)
    grid = [row.ljust(max_len) for row in grid]

    instructions = [int(x) if x.isdigit() else x for x in re.findall(r'\d+|[LR]', txt[1])]
    return instructions, grid


def wrap_move(coord: Tuple[int, int], direction: Tuple[int, int], grid: List[str]) -> Tuple[int, int]:
    rows, cols = len(grid), len(grid[0])
    r, c = coord
    dr, dc = direction
    while True:
        r = (r + dr) % rows
        c = (c + dc) % cols
        if grid[r][c] != ' ':
            return r, c


def part_one(instructions: List, grid: List[str]) -> int:
    coord = (0, grid[0].index('.'))
    dindex = 0

    for instr in instructions:
        if instr == 'R':
            dindex = (dindex + 1) % NUM_DIRECTIONS
        elif instr == 'L':
            dindex = (dindex - 1) % NUM_DIRECTIONS
        else:
            for _ in range(instr):
                dr, dc = DIRECTIONS[dindex]
                next_coord = ((coord[0] + dr) % len(grid), (coord[1] + dc) % len(grid[0]))

                if grid[next_coord[0]][next_coord[1]] == ' ':
                    next_coord = wrap_move(next_coord, (dr, dc), grid)

                if grid[next_coord[0]][next_coord[1]] == '#':
                    break
                coord = next_coord

    return (coord[0] + 1) * 1000 + 4 * (coord[1] + 1) + dindex


def fold_cube(grid: List[str]):
    filled = sum(c != ' ' for row in grid for c in row)
    grid_res = int(math.sqrt(filled // 6))
    n, m = len(grid) // grid_res, len(grid[0]) // grid_res
    blocks = [(i, j) for i in range(n) for j in range(m) if grid[i*grid_res][j*grid_res] != ' ']

    block_assignments: Dict[Tuple[int,int], CubeFace] = {blocks[0]: CubeFace(1, 0)}
    q = deque([blocks[0]])

    while q:
        block = q.popleft()
        face = block_assignments[block]
        bi, bj = block
        for epi, (di, dj) in enumerate(DIRECTIONS):
            next_block = (bi + di, bj + dj)
            if next_block not in blocks or next_block in block_assignments:
                continue

            active_edge = CubeFace(face.value, (epi + face.rotation) % NUM_DIRECTIONS)
            nm = CUBE_EDGES[active_edge]
            r = (nm.rotation - epi + 2) % NUM_DIRECTIONS

            block_assignments[next_block] = CubeFace(nm.value, r)
            q.append(next_block)

    inv_block_assignments = {v.value: k for k, v in block_assignments.items()}
    return block_assignments, inv_block_assignments, grid_res


def rotate_coord_with_edge(rel_coord: Tuple[int, int], dindex: int, grid_res: int, next_dindex: int) -> Tuple[int, int]:
    row, col = rel_coord
    if next_dindex == 0:      # facing right
        return row, 0
    elif next_dindex == 1:    # facing down
        return 0, grid_res - 1 - col
    elif next_dindex == 2:    # facing left
        return grid_res - 1 - row, grid_res - 1
    else:                     # facing up
        return grid_res - 1, col


def part_two(instructions: List, grid: List[str]) -> int:
    block_assignments, inv_block_assignments, grid_res = fold_cube(grid)
    # Start at the top-left block
    current_block = min(block_assignments)
    coord = [current_block[0] * grid_res, current_block[1] * grid_res]
    dindex = 0  # facing right

    for instr in instructions:
        if instr == 'R':
            dindex = (dindex + 1) % NUM_DIRECTIONS
        elif instr == 'L':
            dindex = (dindex - 1) % NUM_DIRECTIONS
        else:
            for _ in range(instr):
                dr, dc = DIRECTIONS[dindex]
                next_coord = [coord[0] + dr, coord[1] + dc]
                next_block = (next_coord[0] // grid_res, next_coord[1] // grid_res)
                next_dindex = dindex

                if next_block != current_block:
                    # Crossing cube edge
                    curr_face = block_assignments[current_block]
                    exit_edge = CubeFace(curr_face.value, (curr_face.rotation + dindex) % NUM_DIRECTIONS)
                    next_edge = CUBE_EDGES[exit_edge]

                    next_block = inv_block_assignments[next_edge.value]
                    next_face = block_assignments[next_block]

                    next_dindex = (next_edge.rotation - next_face.rotation + 2) % NUM_DIRECTIONS

                    # Relative coordinates inside the current block
                    block_coord = [coord[0] - current_block[0] * grid_res,
                                   coord[1] - current_block[1] * grid_res]

                    # Compute relative position along the edge
                    if dindex == 0:        # moving right
                        rel = block_coord[0]
                    elif dindex == 1:      # moving down
                        rel = grid_res - 1 - block_coord[1]
                    elif dindex == 2:      # moving left
                        rel = grid_res - 1 - block_coord[0]
                    else:                  # moving up
                        rel = block_coord[1]

                    # Map relative coordinate to new block
                    if next_dindex == 0:      # entering from left
                        next_coord_block = [rel, 0]
                    elif next_dindex == 1:    # entering from top
                        next_coord_block = [0, grid_res - 1 - rel]
                    elif next_dindex == 2:    # entering from right
                        next_coord_block = [grid_res - 1 - rel, grid_res - 1]
                    else:                     # entering from bottom
                        next_coord_block = [grid_res - 1, rel]

                    # Map back to global coordinates
                    next_coord = [next_block[0] * grid_res + next_coord_block[0],
                                  next_block[1] * grid_res + next_coord_block[1]]

                # Move if possible
                if grid[next_coord[0]][next_coord[1]] == '.':
                    coord = next_coord
                    current_block = next_block
                    dindex = next_dindex
                elif grid[next_coord[0]][next_coord[1]] == '#':
                    break
                else:
                    raise Exception("Unexpected tile encountered!")

    return 1000 * (coord[0] + 1) + 4 * (coord[1] + 1) + dindex


if __name__ == "__main__":
    instructions, grid = read_input_file()
    print("Part 1:", part_one(instructions, grid))
    print("Part 2:", part_two(instructions, grid))
