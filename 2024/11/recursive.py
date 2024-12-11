import functools
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


def parse_input(file_path):
    with open(file_path, "r") as f:
        stones = f.read().strip().split()
    return stones


@functools.cache
def count(num, blink, is_part2=False):
    exit_blink = 25
    if is_part2:
        exit_blink = 75
    if blink == exit_blink:
        return 1
    # Rule 1
    # If the stone is engraved with the number 0,
    # it is replaced by a stone engraved with the number 1.
    if num == 0:
        return count(1, blink+1, is_part2)
    num_str = str(num)
    num_len = len(num_str)
    # Rule 2
    # If the stone is engraved with a number that has an even number
    # of digits, it is replaced by two stones.
    # The left half of the digits are engraved on the new left stone,
    # and the right half of the digits are engraved on the new right stone.
    if num_len % 2 == 0:
        return (count(int(num_str[:num_len//2]), blink+1, is_part2) +
                count(int(num_str[num_len//2:]), blink+1, is_part2))
    # Rule 3
    # If none of the other rules apply, the stone is replaced by a new stone;
    # the old stone's number multiplied by 2024 is engraved on the new stone.
    return count(num*2024, blink+1, is_part2)


@performance_profiler
def part_one(stones):
    return sum(count(int( n ), 0, False) for n in stones)


@performance_profiler
def part_two(stones):
    return sum(count(int( n ), 0, True) for n in stones)


if __name__ == "__main__":
    numbers = parse_input("input.txt")

    print("Part 1:", part_one(numbers))
    print("Part 2:", part_two(numbers))
