# Day 12: Passage Pathing

from pathlib import Path
from typing import Dict, List, Set


def read_input_file(filepath: str = "input.txt") -> Dict[str, List[str]]:
    """
    Read the cave connections from the input file and build an adjacency list.
    """
    graph: Dict[str, List[str]] = {}
    for line in Path(filepath).read_text().strip().splitlines():
        a, b = line.split("-")
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)
    return graph


def is_small_cave(cave: str) -> bool:
    """Return True if the cave name is lowercase (a small cave)."""
    return cave.islower()


def part_one(graph: Dict[str, List[str]]) -> int:
    """
    Count all distinct paths from 'start' to 'end' following Part 1 rules:
    - Small caves can be visited at most once.
    """

    def dfs(current: str, visited: Set[str]) -> int:
        if current == "end":
            return 1
        total_paths = 0
        for neighbor in graph[current]:
            if is_small_cave(neighbor) and neighbor in visited:
                continue
            total_paths += dfs(neighbor, visited | {neighbor} if is_small_cave(neighbor) else visited)
        return total_paths

    return dfs("start", {"start"})


def part_two(graph: Dict[str, List[str]]) -> int:
    """
    Count all distinct paths from 'start' to 'end' following Part 2 rules:
    - One small cave can be visited twice.
    - Other small caves can be visited at most once.
    - 'start' cannot be revisited.
    """

    def dfs(current: str, visited: Set[str], small_cave_used: bool) -> int:
        if current == "end":
            return 1
        total_paths = 0
        for neighbor in graph[current]:
            if neighbor == "start":
                continue
            if is_small_cave(neighbor):
                if neighbor not in visited:
                    total_paths += dfs(neighbor, visited | {neighbor}, small_cave_used)
                elif not small_cave_used:
                    total_paths += dfs(neighbor, visited, True)
            else:
                total_paths += dfs(neighbor, visited, small_cave_used)
        return total_paths

    return dfs("start", {"start"}, False)


if __name__ == "__main__":
    graph = read_input_file()
    print(f"Part 1: {part_one(graph)}")
    print(f"Part 2: {part_two(graph)}")
