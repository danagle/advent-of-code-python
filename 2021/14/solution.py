# Day 14: Extended Polymerization

from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Tuple


def read_input_file(filepath: str = "input.txt") -> Tuple[str, Dict[str, str]]:
    """
    Reads the polymer template and pair insertion rules from the input file.
    
    Returns:
        template: Initial polymer string.
        rules: Dictionary mapping pairs (e.g., "AB") to insertion element (e.g., "C").
    """
    lines = Path(filepath).read_text().strip().splitlines()
    template = lines[0]
    rules: Dict[str, str] = {}
    for line in lines[2:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert
    return template, rules


def polymerize(template: str, rules: Dict[str, str], steps: int) -> int:
    """
    Perform polymerization for the given number of steps using pair counts.
    
    Returns:
        Difference between the most and least common elements.
    """
    # Count initial pairs
    pair_counts: Dict[str, int] = defaultdict(int)
    for i in range(len(template) - 1):
        pair_counts[template[i:i + 2]] += 1

    # Perform polymerization steps
    for _ in range(steps):
        new_counts: Dict[str, int] = defaultdict(int)
        for pair, count in pair_counts.items():
            if pair in rules:
                insert = rules[pair]
                new_counts[pair[0] + insert] += count
                new_counts[insert + pair[1]] += count
            else:
                new_counts[pair] += count
        pair_counts = new_counts

    # Count elements
    element_counts: Dict[str, int] = defaultdict(int)
    for pair, count in pair_counts.items():
        element_counts[pair[0]] += count
    element_counts[template[-1]] += 1  # last element of template

    counts = element_counts.values()
    return max(counts) - min(counts)


if __name__ == "__main__":
    template, rules = read_input_file()
    print(f"Part 1: {polymerize(template, rules, 10)}")
    print(f"Part 2: {polymerize(template, rules, 40)}")
