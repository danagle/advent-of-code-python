# Day 5: Supply Stacks 

from pathlib import Path
from typing import List, Tuple


Instruction = Tuple[int, int, int]  # (count, from_stack, to_stack)


def read_input_file(filepath: str = "input.txt") -> Tuple[List[List[str]], List[Instruction]]:
    """
    Reads the input file and returns:
      - The initial stacks as a list of lists (bottom to top)
      - The movement instructions as a list of (count, from, to) tuples
    """
    text = Path(filepath).read_text().split("\n\n")
    stack_section, instruction_section = text[0].splitlines(), text[1].strip().splitlines()

    # Determine the number of stacks based on the last line of stack_section
    num_stacks = int(stack_section[-1].split()[-1])
    stacks: List[List[str]] = [[] for _ in range(num_stacks)]

    # Parse stacks from bottom up
    for line in reversed(stack_section[:-1]):
        for i in range(num_stacks):
            pos = 1 + i * 4
            if pos < len(line) and line[pos].isalpha():
                stacks[i].append(line[pos])

    # Parse movement instructions
    instructions: List[Instruction] = []
    for line in instruction_section:
        parts = line.split()
        count, src, dst = int(parts[1]), int(parts[3]), int(parts[5])
        instructions.append((count, src - 1, dst - 1))  # convert to 0-indexed

    return stacks, instructions


def move_crates_9000(stacks: List[List[str]], instructions: List[Instruction]) -> str:
    """
    Simulates the CrateMover 9000 behavior (move one crate at a time).
    Returns the final top crates as a string.
    """
    stacks = [s.copy() for s in stacks]
    for count, src, dst in instructions:
        for _ in range(count):
            if stacks[src]:
                stacks[dst].append(stacks[src].pop())
    return "".join(stack[-1] for stack in stacks if stack)


def move_crates_9001(stacks: List[List[str]], instructions: List[Instruction]) -> str:
    """
    Simulates the CrateMover 9001 behavior (move multiple crates at once preserving order).
    Returns the final top crates as a string.
    """
    stacks = [s.copy() for s in stacks]
    for count, src, dst in instructions:
        if stacks[src]:
            group = stacks[src][-count:]
            stacks[src] = stacks[src][:-count]
            stacks[dst].extend(group)
    return "".join(stack[-1] for stack in stacks if stack)


if __name__ == "__main__":
    stacks, instructions = read_input_file()
    print("Part 1:", move_crates_9000(stacks, instructions))
    print("Part 2:", move_crates_9001(stacks, instructions))
