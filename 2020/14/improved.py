"""
Advent of Code 2020
Day 14: Docking Data
https://adventofcode.com/2020/day/14

Uses bitwise operations and integer masks instead of strings
"""
from pathlib import Path
import re
from typing import List


def read_input_data(filepath: str = "input.txt") -> List[str]:
    """Read and return input lines."""
    return Path(filepath).read_text().strip().splitlines()


def apply_mask_to_value(value: int, mask: str) -> int:
    """Apply a bitmask to a value (Part 1 logic)."""
    or_mask = int(mask.replace("X", "0"), 2)
    and_mask = int(mask.replace("X", "1"), 2)
    return (value & and_mask) | or_mask


def generate_addresses(base_addr: int, mask: str) -> List[int]:
    """
    Efficiently generate all addresses after applying the mask (Part 2).
    - '1' in mask sets bit to 1
    - 'X' in mask floats between 0 and 1
    """
    # Apply all '1's directly to base address
    addr = base_addr | int(mask.replace("X", "0"), 2)

    # Collect positions of floating bits
    floating_bits = [35 - i for i, bit in enumerate(mask) if bit == "X"]

    addresses = []
    # Generate combinations by toggling each floating bit
    for n in range(1 << len(floating_bits)):
        a = addr
        for i, bit_pos in enumerate(floating_bits):
            if n & (1 << i):
                a |= (1 << bit_pos)
            else:
                a &= ~(1 << bit_pos)
        addresses.append(a)
    return addresses


def part_one(lines: List[str]) -> int:
    """Execute the docking program (mask applies to values)."""
    memory = {}
    mask = ""

    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            addr, val = map(int, re.findall(r"\d+", line))
            memory[addr] = apply_mask_to_value(val, mask)

    return sum(memory.values())


def part_two(lines: List[str]) -> int:
    """Execute the docking program (mask applies to addresses)."""
    memory = {}
    mask = ""

    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            addr, val = map(int, re.findall(r"\d+", line))
            for resolved_addr in generate_addresses(addr, mask):
                memory[resolved_addr] = val

    return sum(memory.values())


if __name__ == "__main__":
    lines = read_input_data()
    p1 = part_one(lines)
    print("Part 1:", p1)
    p2 = part_two(lines)
    print("Part 2:", p2)
