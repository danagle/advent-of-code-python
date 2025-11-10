# Day 16: Proboscidea Volcanium
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Tuple


def load_input_file(filepath: str = "input.txt") -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    """Parse input file into a graph of valves and a flow rate mapping."""
    graph = {}
    flow_rate = {}

    for line in Path(filepath).read_text().splitlines():
        parts = line.replace(",", "").split()
        valve = parts[1]
        graph[valve] = parts[9:]
        rate = int(parts[4].split("=")[1][:-1])
        if rate > 0:
            flow_rate[valve] = rate

    return graph, flow_rate


def shortest_paths_from(valve: str, key_valves: List[str], graph: Dict[str, List[str]]) -> Dict[str, int]:
    """Compute shortest path lengths from a valve to all other key valves using BFS."""
    distances = {}
    for target in key_valves:
        if valve == target:
            continue

        queue = deque([[valve]])
        visited = set()

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current in visited:
                continue
            visited.add(current)

            if current == target:
                distances[target] = len(path) - 1
                break

            for neighbor in graph[current]:
                if neighbor not in path:
                    queue.append(path + [neighbor])

    return distances


def compute_path_time(distances: Dict[str, Dict[str, int]], path: List[str]) -> int:
    """Compute total time spent along a path (each move + 1 minute to open valve)."""
    return sum(distances[path[i - 1]][path[i]] + 1 for i in range(1, len(path)))


def compute_pressure(distances: Dict[str, Dict[str, int]], flow_rate: Dict[str, int],
                     path: List[str], time_limit: int = 30) -> int:
    """Compute total pressure released along a path within the time limit."""
    total = 0
    time_remaining = time_limit

    for i in range(1, len(path)):
        move_time = distances[path[i - 1]][path[i]] + 1
        if time_remaining > move_time:
            time_remaining -= move_time
            total += flow_rate[path[i]] * time_remaining
        else:
            break

    return total


def part_one(graph, flow_rate) -> int:
    key_valves = ["AA"] + list(flow_rate.keys())

    # Precompute shortest paths between all key valves
    distances = {v: shortest_paths_from(v, key_valves, graph) for v in key_valves}

    queue = deque([["AA"]])
    pressures = set()

    while queue:
        path = queue.popleft()

        if compute_path_time(distances, path) > 30 or len(path) == len(key_valves):
            pressures.add(compute_pressure(distances, flow_rate, path))
            continue

        for next_valve in key_valves:
            if next_valve not in path:
                queue.append(path + [next_valve])

    return max(pressures)


def part_two(graph, flow_rate) -> int:
    key_valves = ["AA"] + list(flow_rate.keys())

    # Precompute shortest paths between all key valves
    distances = {v: shortest_paths_from(v, key_valves, graph) for v in key_valves}

    queue = deque([["AA"]])
    pressures = defaultdict(int)

    while queue:
        path = queue.popleft()
        if compute_path_time(distances, path) > 26 or len(path) >= len(key_valves) // 2:
            pressure = compute_pressure(distances, flow_rate, path, 26)
            key_set = frozenset(set(path) - {"AA"})
            pressures[key_set] = max(pressure, pressures[key_set])
            continue

        for next_valve in key_valves:
            if next_valve not in path:
                queue.append(path + [next_valve])

    # Find the best combination of two disjoint sets of opened valves
    max_total = 0
    threshold = max(pressures.values()) * 0.75

    for p1 in pressures:
        if pressures[p1] < threshold:
            continue
        for p2 in pressures:
            if pressures[p2] < threshold:
                continue
            if p1.isdisjoint(p2):
                max_total = max(max_total, pressures[p1] + pressures[p2])

    return max_total


if __name__ == "__main__":
    graph, flow_rate = load_input_file()
    print("Part 1:", part_one(graph, flow_rate))
    print("Part 2:", part_two(graph, flow_rate))
