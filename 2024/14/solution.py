"""
Advent of Code 2024
Day 14: Restroom Redoubt
https://adventofcode.com/2024/day/14
"""
import re
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
    with open(file_path, "r") as f:
        robots = [(int(x), int(y), int(vx), int(vy)) for (x, y, vx, vy) in 
                  [re.findall('-?[0-9]+', line) for line in f]]
    return robots


@performance_profiler
def part_one(robots):
    T = 100
    x_max = 101
    y_max = 103
    pos = []
    for r in robots:
        px, py, vx, vy = r
        x_final = (px + vx * T) % x_max
        y_final = (py + vy * T) % y_max
        pos.append((x_final, y_final))

    x_mid = x_max // 2
    y_mid = y_max // 2
    quad = [0, 0, 0, 0]

    for x, y in pos:
        if x < x_mid and y < y_mid:
            quad[0] += 1
        elif x < x_mid and y > y_mid:
            quad[1] += 1
        elif x > x_mid and y < y_mid:
            quad[2] += 1
        elif x > x_mid and y > y_mid:
            quad[3] += 1

    result = 1
    for n in quad:
        result *= n

    return result


@performance_profiler
def part_two(robots):
    T = 0
    x_max = 101
    y_max = 103
    pos = []
    vel = []

    for r in robots:
        px, py, vx, vy = r
        pos.append((px, py))
        vel.append((vx, vy))

    while True:
        unique_positions = set(pos)

        if len(unique_positions) == len(pos):
            break

        for i in range(len(pos)):
            px, py = pos[i]
            vx, vy = vel[i]
            pos[i] = ((px + vx) % x_max, (py + vy) % y_max)

        T += 1

    return T


if __name__ == "__main__":
    robots = parse_input("input.txt")
    p1 = part_one(robots)
    p2 = part_two(robots)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
