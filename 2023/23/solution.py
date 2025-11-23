# Day 23: A Long Walk
import sys

sys.setrecursionlimit(10_000)

DIRECTIONS = (
    (-1, 0, "<"),  # left
    ( 1, 0, ">"),  # right
    ( 0,-1, "^"),  # up
    ( 0, 1, "v"),  # down
)

def read_input_file():
    grid = open("input.txt").read().splitlines()

    height = len(grid)

    start = (grid[0].find("."), 0)
    goal  = (grid[-1].find("."), height - 1)
    
    return grid, start, goal


def part_one(grid, start, goal):
    height, width = len(grid), len(grid[0])
    visited = [False] * (width * height)
    sx, sy = start
    visited[sx] = True  # mark starting tile

    def dfs_with_slopes(x, y, visited, path_length):
        """Return longest path to goal using strict slope rules."""
        if (x, y) == goal:
            return path_length

        visited[y * width + x] = True
        best = 0

        for dx, dy, slope_symbol in DIRECTIONS:
            nx, ny = x + dx, y + dy
            cell = grid[ny][nx]

            # Movement is allowed if the cell is open or matches slope direction
            if (cell == "." or cell == slope_symbol) and not visited[ny * width + nx]:
                best = max(best, dfs_with_slopes(nx, ny, visited, path_length + 1))

        visited[y * width + x] = False
        return best

    return dfs_with_slopes(sx, sy + 1, visited, 1)


def build_compressed_graph(grid, start, goal):
    """Compresses the maze into a graph of junction nodes."""

    node_lookup = {start: 0, goal: 1}
    graph = [[], []]   # adjacency list: graph[node] = [(neighbor, distance)]

    def explore(current, previous, last_node, steps_since_node, visited):
        visited.add(current)
        x, y = current

        # Discover walkable neighbors
        neighbors = []
        for dx, dy, _ in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if grid[ny][nx] != "#" and (nx, ny) != previous:
                neighbors.append((nx, ny))

        # Create a new graph node at a junction
        if len(neighbors) > 1:
            new_node = node_lookup[current] = len(node_lookup)
            graph.append([])

            # Connect last node to this one
            graph[new_node].append((last_node, steps_since_node))
            graph[last_node].append((new_node, steps_since_node))

            last_node = new_node
            steps_since_node = 0

        # Recurse through neighbors
        for nbr in neighbors:
            if nbr in node_lookup:
                # Already known node: just add edge
                nid = node_lookup[nbr]
                graph[nid].append((last_node, steps_since_node + 1))
                graph[last_node].append((nid, steps_since_node + 1))
            elif nbr not in visited:
                explore(nbr, current, last_node,
                        steps_since_node + 1, visited)

    # Kick off exploration
    sx, sy = start
    explore((sx, sy + 1), start, 0, 1, set())

    return graph


def prune_dead_junctions(start_node, graph):
    """Prune special degree-3 dead branches by trimming backward edges."""
    stack = [start_node]

    while stack:
        next_layer = []
        for node in stack:
            for neighbor, _ in list(graph[node]):
                if len(graph[neighbor]) == 3:
                    # Remove edge pointing back
                    for target_node, dist in graph[neighbor]:
                        if target_node == node:
                            graph[neighbor].remove((target_node, dist))
                            break
                    next_layer.append(neighbor)
        stack = next_layer


def dfs_longest_path(current, visited_mask, distance, graph):
    """DFS that finds the longest simple path from start -> goal in node graph."""
    GOAL_NODE = 1
    if current == GOAL_NODE:
        return distance

    visited_mask |= 1 << current
    best = 0

    for neighbor, weight in graph[current]:
        if not (visited_mask & (1 << neighbor)):
            best = max(best,
                       dfs_longest_path(neighbor, visited_mask,
                                        distance + weight, graph))
    return best


def part_two(grid, start, goal):
    graph = build_compressed_graph(grid, start, goal)
    prune_dead_junctions(0, graph)

    return dfs_longest_path(0, 0, 0, graph)


if __name__ == "__main__":
    hiking_trails, current_path, end_path = read_input_file()
    p1 = part_one(hiking_trails, current_path, end_path)
    print("Part 1:", p1)
    p2 = part_two(hiking_trails, current_path, end_path)
    print("Part 2:", p2)
