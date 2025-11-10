# Day 10: Cathode-Ray Tube

from pathlib import Path


def read_input_file(filepath: str = "input.txt") -> dict[int, tuple[int, int]]:
    """
    Execute the CPU instructions and record the register value and signal strength at each cycle.
    Returns a mapping of cycle -> (register_x, signal_strength).
    """
    register_x = 1
    cycle_count = 0
    cycle_log = {}

    for instruction in Path(filepath).read_text().strip().splitlines():
        if instruction.startswith("addx"):
            # Two cycles for addx
            for _ in range(2):
                cycle_count += 1
                cycle_log[cycle_count] = (register_x, register_x * cycle_count)
            register_x += int(instruction.split()[1])
        else:
            # One cycle for noop
            cycle_count += 1
            cycle_log[cycle_count] = (register_x, register_x * cycle_count)

    return cycle_log


def part_one(cycle_log: dict[int, tuple[int, int]]) -> int:
    """Compute the sum of signal strengths at specific cycle checkpoints."""
    sample_cycles = [20, 60, 100, 140, 180, 220]
    return sum(cycle_log[cycle][1] for cycle in sample_cycles)


def part_two(cycle_log: dict[int, tuple[int, int]]) -> None:
    """Render the CRT display showing the sprite positions over time."""
    screen_width, screen_height = 40, 6
    display = [[" " for _ in range(screen_width)] for _ in range(screen_height)]

    for cycle, (register_x, _) in cycle_log.items():
        pixel_index = (cycle - 1) % screen_width
        row_index = (cycle - 1) // screen_width
        if pixel_index in [register_x - 1, register_x, register_x + 1]:
            display[row_index][pixel_index] = "#"

    print("Part 2:")
    for row in display:
        print("".join(row))


if __name__ == "__main__":
    cycle_log = read_input_file()
    print("Part 1:", part_one(cycle_log))
    part_two(cycle_log)
