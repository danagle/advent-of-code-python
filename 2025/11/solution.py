"""
Advent of Code 2025
Day 11: Reactor
https://adventofcode.com/2025/day/11
"""
from functools import cache
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """
    Reads a network graph from the input file.
    Returns a dictionary mapping each node to its list of adjacent nodes.
    """
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    network = {
        node.strip(): adjacents.strip().split()
        for line in lines
        for node, adjacents in [line.split(':', 1)]
    }
    # Add 'out' key to prevent KeyError exception
    network["out"] = []

    return network


def part_one_and_two(graph):
    """
    Solves both parts by counting distinct paths through the graph.
    
    Part 1: Count all paths from 'you' to 'out'
    Part 2: Count all paths from 'svr' to 'out' that pass through both 'dac' and 'fft'
    """

    @cache
    def paths(node_a, node_b):
        """
        Recursively counts all distinct paths from node_a to node_b.
        
        Base case: If node_b is directly adjacent to node_a, that's 1 path
        Recursive case: Sum paths from each of node_a's neighbors to node_b
        
        Uses @cache to memoize results and avoid redundant calculations
        """
        return (node_b in graph[node_a]) + sum(paths(node, node_b)
                                               for node in graph[node_a])

    # Part 1: Direct path count from 'you' to 'out'
    part1 = paths("you", "out")

    # Part 2: Count paths that go through both intermediate nodes
    # There are two possible orderings: svr->dac->fft->out and svr->fft->dac->out
    # For each ordering, multiply the path counts between consecutive waypoints
    order1 = paths("svr", "dac") * paths("dac", "fft") * paths("fft", "out")
    order2 = paths("svr", "fft") * paths("fft", "dac") * paths("dac", "out")
    part2 = order1 + order2
    
    return part1, part2
    

if __name__ == "__main__":
    network = read_input_file()
    p1, p2 = part_one_and_two(network)
    print("Part 1:", p1)
    print("Part 2:", p2)
