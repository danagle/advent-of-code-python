# Day 22: Reactor Reboot

from numba import njit
import numpy as np
from pathlib import Path
from typing import List, Set, Tuple


def read_input_file(filepath: str = "input.txt") -> List[Tuple[str, List[List[int]]]]:
    """
    Returns a list of tuples:
        (instruction, [[x_start, x_end], [y_start, y_end], [z_start, z_end]])
    """
    lines = Path(filepath).read_text().strip().splitlines()
    instructions = []

    for line in lines:
        instruction, coords = line.split()
        ranges = [list(map(int, part[2:].split(".."))) for part in coords.split(",")]
        for r in ranges:
            r[1] += 1  # convert inclusive to half-open
        instructions.append((instruction, ranges))

    return instructions


def part_one(instructions: List[Tuple[str, List[List[int]]]]) -> int:
    """
    Execute the reboot steps limited to the initialization region (−50..50).
    Returns the number of cubes that are 'on' after processing all steps.
    """
    active_cubes: Set[Tuple[int, int, int]] = set()

    for instruction, cube in instructions:
        x_range, y_range, z_range = cube

        # Clamp ranges to the initialization region
        x0, x1 = max(x_range[0], -50), min(x_range[1], 51)
        y0, y1 = max(y_range[0], -50), min(y_range[1], 51)
        z0, z1 = max(z_range[0], -50), min(z_range[1], 51)

        # Skip instructions fully outside the region
        if x0 >= x1 or y0 >= y1 or z0 >= z1:
            continue

        turn_on = instruction == "on"

        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    if turn_on:
                        active_cubes.add((x, y, z))
                    else:
                        active_cubes.discard((x, y, z))

    return len(active_cubes)


def part_two_original(instructions: List[tuple[str, list[list[int]]]]) -> int:
    """
    Process a list of on/off cuboid instructions and return
    the total volume of cubes that are 'on' after all steps.
    """
    # Collect unique coordinate boundaries for compression
    axes = [set() for _ in range(3)]
    for _, cube in instructions:
        for dim in range(3):
            axes[dim].update(cube[dim])

    axes = [sorted(a) for a in axes]
    x_index = {x: i for i, x in enumerate(axes[0])}
    y_index = {y: i for i, y in enumerate(axes[1])}
    z_index = {z: i for i, z in enumerate(axes[2])}

    # Initialize compressed 3D grid
    x_len = len(axes[0]) - 1
    y_len = len(axes[1]) - 1
    z_len = len(axes[2]) - 1
    grid = [[[False] * z_len for _ in range(y_len)] for _ in range(x_len)]

    # Apply each instruction
    for instruction, cube in instructions:
        turn_on = instruction == "on"
        x0, x1 = cube[0]
        y0, y1 = cube[1]
        z0, z1 = cube[2]

        for xi in range(x_index[x0], x_index[x1]):
            for yi in range(y_index[y0], y_index[y1]):
                for zi in range(z_index[z0], z_index[z1]):
                    grid[xi][yi][zi] = turn_on

    # Compute total "on" volume
    total_volume = 0
    for xi in range(x_len):
        dx = axes[0][xi + 1] - axes[0][xi]
        for yi in range(y_len):
            dy = axes[1][yi + 1] - axes[1][yi]
            for zi in range(z_len):
                if grid[xi][yi][zi]:
                    dz = axes[2][zi + 1] - axes[2][zi]
                    total_volume += dx * dy * dz

    return total_volume


# Refactor of part_two to use a sparse cuboid list
Cuboid = Tuple[int, int, int, int, int, int]  # (x0, x1, y0, y1, z0, z1)

def cuboid_intersection(a: Cuboid, b: Cuboid) -> Cuboid | None:
    """
    Return the intersecting cuboid of a and b, or None if they don't overlap.
    """
    x0 = max(a[0], b[0])
    x1 = min(a[1], b[1])
    y0 = max(a[2], b[2])
    y1 = min(a[3], b[3])
    z0 = max(a[4], b[4])
    z1 = min(a[5], b[5])
    if x0 < x1 and y0 < y1 and z0 < z1:
        return (x0, x1, y0, y1, z0, z1)
    return None


def add_cuboid(active: List[Tuple[Cuboid, int]], new: Cuboid, sign: int):
    """
    Add a cuboid to the list using inclusion-exclusion principle.
    Each cuboid in the list has a sign (+1 for 'on', -1 for 'off' overlap adjustment)
    """
    updates = []
    for existing, existing_sign in active:
        inter = cuboid_intersection(existing, new)
        if inter:
            updates.append((inter, -existing_sign))
    if sign == 1:
        updates.append((new, 1))
    active.extend(updates)


def part_two_sparse(instructions: List[Tuple[str, List[List[int]]]]) -> int:
    """
    Sparse cuboid implementation of reactor reboot.
    """
    active: List[Tuple[Cuboid, int]] = []

    for instr, cube in instructions:
        x0, x1 = cube[0]
        y0, y1 = cube[1]
        z0, z1 = cube[2]
        new_cuboid: Cuboid = (x0, x1, y0, y1, z0, z1)
        add_cuboid(active, new_cuboid, 1 if instr == "on" else 0)

    # Compute total volume
    total = 0
    for cuboid, sign in active:
        dx = cuboid[1] - cuboid[0]
        dy = cuboid[3] - cuboid[2]
        dz = cuboid[5] - cuboid[4]
        total += sign * dx * dy * dz

    return total

# Refactor of part_two to use Numpy

def part_two_numpy(instructions: List[Tuple[str, List[List[int]]]]) -> int:
    # Extract all unique coordinates for compression
    axes = [set(), set(), set()]
    for _, cube in instructions:
        for dim in range(3):
            axes[dim].update(cube[dim])
    axes = [sorted(a) for a in axes]
    x_index = {x: i for i, x in enumerate(axes[0])}
    y_index = {y: i for i, y in enumerate(axes[1])}
    z_index = {z: i for i, z in enumerate(axes[2])}

    grid = np.zeros((len(axes[0]) - 1, len(axes[1]) - 1, len(axes[2]) - 1), dtype=bool)

    for instruction, cube in instructions:
        turn_on = instruction == "on"
        x0, x1 = cube[0]
        y0, y1 = cube[1]
        z0, z1 = cube[2]

        grid[
            x_index[x0]:x_index[x1],
            y_index[y0]:y_index[y1],
            z_index[z0]:z_index[z1]
        ] = turn_on

    # Compute total "on" volume
    dx = np.diff(axes[0])
    dy = np.diff(axes[1])
    dz = np.diff(axes[2])
    volume = (grid * dx[:, None, None] * dy[None, :, None] * dz[None, None, :]).sum()
    return volume


# Refactor of part_two to use Numba

@njit
def apply_instruction(grid, x0, x1, y0, y1, z0, z1, turn_on):
    """Apply a single instruction to the 3D grid."""
    for xi in range(x0, x1):
        for yi in range(y0, y1):
            for zi in range(z0, z1):
                grid[xi, yi, zi] = turn_on


@njit
def compute_volume(grid, dx, dy, dz):
    """Compute total volume of 'on' cells in the grid."""
    total = 0
    nx, ny, nz = grid.shape
    for xi in range(nx):
        for yi in range(ny):
            for zi in range(nz):
                if grid[xi, yi, zi]:
                    total += dx[xi] * dy[yi] * dz[zi]
    return total


def part_two_numba(instructions: List[Tuple[str, List[List[int]]]]) -> int:
    """Reactor reboot using compressed grid + Numba acceleration."""
    # Coordinate compression
    axes = [set(), set(), set()]
    for _, cube in instructions:
        for dim in range(3):
            axes[dim].update(cube[dim])
    axes = [sorted(a) for a in axes]
    x_index = {x: i for i, x in enumerate(axes[0])}
    y_index = {y: i for i, y in enumerate(axes[1])}
    z_index = {z: i for i, z in enumerate(axes[2])}

    nx, ny, nz = len(axes[0]) - 1, len(axes[1]) - 1, len(axes[2]) - 1
    grid = np.zeros((nx, ny, nz), dtype=np.bool_)

    # Apply instructions using Numba
    for instr, cube in instructions:
        turn_on = instr == "on"
        x0, x1 = x_index[cube[0][0]], x_index[cube[0][1]]
        y0, y1 = y_index[cube[1][0]], y_index[cube[1][1]]
        z0, z1 = z_index[cube[2][0]], z_index[cube[2][1]]

        apply_instruction(grid, x0, x1, y0, y1, z0, z1, turn_on)

    # Precompute dx, dy, dz
    dx = np.array([axes[0][i + 1] - axes[0][i] for i in range(nx)], dtype=np.int64)
    dy = np.array([axes[1][i + 1] - axes[1][i] for i in range(ny)], dtype=np.int64)
    dz = np.array([axes[2][i + 1] - axes[2][i] for i in range(nz)], dtype=np.int64)

    return compute_volume(grid, dx, dy, dz)


if __name__ == "__main__":
    instructions = read_input_file()
    
    p1 = part_one(instructions)
    print("Part 1:", p1)

    # 76.77 secs
    #p2 = part_two_original(instructions)
    # 6.06 secs
    #p2 = part_two_sparse(instructions)
    # 3.42 secs
    #p2 = part_two_numpy(instructions)
    # 1.47 secs
    p2 = part_two_numba(instructions)
 
    print("Part 2:", p2)
