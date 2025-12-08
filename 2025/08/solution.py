"""
Advent of Code 2025
Day 8: Playground
https://adventofcode.com/2025/day/8
"""
from itertools import combinations
from pathlib import Path


def read_input_file(filepath="input.txt"):
    """Creates a list of tuples (x, y, z) from the input text file."""
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    return [tuple(map(int, line.strip().split(','))) for line in lines]
    

def euclidean_distance_squared(point1, point2):
    """Computes the distance squared between two junction box coordinates."""
    return sum((coord1 - coord2) ** 2 for coord1, coord2 in zip(point1, point2))


def find_circuit_containing(box, circuits):
    """Find which circuit contains the given junction box."""
    for circuit_id, boxes in circuits.items():
        if box in boxes:
            return circuit_id
    return None


def part_one_and_two(boxes):
    """Creates circuits by connecting the nearest junction boxes."""
    # Each junction box starts as its own circuit
    circuits = {box: {box} for box in boxes}

    # Sort all box pairs by distance (closest first)
    box_pairs = sorted(
        combinations(boxes, 2),
        key=lambda pair: euclidean_distance_squared(pair[0], pair[1])
    )

    # Merge circuits by connecting closest pairs
    for connection_count, (box_a, box_b) in enumerate(box_pairs, start=1):
        # Find which circuits these points belong to
        circuit_a = find_circuit_containing(box_a, circuits)
        circuit_b = find_circuit_containing(box_b, circuits)
        
        # If they're in different circuits, merge them
        if circuit_a != circuit_b:
            circuits[circuit_a] |= circuits[circuit_b]
            del circuits[circuit_b]
        
        if connection_count == 1000:
            # Part 1: multiply together the sizes of the three largest circuits
            circuit_sizes = sorted(len(boxes) for boxes in circuits.values())
            p1 = circuit_sizes[-3] * circuit_sizes[-2] * circuit_sizes[-1]
        
        # When all boxes are in one circuit, we're done
        # Part 2: multiply together the X coordinates of the last two junction boxes
        if len(circuits) == 1:
            p2 = box_a[0] * box_b[0]
            break

    return p1, p2


if __name__ == "__main__":
    junction_boxes = read_input_file()
    p1, p2 = part_one_and_two(junction_boxes)
    print("Part 1:", p1)
    print("Part 2:", p2)
