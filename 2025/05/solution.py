"""
Advent of Code 2025
Day 5: Cafeteria
https://adventofcode.com/2025/day/5
"""
import sys
import bisect
from time import perf_counter
from typing import List, Tuple

class Timer:
    """Simple timer for tracking performance"""
    def __init__(self):
        self.start_time = perf_counter()
        self.last_checkpoint = self.start_time
    
    def checkpoint(self, label: str) -> str:
        current = perf_counter()
        elapsed = (current - self.last_checkpoint) * 1000
        self.last_checkpoint = current
        return f"{label}: {elapsed:.3f}ms"
    
    def total(self) -> str:
        elapsed = (perf_counter() - self.start_time) * 1000
        return f"Total: {elapsed:.3f}ms"


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge overlapping or adjacent ranges"""
    if len(ranges) <= 1:
        return ranges
    
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        # Check if ranges overlap or are adjacent
        if start <= last_end + 1:
            # Merge by extending the end if necessary
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))
    
    return merged


def id_in_ranges(ranges: List[Tuple[int, int]], value: int) -> bool:
    """Binary search to check if id value falls within any range"""
    if not ranges:
        return False
    
    # Find the rightmost range whose start is <= value
    idx = bisect.bisect_right(ranges, (value, float('inf'))) - 1
    
    # Check if value falls within that range
    if idx >= 0:
        start, end = ranges[idx]
        if start <= value <= end:
            return True
    
    return False


def parse_input(input_text):
    # Split input into ranges and values sections
    sections = input_text.strip().split('\n\n')
    if len(sections) != 2:
        print("Error: Invalid input format", file=sys.stderr)
        return 1
    
    ranges_text, values_text = sections
    
    # Parse ranges (format: "start-end")
    fresh_ranges = []
    for line in ranges_text.strip().split('\n'):
        if '-' in line:
            start, end = line.split('-')
            fresh_ranges.append((int(start), int(end)))
            
    # Parse ingredient ids
    ingredient_ids = [int(line) for line in values_text.strip().split('\n') if line]
    
    return fresh_ranges, ingredient_ids


def main():
    timer = Timer()
    
    # Read all input from stdin
    input_text = sys.stdin.read()
    
    ranges, ids = parse_input(input_text)
    print(timer.checkpoint("Parsing"))
    
    # Sort ranges by start value
    ranges.sort()
    print(timer.checkpoint("Sorting Ranges"))
    
    # Merge overlapping ranges
    ranges = merge_ranges(ranges)
    print(timer.checkpoint("Merging Ranges"))
    
    # Part 1: Count how many values fall within any range
    p1 = sum(id_in_ranges(ranges, id) for id in ids)
    print(f"Part 1 Answer: {p1} - {timer.checkpoint('Part 1')}")
    
    # Part 2: Sum the total size of all ranges
    p2 = sum(end - start + 1 for start, end in ranges)
    print(f"Part 2 Answer: {p2} - {timer.checkpoint('Part 2')}")
    
    print(timer.total())


if __name__ == "__main__":
    main()