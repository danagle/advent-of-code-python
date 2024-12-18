"""
Advent of Code 2024
Day 18: RAM Run
https://adventofcode.com/2024/day/18
"""
from itertools import count
import networkx as nx


def read_input(file_path):
    with open(file_path) as f:
        nodes = list(tuple(map(int, l.split(","))) for l in f.read().strip().split("\n"))
    return nodes


def solve_day_18(nodes):
    grid = nx.grid_2d_graph(71, 71)

    for i, p in enumerate(nodes):
        grid.remove_node(p)
        if i == 1023:
            # Part 1
            print("Part 1:", nx.shortest_path_length(grid, (0, 0), (70, 70)))
        elif not nx.has_path(grid, (0, 0), (70, 70)):
            # Part 2
            print("Part 2:", p)
            break


if __name__ == "__main__":
    nodes = read_input("input.txt")
    solve_day_18(nodes)
