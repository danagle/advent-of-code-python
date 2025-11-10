# Day 7: No Space Left On Device

from collections import defaultdict
from pathlib import Path
from typing import Dict


def read_input_file(filepath: str = "input.txt") -> Dict[Path, int]:
    """
    Parse the filesystem commands and file listings from the input file.
    Returns a mapping from each folder path to its cumulative size.
    """
    current_dir = Path("/")
    file_sizes = {}

    for line in Path(filepath).read_text().strip().splitlines():
        if line.startswith("$"):
            # Handle directory navigation commands
            if " cd " in line:
                target = line.split()[2]
                if target == "/":
                    current_dir = Path("/")
                elif target == "..":
                    current_dir = current_dir.parent
                else:
                    current_dir = (current_dir / target).resolve()
        else:
            # Handle file entries (ignore directories)
            if not line.startswith("dir"):
                size_str, filename = line.split()
                file_path = (current_dir / filename).resolve()
                file_sizes[file_path] = int(size_str)

    # Compute folder sizes by aggregating file sizes up the directory tree
    folder_sizes = defaultdict(int)
    for file_path, size in file_sizes.items():
        parent_dir = file_path.parent
        while True:
            folder_sizes[parent_dir] += size
            if parent_dir == Path("/"):
                break
            parent_dir = parent_dir.parent

    return folder_sizes


def part_one(folder_sizes: Dict[Path, int]) -> int:
    """
    Sum of the total sizes of directories with size <= 100,000.
    """
    return sum(size for size in folder_sizes.values() if size <= 100_000)


def part_two(folder_sizes: Dict[Path, int]) -> int:
    """
    Find the smallest directory that can be deleted to free up enough space.
    """
    total_disk_space = 70_000_000
    required_free_space = 30_000_000

    used_space = folder_sizes[Path("/")]
    min_space_to_free = required_free_space - (total_disk_space - used_space)

    for folder_size in sorted(folder_sizes.values()):
        if folder_size > min_space_to_free:
            return folder_size
    raise ValueError("No folder large enough to free the required space.")


if __name__ == "__main__":
    folder_sizes = read_input_file()
    print("Part 1:", part_one(folder_sizes))
    print("Part 2:", part_two(folder_sizes))
