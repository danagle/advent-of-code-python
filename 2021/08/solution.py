# Day 8: Seven Segment Search

from pathlib import Path
from typing import List, Tuple, Dict, Set


def read_input_file(filepath: str = "input.txt") -> List[Tuple[List[str], List[str]]]:
    """
    Read input file and return list of tuples:
    (signal_patterns, output_values), both as lists of strings.
    """
    data: List[Tuple[List[str], List[str]]] = []
    for line in Path(filepath).read_text().strip().splitlines():
        patterns_str, output_str = line.split(" | ")
        patterns = patterns_str.split()
        output = output_str.split()
        data.append((patterns, output))
    return data


def part_one(entries: List[Tuple[List[str], List[str]]]) -> int:
    """
    Count the digits in the output values that have unique segment lengths:
    1 (2 segments), 4 (4), 7 (3), 8 (7).
    """
    unique_lengths = {2, 3, 4, 7}
    return sum(len([d for d in output if len(d) in unique_lengths])
               for _, output in entries)


def decode_entry(signal_patterns: List[str]) -> Dict[frozenset, int]:
    """
    Decode the signal patterns to map frozenset of segments to the digit they represent.
    """
    patterns: List[Set[str]] = [set(p) for p in signal_patterns]
    mapping: Dict[int, Set[str]] = {}

    # Unique segment counts
    for p in patterns:
        if len(p) == 2:
            mapping[1] = p
        elif len(p) == 3:
            mapping[7] = p
        elif len(p) == 4:
            mapping[4] = p
        elif len(p) == 7:
            mapping[8] = p

    # Deduce remaining numbers
    for p in patterns:
        if p in mapping.values():
            continue
        if len(p) == 6:  # 0, 6, 9
            if mapping[4].issubset(p):
                mapping[9] = p
            elif mapping[1].issubset(p):
                mapping[0] = p
            else:
                mapping[6] = p
        elif len(p) == 5:  # 2, 3, 5
            if mapping[1].issubset(p):
                mapping[3] = p
            elif len(p.intersection(mapping[4])) == 3:
                mapping[5] = p
            else:
                mapping[2] = p

    # Reverse mapping: frozenset -> digit
    return {frozenset(v): k for k, v in mapping.items()}


def part_two(entries: List[Tuple[List[str], List[str]]]) -> int:
    """
    Decode all entries and sum their output values.
    """
    total = 0
    for patterns, output in entries:
        mapping = decode_entry(patterns)
        value = int("".join(str(mapping[frozenset(o)]) for o in output))
        total += value
    return total


if __name__ == "__main__":
    entries = read_input_file()
    print(f"Part 1: {part_one(entries)}")
    print(f"Part 2: {part_two(entries)}")
