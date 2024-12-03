"""
Advent of Code 2024
Day 3: Mull It Over
https://adventofcode.com/2024/day/3
"""
import re

def read_input(file_path):
    with open("input.txt", "r") as f:
        input = f.read()
    return input.replace("\r", "").replace("\n", "")


def evaluate_string(input):
    # A lambda function to perform the multiplication operation
    mul = lambda a, b: a * b
    # At the beginning of the program, mul instructions are enabled.
    useMul = True
    # Regular expression to capture instructions
    r = re.compile("mul\(\d+,\d+\)|do\(\)|don't\(\)")
    
    part_1 = part_2 = 0

    for instr in re.findall(r, input):
        if instr == "do()":
            useMul = True
        elif instr == "don't()":
            useMul = False
        else:
            # Use the 'eval' cheat code!
            result = eval(instr)
            part_1 += result
            if useMul:
                part_2 += result
    
    return part_1, part_2


if __name__ == "__main__":
    input = read_input("input.txt")
    p1, p2 = evaluate_string(input)
    print("Part 1: ", p1)
    print("Part 2: ", p2)
