"""
Advent of Code 2024
Day 9: Disk Fragmenter
https://adventofcode.com/2024/day/9
"""
from collections import deque
from dataclasses import dataclass
from time import perf_counter as measure_time

def performance_profiler(method):
    """
    A decorator that measures and prints the execution time of a method.
    
    Args:
        method (callable): The function to be timed
    
    Returns:
        callable: A wrapper function that measures the method's execution time
    """
    def timing_wrapper(*args, **kwargs):
        start_time = measure_time()
        result = method(*args, **kwargs)
        print(
            f"Method {method.__name__} took: "
            f"{measure_time() - start_time:2.5f} sec"
        )
        return result
    return timing_wrapper


@dataclass
class File:
    """
    Represents a file on the disk with its unique identifier, size, and position.
    
    Attributes:
        id (int): Unique identifier for the file
        size (int): Size of the file in blocks
        position (int): Starting position of the file on the disk
    """
    id: int
    size: int
    position: int


@dataclass
class FreeSpace:
    """
    Represents a free space block on the disk.
    
    Attributes:
        position (int): Starting position of the free space
        size (int): Size of the free space in blocks
    """
    position: int
    size: int


@performance_profiler
def part_one(parsed_input):
    """
    Compact the disk by moving blocks, prioritizing non-None (file) blocks.
    
    Args:
        parsed_input (tuple): Tuple containing files, free spaces, and disk state
    
    Returns:
        int: Checksum of the compacted disk
    """
    files, free_spaces, disk = parsed_input
    compacted = compact_disk_blocks(disk)
    return compute_checksum(compacted)


@performance_profiler
def part_two(parsed_input):
    """
    Compact the disk by moving whole files to free spaces.
    
    Args:
        parsed_input (tuple): Tuple containing files, free spaces, and disk state
    
    Returns:
        int: Checksum of the compacted disk
    """
    files, free_spaces, disk = parsed_input
    compacted = compact_disk_files(files, free_spaces, len(disk))
    return compute_checksum(compacted)


def parse_input(file_path):
    """
    Parse input file to create a representation of the initial disk state.

    The input is expected to be a sequence of alternating file and free space lengths.
    Even indices represent file lengths, odd indices represent free space lengths.

    Args:
        file_path (str): Path to the input file

    Returns:
        Tuple of (files, free_spaces, initial_disk) where:
        - files: List of File objects
        - free_spaces: List of FreeSpace objects
        - initial_disk: List representing initial disk state
    """
    with open(file_path, "r") as f:
        input_content = f.read().strip()

    files = []
    free_spaces = []
    disk = []
    pos = 0
    file_id = 0

    # Parse alternating file and space lengths
    for i, length in enumerate(map(int, input_content)):
        length = int(length)
        if i % 2 == 0:  # File
            # Create a File object and fill disk with file ID
            files.append(File(file_id, length, pos))
            disk.extend([file_id] * length)
            file_id += 1
        else:  # Free space
            # Create a FreeSpace object and fill disk with None
            free_spaces.append(FreeSpace(pos, length))
            disk.extend([None] * length)
        pos += length

    return (files, free_spaces, disk)


def compact_disk_blocks(disk):
    """
    Compact disk for part 1 by moving blocks using a deque.
    
    Strategy:
    1. Move all non-None blocks to the left
    2. Pad the end with None to maintain original disk size
    
    Args:
        disk (list): Initial disk state
    
    Returns:
        list: Compacted disk with non-None blocks moved to the left
    """
    dq = deque(disk)
    result = []

    while dq:
        # Get next block from the left
        block = dq.popleft()
        if block is None:
            # If it's a free space, find the rightmost file block
            while dq and block is None:
                block = dq.pop()
        if block is not None:
            result.append(block)

    # Pad the result with None to maintain disk size
    result.extend([None] * (len(disk) - len(result)))
    return result


def compact_disk_files(files, free_spaces, disk_size):
    """
    Compact disk for part 2 by moving whole files to free spaces.
    
    Strategy:
    1. Process files from highest ID to lowest
    2. Try to move each file to the leftmost compatible free space
    3. If no free space fits the file, keep it in its original position
    
    Args:
        files (list): List of File objects
        free_spaces (list): List of FreeSpace objects
        disk_size (int): Total size of the disk
    
    Returns:
        list: Compacted disk with files moved to optimize space
    """
    result = [None] * disk_size
    spaces = free_spaces.copy()  # Copy to modify safely

    # Process files from highest ID to lowest
    for file in sorted(files, key=lambda x: -x.id):
        moved = False

        # Try to fit file in each free space from left to right
        for i, space in enumerate(spaces):
            if space.position > file.position:
                break
            if space.size >= file.size:
                # Move file to this space
                pos = space.position
                for j in range(file.size):
                    result[pos + j] = file.id

                # Update free space
                spaces[i] = FreeSpace(
                    space.position + file.size, space.size - file.size
                )
                if spaces[i].size == 0:
                    spaces.pop(i)
                moved = True
                break

        if not moved:
            # Keep file in original position
            pos = file.position
            for j in range(file.size):
                result[pos + j] = file.id

    return result


def compute_checksum(disk):
    """
    Compute the checksum by multiplying file IDs with their positions.
    
    Args:
        disk (list): Compacted disk state
    
    Returns:
        int: Checksum calculated as sum of (position * file_id) for non-None blocks
    """
    return sum(pos * file_id for pos, file_id in enumerate(disk) if file_id is not None)


if __name__ == "__main__":
    parsed_input = parse_input("input.txt")

    p1 = part_one(parsed_input)
    p2 = part_two(parsed_input)

    print("Part 1:", p1)
    print("Part 2:", p2)
