"""
Advent of Code 2024
Day 4: Ceres Search
https://adventofcode.com/2024/day/4
"""

def read_input(file_path):
    # Initialize the grid as a dictionary mapping (x, y) points to characters
    grid = {}
    with open("input.txt", "r") as f:
        input = f.read().replace("\r\n", "\n").strip()
        for y, line in enumerate(input.split("\n")):
            for x, char in enumerate(line):
                grid[(x, y)] = char
    return grid


def day04(grid):

    # Helper function to get adjacent sequences of characters from the grid
    def adjacent(pos, length):
        # Directions for the 8 neighbors: diagonals and cardinal directions
        directions = [
            (-1, -1), (1, -1), (1, 1), (-1, 1),  # Diagonals
            (0, -1), (1, 0), (0, 1), (-1, 0),   # Cardinal directions
        ]

        # Create a list to hold strings for each direction
        text_strings = [""] * len(directions)

        for i, (dx, dy) in enumerate(directions):
            for step in range(length):
                # Calculate the new position by adding the direction multiplied by step
                point = (pos[0] + (dx * step), pos[1] + (dy * step))
                # Append the character at that point if it exists in the grid
                if point in grid:
                    text_strings[i] += str(grid[point])
                else:
                    break  # Stop if the point is out of bounds
        return text_strings

    def x_mas_check(pos):
        """
        There are 4 possible character patterns:

        M_M   M_S   S_S   S_M   
        _A_   _A_   _A_   _A_
        S_S   M_S   M_M   S_M
        """
        offsets = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        character_patterns = set(["MMSS", "MSSM", "SSMM", "SMMS"])
        if grid[pos] == "A" and all((pos[0]+off[0], pos[1]+off[1]) in grid for off in offsets):
            check_str = "".join([grid[(pos[0]+off[0], pos[1]+off[1])] for off in offsets])
            return check_str in character_patterns
        return False

    # Part One and Part Two results
    part1, part2 = 0, 0

    # Iterate through all points in the grid
    for p in grid.keys():
        # Part One: Count occurrences of "XMAS" in all directions (length 4)
        part1 += sum("XMAS" in s for s in adjacent(p, 4))
        # Part Two: Count occurrences X-MAS patterns
        part2 += x_mas_check(p)

    return part1, part2


if __name__ == "__main__":
    input_grid = read_input("input.txt")
    p1, p2 = day04(input_grid)
    # Print results
    print("Part One:", p1)
    print("Part Two:", p2)
