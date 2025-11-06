# Day 18: Snailfish

from functools import reduce
from math import ceil
from pathlib import Path
from typing import List, Union, Optional

# Type alias for a snailfish number representation
SnailfishToken = Union[int, str]
SnailfishList = List[SnailfishToken]


def read_input_file(filepath: str = "input.txt") -> List[SnailfishList]:
    """
    Reads the input file and parses each line as a snailfish number.
    
    Converts each line from a string like "[1,2]" into a token list ['[', 1, ',', 2, ']']
    
    Args:
        filepath: Path to the input file
        
    Returns:
        List of snailfish numbers, where each number is a list of tokens
    """
    lines = Path(filepath).read_text().strip().splitlines()
    snailfish_numbers = []
    
    for line in lines:
        tokens: SnailfishList = []
        current_number = ''
        
        for char in line:
            if char.isdigit():
                current_number += char
            else:
                if current_number:
                    tokens.append(int(current_number))
                    current_number = ''
                tokens.append(char)
        
        snailfish_numbers.append(tokens)
    
    return snailfish_numbers


def snailfish_add(left: SnailfishList, right: SnailfishList) -> SnailfishList:
    """
    Adds two snailfish numbers and reduces the result.
    
    Args:
        left: First snailfish number
        right: Second snailfish number
        
    Returns:
        Reduced sum of the two numbers
    """
    combined = ['['] + left + [','] + right + [']']
    return snailfish_reduce(combined)


def index_next_number_right(tokens: SnailfishList, start_index: int) -> Optional[int]:
    """
    Finds the index of the next integer to the right of the given position.
    
    Args:
        tokens: List of snailfish tokens
        start_index: Starting position to search from
        
    Returns:
        Index of next integer, or None if not found
    """
    for index in range(start_index + 1, len(tokens)):
        if isinstance(tokens[index], int):
            return index
    return None


def index_next_number_left(tokens: SnailfishList, start_index: int) -> Optional[int]:
    """
    Finds the index of the next integer to the left of the given position.
    
    Args:
        tokens: List of snailfish tokens
        start_index: Starting position to search from
        
    Returns:
        Index of next integer, or None if not found
    """
    for index in range(start_index - 1, -1, -1):
        if isinstance(tokens[index], int):
            return index
    return None


def explode(tokens: SnailfishList) -> bool:
    """
    Attempts to explode a pair nested inside four pairs.
    
    When a pair is nested inside four pairs, the leftmost such pair explodes.
    The left value is added to the first number to the left (if any).
    The right value is added to the first number to the right (if any).
    The pair is replaced with 0.
    
    Args:
        tokens: List of snailfish tokens (modified in place)
        
    Returns:
        True if an explosion occurred, False otherwise
    """
    depth = -1
    
    for i, token in enumerate(tokens):
        if token == '[':
            depth += 1
        elif token == ']':
            depth -= 1
        elif token == ',':
            continue
        else:  # It's an integer
            if depth == 4:
                # Found a pair nested in 4 pairs
                left_value_index = i
                left_neighbor_index = index_next_number_left(tokens, i)
                
                right_value_index = index_next_number_right(tokens, i)
                right_neighbor_index = index_next_number_right(tokens, right_value_index)
                
                # Add values to neighbors
                if left_neighbor_index is not None:
                    tokens[left_neighbor_index] += tokens[left_value_index]
                if right_neighbor_index is not None:
                    tokens[right_neighbor_index] += tokens[right_value_index]
                
                # Replace the pair with 0
                tokens[left_value_index] = 0
                del tokens[left_value_index + 1]  # Remove ','
                del tokens[left_value_index + 1]  # Remove right value
                del tokens[left_value_index + 1]  # Remove ']'
                del tokens[left_value_index - 1]  # Remove '['
                
                return True
    
    return False


def split(tokens: SnailfishList) -> bool:
    """
    Attempts to split a number >= 10 into a pair.
    
    Replaces the first number >= 10 with [n//2, ceil(n/2)].
    
    Args:
        tokens: List of snailfish tokens (modified in place)
        
    Returns:
        True if a split occurred, False otherwise
    """
    for i, token in enumerate(tokens):
        if isinstance(token, int) and token >= 10:
            # Split the number into a pair
            del tokens[i]
            tokens.insert(i, '[')
            tokens.insert(i + 1, token // 2)
            tokens.insert(i + 2, ',')
            tokens.insert(i + 3, ceil(token / 2))
            tokens.insert(i + 4, ']')
            return True
    
    return False


def snailfish_reduce(tokens: SnailfishList) -> SnailfishList:
    """
    Reduces a snailfish number by repeatedly exploding and splitting.
    
    Args:
        tokens: List of snailfish tokens (modified in place)
        
    Returns:
        The reduced snailfish number
    """
    while True:
        if explode(tokens):
            continue
        if split(tokens):
            continue
        break
    
    return tokens


def get_magnitude_impl(value: Union[int, List]) -> int:
    """
    Recursively calculates the magnitude of a snailfish number.
    
    Args:
        value: Either an integer or a list [left, right]
        
    Returns:
        The magnitude as an integer
    """
    if isinstance(value, int):
        return value
    return 3 * get_magnitude_impl(value[0]) + 2 * get_magnitude_impl(value[1])


def get_magnitude(tokens: SnailfishList) -> int:
    """
    Calculates the magnitude of a snailfish number.
    
    Converts the token list back to a nested list structure and calculates magnitude.
    
    Args:
        tokens: List of snailfish tokens
        
    Returns:
        The magnitude of the snailfish number
    """
    nested_list = eval(''.join(str(token) for token in tokens))
    return get_magnitude_impl(nested_list)


def part_one(snailfish_numbers):
    """Part 1: Sum all numbers and find magnitude."""
    final_sum = reduce(snailfish_add, snailfish_numbers)

    return get_magnitude(final_sum)

    
def part_two(snailfish_numbers):
    """Part 2: Find largest magnitude from adding any two different numbers"""
    largest_magnitude = max(
        get_magnitude(snailfish_add(left, right))
        for left in snailfish_numbers
        for right in snailfish_numbers
        if left != right
    )
    
    return largest_magnitude


if __name__ == "__main__":
    snailfish_numbers = read_input_file()
    p1 = part_one(snailfish_numbers)
    print(f"Part 1: {p1}")
    p2 = part_two(snailfish_numbers)
    print(f"Part 2: {p2}")
