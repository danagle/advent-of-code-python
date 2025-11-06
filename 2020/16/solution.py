"""
Advent of Code 2020
Day 16: Ticket Translation
https://adventofcode.com/2020/day/16
"""
from pathlib import Path
import re
import math


def read_input_file(filepath: str = "input.txt"):
    """Parse the input into rules, your ticket, and nearby tickets."""
    sections = Path(filepath).read_text().strip().split("\n\n")
    rule_lines, your_ticket_lines, nearby_ticket_lines = sections

    # Parse rules
    rules = {}
    rule_pattern = re.compile(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)")
    for line in rule_lines.splitlines():
        name, a1, a2, b1, b2 = rule_pattern.match(line).groups()
        rules[name] = [(int(a1), int(a2)), (int(b1), int(b2))]

    # Parse tickets
    your_ticket = [int(x) for x in your_ticket_lines.splitlines()[1].split(",")]
    nearby_tickets = [
        [int(x) for x in line.split(",")] for line in nearby_ticket_lines.splitlines()[1:]
    ]

    return rules, your_ticket, nearby_tickets


def is_value_valid(value: int, rules: dict) -> bool:
    """Check if a value fits at least one rule."""
    for ranges in rules.values():
        for low, high in ranges:
            if low <= value <= high:
                return True
    return False


def part_one(rules, nearby_tickets):
    """Compute the ticket scanning error rate."""
    error_rate = 0
    valid_tickets = []

    for ticket in nearby_tickets:
        invalid_values = [v for v in ticket if not is_value_valid(v, rules)]
        if invalid_values:
            error_rate += sum(invalid_values)
        else:
            valid_tickets.append(ticket)

    print("Part 1:", error_rate)
    return valid_tickets


def value_matches_rule(value: int, rule_ranges) -> bool:
    """Check if a value satisfies a specific rule."""
    return any(low <= value <= high for low, high in rule_ranges)


def determine_field_positions(rules, valid_tickets):
    """Determine which field index corresponds to which rule."""
    num_fields = len(valid_tickets[0])
    possible_fields = {rule: set(range(num_fields)) for rule in rules}

    # Eliminate impossible positions
    for rule, ranges in rules.items():
        for col in range(num_fields):
            if not all(value_matches_rule(ticket[col], ranges) for ticket in valid_tickets):
                possible_fields[rule].discard(col)

    # Deduce exact field positions
    final_mapping = {}
    while possible_fields:
        # Find rule with exactly one remaining possible position
        determined = [(r, next(iter(c))) for r, c in possible_fields.items() if len(c) == 1]
        for rule, idx in determined:
            final_mapping[rule] = idx
            del possible_fields[rule]
            for c in possible_fields.values():
                c.discard(idx)

    return final_mapping


def part_two(rules, your_ticket, valid_tickets):
    """Determine field mapping and compute the departure product."""
    mapping = determine_field_positions(rules, valid_tickets)

    product = math.prod(
        your_ticket[idx]
        for rule, idx in mapping.items()
        if rule.startswith("departure")
    )

    return product


if __name__ == "__main__":
    rules, your_ticket, nearby_tickets = read_input_file()
    valid_tickets = part_one(rules, nearby_tickets)
    p2 = part_two(rules, your_ticket, valid_tickets)
    print("Part 2:", p2)
