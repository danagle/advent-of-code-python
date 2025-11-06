"""
Advent of Code 2020
Day 7: Handy Haversacks
https://adventofcode.com/2020/day/7
"""
from collections import defaultdict
from pathlib import Path
import re


def load_rules(filename: str) -> dict[str, dict[str, int]]:
    """
    Parse bag rules from the input file.
    Returns a dictionary where each key is a bag color,
    and its value is a dict of contained bags and their counts.
    Example:
        {
            "light red": {"bright white": 1, "muted yellow": 2},
            "faded blue": {},
        }
    """
    rule_pattern = re.compile(r"(\d+) ([a-z ]+) bag")
    rules = {}

    for line in Path(filename).read_text().strip().splitlines():
        container, contents = line.split(" bags contain ")
        if "no other bags" in contents:
            rules[container] = {}
        else:
            contained = {color: int(num) for num, color in rule_pattern.findall(contents)}
            rules[container] = contained
    return rules


def build_reverse_graph(rules: dict[str, dict[str, int]]) -> dict[str, set[str]]:
    """
    Create a reverse mapping from contained bag → set of containers that can hold it.
    Example:
        { "shiny gold": {"bright white", "muted yellow"}, ... }
    """
    reverse = defaultdict(set)
    for outer, inner_bags in rules.items():
        for color in inner_bags:
            reverse[color].add(outer)
    return reverse


def find_possible_containers(target: str, reverse_graph: dict[str, set[str]]) -> set[str]:
    """
    Recursively find all bags that can eventually contain the target color.
    """
    found = set()

    def dfs(color):
        for outer in reverse_graph.get(color, []):
            if outer not in found:
                found.add(outer)
                dfs(outer)

    dfs(target)
    return found


def count_total_bags(color: str, rules: dict[str, dict[str, int]]) -> int:
    """
    Recursively count how many individual bags are required inside one bag of the given color.
    """
    total = 0
    for inner_color, count in rules.get(color, {}).items():
        total += count + count * count_total_bags(inner_color, rules)
    return total


def part_one(rules: dict[str, dict[str, int]]):
    reverse_graph = build_reverse_graph(rules)
    containers = find_possible_containers("shiny gold", reverse_graph)
    print(f"Part 1 answer: {len(containers)}")


def part_two(rules: dict[str, dict[str, int]]):
    total_inside = count_total_bags("shiny gold", rules)
    print(f"Part 2 answer: {total_inside}")


if __name__ == "__main__":
    rules = load_rules("input.txt")
    part_one(rules)
    part_two(rules)
