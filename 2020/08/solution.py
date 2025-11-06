"""
Advent of Code 2020
Day 8: Handheld Halting
https://adventofcode.com/2020/day/8
"""
from pathlib import Path
from typing import List, Tuple


class Computer:
    """A simple virtual machine that executes assembly-like instructions."""

    def __init__(self):
        self.code: List[Tuple[str, int]] = []
        self.accumulator: int = 0
        self.pc: int = 0
        self.terminated: bool = False

    def load_program(self, instructions: List[Tuple[str, int]]) -> None:
        """Load a new program into memory and reset the computer state."""
        self.code = instructions
        self.accumulator = 0
        self.pc = 0
        self.terminated = False

    def run(self) -> None:
        """Execute the loaded program until a loop is detected or it terminates."""
        visited = set()

        while self.pc not in visited and self.pc < len(self.code):
            visited.add(self.pc)
            op, arg = self.code[self.pc]

            if op == "nop":
                self.pc += 1
            elif op == "acc":
                self.accumulator += arg
                self.pc += 1
            elif op == "jmp":
                self.pc += arg
            else:
                raise ValueError(f"Invalid instruction '{op}' at line {self.pc}")

        if self.pc == len(self.code):
            self.terminated = True

    def result(self) -> int:
        """Return the value in the accumulator."""
        return self.accumulator


def read_instructions(filepath: str = "input.txt") -> List[Tuple[str, int]]:
    """Read and parse the instruction list from the input file."""
    lines = Path(filepath).read_text().strip().splitlines()
    return [(op, int(arg)) for op, arg in (line.split() for line in lines)]


def part_one(instructions: List[Tuple[str, int]]) -> None:
    """Run the program until it loops; print the accumulator before looping."""
    computer = Computer()
    computer.load_program(instructions)
    computer.run()
    print("Part 1:", computer.result())


def part_two(instructions: List[Tuple[str, int]]) -> None:
    """
    Try flipping exactly one 'nop' or 'jmp' instruction to fix the infinite loop.
    When the program terminates successfully, print the accumulator value.
    """
    instructions = read_instructions()
    computer = Computer()

    for i, (op, arg) in enumerate(instructions):
        if op not in {"nop", "jmp"}:
            continue

        # Create a modified copy with one swapped instruction
        modified = instructions.copy()
        modified[i] = ("jmp" if op == "nop" else "nop", arg)

        computer.load_program(modified)
        computer.run()

        if computer.terminated:
            print("Part 2:", computer.result())
            break


if __name__ == "__main__":
    instructions = read_instructions()
    part_one(instructions)
    part_two(instructions)
