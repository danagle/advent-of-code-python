"""
Advent of Code 2024
Day 16: Reindeer Maze
https://adventofcode.com/2024/day/16
"""
import heapq
from time import perf_counter as measure_time

def performance_profiler(method):
    """
    A decorator that measures and prints the execution time of a method.
    
    This decorator wraps the given method and calculates its execution time,
    providing performance insights for the decorated function.
    
    Args:
        method (callable): The function to be timed
    
    Returns:
        callable: A wrapper function that measures the method's execution time
    """
    def timing_wrapper(*args, **kwargs):
        # Record the start time before method execution
        start_time = measure_time()
        
        # Execute the original method
        result = method(*args, **kwargs)
        
        # Print the execution time with high precision
        print(
            f"Method {method.__name__} took: "
            f"{measure_time() - start_time:2.5f} sec"
        )
        
        # Return the original method's result
        return result
    return timing_wrapper


def parse_input(file_path):
    start = (-1, -1)
    empty_spaces = set()
    with open(file_path) as f:
        lines = f.read().strip().splitlines()
        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                if tile == "E":
                    end = (x, y)
                    empty_spaces.add((x, y))
                elif tile == "S":
                    start = (x, y)
                elif tile == ".":
                    empty_spaces.add((x, y))
    return start, end, empty_spaces


def dijkstras_algorithm(start_position, graph):
    """
    Implements a variation of Dijkstra's algorithm to navigate a grid-like graph.

    Args:
        start_position (tuple): Starting coordinates as a tuple (x, y).
        graph (set): A set of valid positions in the grid represented as (x, y) tuples.

    Returns:
        dict: A dictionary where keys are ((x, y), direction) tuples, representing the position and orientation,
              and values are the cost to reach that state.
    """

    # Movement deltas for each direction.
    direction_deltas = {
        ">": (1, 0),   # Move right
        "v": (0, 1),   # Move down
        "<": (-1, 0),  # Move left
        "^": (0, -1)   # Move up
    }

    # Circular ordering of directions to handle turning.
    direction_order = ">v<^"

    # Priority queue for nodes to visit, initialized with the start position and direction.
    nodes_to_visit = []
    # Dictionary to track the minimum cost to reach each position and direction.
    visited_states = {
        (start_position, ">"): 0,  # Starting position facing right with zero cost.
    }

    # Push the initial state to the priority queue.
    heapq.heappush(nodes_to_visit, (0, ">", start_position))

    while nodes_to_visit:
        # Get the node with the smallest cost (Dijkstra's core idea).
        current_cost, current_direction, (current_x, current_y) = heapq.heappop(nodes_to_visit)

        # Skip processing if this state has already been visited with a lower cost.
        if ((current_x, current_y), current_direction) in visited_states \
                and visited_states[((current_x, current_y), current_direction)] < current_cost:
            continue

        # Determine the movement delta for the current direction.
        delta_x, delta_y = direction_deltas[current_direction]

        # Attempt to move forward in the current direction. (Cost: 1)
        next_position = (current_x + delta_x, current_y + delta_y)
        if next_position in graph:  # Check if the next position is valid.
            if (next_position, current_direction) not in visited_states \
                    or visited_states[(next_position, current_direction)] > current_cost + 1:
                visited_states[(next_position, current_direction)] = current_cost + 1
                heapq.heappush(nodes_to_visit, (current_cost + 1, current_direction, next_position))

        # Attempt to turn left (-1) or right (+1). (Cost: 1000)
        for turn in [-1, 1]:
            new_direction = direction_order[(direction_order.index(current_direction) + turn) % 4]
            if ((current_x, current_y), new_direction) not in visited_states \
                    or visited_states[((current_x, current_y), new_direction)] > current_cost + 1000:
                visited_states[((current_x, current_y), new_direction)] = current_cost + 1000
                heapq.heappush(nodes_to_visit, (current_cost + 1000, new_direction, (current_x, current_y)))

    return visited_states


def trace_back(visited_states, target_state):
    """
    Traces back all reachable states from a given target state in a grid-based graph.

    Args:
        visited_states (dict): A dictionary where keys are ((x, y), direction) tuples and
                              values are the cost to reach that state.
        target_state (tuple): The target state as a tuple ((x, y), direction).

    Returns:
        set: A set of all positions (x, y) that are reachable from the target state.
    """
    # Movement deltas for each direction, mapping the direction character to coordinate changes.
    direction_deltas = {
        ">": (1, 0),   # Move right
        "v": (0, 1),   # Move down
        "<": (-1, 0),  # Move left
        "^": (0, -1)   # Move up
    }

    # Circular order of directions to facilitate left or right turns.
    direction_order = ">v<^"

    # Initialize the queue with the target state and a set to track visited positions.
    states_to_process = [target_state]
    reachable_positions = set()

    while states_to_process:
        # Pop the next state to process from the queue.
        current_position, current_direction = states_to_process.pop(0)

        # Add the current position to the set of reachable positions.
        reachable_positions.add(current_position)

        # Attempt to trace back to the previous state by moving backward.
        delta_x, delta_y = direction_deltas[current_direction]
        previous_position = (current_position[0] - delta_x, current_position[1] - delta_y)

        if (previous_position, current_direction) in visited_states \
                and visited_states[(previous_position, current_direction)] + 1 == visited_states[(current_position, current_direction)]:
            states_to_process.append((previous_position, current_direction))

        # Attempt to trace back by rotating left or right.
        for turn in [1, -1]:
            new_direction = direction_order[(direction_order.index(current_direction) + turn) % 4]

            if (current_position, new_direction) in visited_states \
                    and visited_states[(current_position, new_direction)] + 1000 == visited_states[(current_position, current_direction)]:
                states_to_process.append((current_position, new_direction))

    return reachable_positions


@performance_profiler
def solve_day_16(start, end, graph):
    visited = dijkstras_algorithm(start, frozenset(graph))

    # Back track from end with lowest cost
    target_score = min(v for k, v in visited.items() if k[0] == end)
    target_state = [k for k, v in visited.items() if v == target_score and k[0] == end]

    return target_score, len(trace_back(visited, target_state[0]))


if __name__ == "__main__":
    start_node, end_node, graph = parse_input("input.txt")
    p1, p2 = solve_day_16(start_node, end_node, graph)
    print("Part 1:", p1)
    print("Part 2:", p2)
