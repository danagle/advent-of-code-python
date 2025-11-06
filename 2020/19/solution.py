"""
Advent of Code 2020
Day 19: Monster Messages
https://adventofcode.com/2020/day/19
"""
from __future__ import annotations
from pathlib import Path
import re
from typing import Dict, List, Union


Rule = Union[str, List[List[int]]]


def read_input_file(filepath: str = "input.txt") -> tuple[Dict[int, Rule], List[str]]:
    """Read and parse the input file into grammar rules and messages."""
    rules_section, messages_section = Path(filepath).read_text().strip().split("\n\n")
    rules: Dict[int, Rule] = {}

    for line in rules_section.splitlines():
        num_str, rule_str = line.split(": ")
        num = int(num_str)
        if '"' in rule_str:
            rules[num] = rule_str.strip('"')
        else:
            rules[num] = [
                [int(x) for x in part.split()] for part in rule_str.split(" | ")
            ]

    messages = messages_section.splitlines()
    return rules, messages


def build_regex(rules: Dict[int, Rule], rule_id: int = 0, memo: Dict[int, str] | None = None) -> str:
    """Recursively build a regex pattern for a given rule ID."""
    if memo is None:
        memo = {}

    if rule_id in memo:
        return memo[rule_id]

    rule = rules[rule_id]
    if isinstance(rule, str):
        memo[rule_id] = rule
        return rule

    parts = []
    for sequence in rule:
        seq_pattern = "".join(build_regex(rules, sub_id, memo) for sub_id in sequence)
        parts.append(seq_pattern)

    pattern = f"(?:{'|'.join(parts)})"
    memo[rule_id] = pattern
    return pattern


def count_matching_messages(rules: Dict[int, Rule], messages: List[str]) -> int:
    """Count how many messages fully match rule 0 (Part 1)."""
    pattern = re.compile(f"^{build_regex(rules, 0)}$")
    return sum(bool(pattern.fullmatch(msg)) for msg in messages)


def count_matching_messages_part2(rules: Dict[int, Rule], messages: List[str]) -> int:
    """
    Handle modified rules for Part 2:
    8: 42 | 42 8      -> one or more 42s
    11: 42 31 | 42 11 31 -> equal number of 42s and 31s
    """
    # Compile base subpatterns
    rule_42 = build_regex(rules, 42)
    rule_31 = build_regex(rules, 31)

    # 8 becomes (42)+
    # 11 becomes (42){n}(31){n} for n >= 1
    max_depth = 10
    patterns = [
        f"^(?:{rule_42})+"
        + f"({rule_42}){{{n}}}({rule_31}){{{n}}}$"
        for n in range(1, max_depth)
    ]

    compiled = [re.compile(p) for p in patterns]
    return sum(any(p.match(msg) for p in compiled) for msg in messages)


if __name__ == "__main__":
    rules, messages = read_input_file()
    p1 = count_matching_messages(rules, messages)
    print("Part 1:", p1)
    p2 = count_matching_messages_part2(rules, messages)
    print("Part 2:", p2)
