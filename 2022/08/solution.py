# Day 8: Treetop Tree House

from copy import deepcopy
from pathlib import Path
from typing import List


def read_input_file(filepath: str = "input.txt") -> List[List[int]]:
    """
    Read the input file and return a grid of tree heights as a 2D list of integers.
    """
    grid = []
    for line in Path(filepath).read_text().strip().splitlines():
        grid.append(list(map(int, line)))
    return grid


def part_one(grid: List[List[int]]) -> int:
    """
    Count the number of trees visible from outside the grid.
    A tree is visible if it's taller than all trees in at least one direction.
    """
    visible_trees = set()
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            # Border trees are always visible
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                visible_trees.add((x, y))
            else:
                current_height = grid[y][x]

                # Trees in each direction
                trees_left = grid[y][:x]
                trees_right = grid[y][x + 1:]
                trees_above = [row[x] for row in grid[:y]]
                trees_below = [row[x] for row in grid[y + 1:]]

                # Check visibility in any direction
                if (
                    all(tree < current_height for tree in trees_left)
                    or all(tree < current_height for tree in trees_right)
                    or all(tree < current_height for tree in trees_above)
                    or all(tree < current_height for tree in trees_below)
                ):
                    visible_trees.add((x, y))

    return len(visible_trees)


def calculate_view_distance(current_height: int, line_of_sight: List[int]) -> int:
    """
    Calculate the viewing distance in one direction
    until a tree of equal or greater height is encountered.
    """
    distance = 0
    for tree_height in line_of_sight:
        distance += 1
        if tree_height >= current_height:
            break
    return distance


def part_two(grid: List[List[int]]) -> int:
    """
    Compute the highest scenic score for any tree.
    The scenic score is the product of view distances in all four directions.
    """
    height = len(grid)
    width = len(grid[0])
    scenic_scores = deepcopy(grid)

    for y in range(height):
        for x in range(width):
            current_height = grid[y][x]

            # Extract directional slices
            trees_left = grid[y][:x][::-1]  # Reverse for proper direction
            trees_right = grid[y][x + 1:]
            trees_above = [row[x] for row in grid[:y]][::-1]
            trees_below = [row[x] for row in grid[y + 1:]]

            scenic_scores[y][x] = (
                calculate_view_distance(current_height, trees_left)
                * calculate_view_distance(current_height, trees_right)
                * calculate_view_distance(current_height, trees_above)
                * calculate_view_distance(current_height, trees_below)
            )

    return max(map(max, scenic_scores))


if __name__ == "__main__":
    tree_grid = read_input_file()
    print("Part 1:", part_one(tree_grid))
    print("Part 2:", part_two(tree_grid))
