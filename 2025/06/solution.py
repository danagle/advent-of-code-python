"""
Advent of Code 2025
Day 6: Trash Compactor
https://adventofcode.com/2025/day/6
"""
from functools import reduce
from itertools import groupby
from operator import add, mul
from pathlib import Path

# Dictionary mapping operator characters to their corresponding functions
OPERATIONS = {'+': add, '*': mul}


def read_input_file(filepath="input.txt"):
    """
    Reads the input file as a list of lines of text.
    """
    return Path(filepath).read_text(encoding="utf-8").strip().splitlines()


def part_one(lines):
    """
    Process lines as rows and apply operators from last row.
    
    Treats input as a grid where numbers are in rows and operators are in the
    last row. Transposes to columns and applies each column's operator to its numbers.
    """
    # Split all lines into tokens
    rows = [line.split() for line in lines]
    
    # Parse number rows (all but last) as integers
    number_rows = [[int(x) for x in row] for row in rows[:-1]]
    operator_row = rows[-1]
    
    # Transpose to get columns, then apply operator to each column's numbers
    columns = zip(*number_rows)
    results = (
        reduce(OPERATIONS[op], nums) 
        for op, nums in zip(operator_row, columns)
    )
    
    return sum(results)


def part_two(lines):
    """
    Process columns by extracting vertical multi-digit numbers and operators.
    
    Reads the grid vertically: each column contains digit characters forming
    numbers, with an operator at the bottom. Consecutive columns with digits
    form multi-digit numbers (e.g., columns "1", "2", "3" form 123).
    """
    # Pad lines to uniform length and transpose to columns
    max_length = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_length) for line in lines]
    columns = list(zip(*padded_lines))
    
    # Extract operators (last char of each column if it's +/*)
    operators = [col[-1] for col in columns if col[-1] in OPERATIONS]
    
    # Extract number strings from each column (all but last char, stripped)
    number_strings = [''.join(col[:-1]).strip() for col in columns]
    
    # Group consecutive non-empty strings - each group forms a multi-digit number
    # groupby(number_strings, bool) separates empty strings from non-empty ones
    # Each non-empty group represents digits that form a complete number
    number_groups = [
        [int(digit) for digit in group]
        for is_non_empty, group in groupby(number_strings, bool)
        if is_non_empty
    ]
    
    # Apply each operator to its corresponding number group
    results = (
        reduce(OPERATIONS[op], nums)
        for op, nums in zip(operators, number_groups)
    )
    
    return sum(results)


if __name__ == "__main__":
    lines = read_input_file()
    print(f"Part 1: {part_one(lines)}")
    print(f"Part 2: {part_two(lines)}")
