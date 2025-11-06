"""
Advent of Code 2020
Day 14: Docking Data
https://adventofcode.com/2020/day/14
"""
from itertools import product
from pathlib import Path
import re
from typing import List


def read_input_data(filepath: str = "input.txt") -> List[str]:
    """Read and return the input lines."""
    return Path(filepath).read_text().strip().splitlines()


def apply_mask_to_value(value: int, mask: str) -> int:
    """Apply a bitmask to a value (Part 1 logic)."""
    value_bits = list(f"{value:036b}")
    for i, bit in enumerate(mask):
        if bit in ("0", "1"):
            value_bits[i] = bit
    return int("".join(value_bits), 2)


def apply_mask_to_address(address: int, mask: str) -> List[int]:
    """Apply a bitmask to a memory address (Part 2 logic)."""
    address_bits = list(f"{address:036b}")

    # Apply mask rules
    for i, bit in enumerate(mask):
        if bit == "1":
            address_bits[i] = "1"
        elif bit == "X":
            address_bits[i] = "X"

    # Generate all combinations for floating bits
    floating_positions = [i for i, bit in enumerate(address_bits) if bit == "X"]
    addresses = []

    for combo in product("01", repeat=len(floating_positions)):
        temp = address_bits.copy()
        for pos, bit in zip(floating_positions, combo):
            temp[pos] = bit
        addresses.append(int("".join(temp), 2))

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
    """Execute the docking program (mask applies to memory addresses)."""
    memory = {}
    mask = ""

    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            addr, val = map(int, re.findall(r"\d+", line))
            for resolved_addr in apply_mask_to_address(addr, mask):
                memory[resolved_addr] = val

    return sum(memory.values())


if __name__ == "__main__":
    lines = read_input_data()
    p1 = part_one(lines)
    print("Part 1:", p1)
    p2 = part_two(lines)
    print("Part 2:", p2)
