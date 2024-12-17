"""
Advent of Code 2024
Day 17: Chronospatial Computer
https://adventofcode.com/2024/day/17
"""
import re

def extract_integers(text):
    """
    Extract all integers (including negative) from a given text string.
    
    Args:
        text (str): Input text to extract integers from.
    
    Returns:
        list: List of integers found in the text.
    """
    return [int(x) for x in re.findall(r"-?\d+", text)]


def parse_input_file(file_path):
    """
    Parse input file containing register values and program instructions.
    
    Args:
        file_path (str): Path to the input file.
    
    Returns:
        tuple: A tuple containing (register_values, program_instructions)
    """
    with open(file_path, "r") as file:
        raw_text = file.read().strip()
    
    # Split input into register values and program instructions
    raw_registers, raw_program = raw_text.split("\n\n")
    register_values = extract_integers(raw_registers)
    
    # Extract program instructions
    program_instructions = raw_program.split(":")[1].strip().split(",")
    program_instructions = [int(x) for x in program_instructions]
    
    return register_values, program_instructions


def select_combination_value(valueA, valueB, valueC, selection_index):
    """
    Select a value based on a specific index and input values.
    
    Args:
        valueA (int): First input value.
        valueB (int): Second input value.
        valueC (int): Third input value.
        selection_index (int): Index used to determine which value to return.
    
    Returns:
        int or None: Selected value based on the index.
    """
    if selection_index < 4:
        return selection_index
    if selection_index == 4:
        return valueA
    if selection_index == 5:
        return valueB
    if selection_index == 6:
        return valueC
    return None


def execute_instruction(valueA, valueB, valueC, instruction_pointer, program):
    """
    Execute a single instruction in the program.
    
    Args:
        valueA (int): 'A' register value.
        valueB (int): 'B' register value.
        valueC (int): 'C' register value.
        instruction_pointer (int): Current position in the program.
        program (list): List of program instructions.
    
    Returns:
        tuple: Updated register values and instruction pointer.
    """
    opcode = program[instruction_pointer]
    argument = program[instruction_pointer + 1]
    combination_value = select_combination_value(valueA, valueB, valueC, argument)
    
    # Complex instructions with multiple operations
    if opcode == 0:
        # Integer division using power of 2
        return (None, valueA // pow(2, combination_value), valueB, valueC, instruction_pointer + 2)
    elif opcode == 1:
        # Bitwise XOR operation
        return (None, valueA, valueB ^ argument, valueC, instruction_pointer + 2)
    elif opcode == 2:
        # Modulo operation
        return (None, valueA, combination_value % 8, valueC, instruction_pointer + 2)
    elif opcode == 3:
        # Conditional jump
        return (None, valueA, valueB, valueC, argument if valueA != 0 else instruction_pointer + 2)
    elif opcode == 4:
        # Another bitwise XOR operation
        return (None, valueA, valueB ^ valueC, valueC, instruction_pointer + 2)
    elif opcode == 5:
        # Output generation
        return (combination_value % 8, valueA, valueB, valueC, instruction_pointer + 2)
    elif opcode == 6:
        # Integer division for second value
        return (None, valueA, valueA // pow(2, combination_value), valueC, instruction_pointer + 2)
    elif opcode == 7:
        # Integer division for third value
        return (None, valueA, valueB, valueC // pow(2, combination_value), instruction_pointer + 2)


def run_program(registerA, registerB, registerC, program):
    """
    Execute the entire program and collect output values.
    
    Args:
        registerA (int): Initial register A value.
        registerB (int): Initial register B value.
        registerC (int): Initial register C value.
        program (list): List of program instructions.
    
    Returns:
        list: Collected output values during program execution.
    """
    instruction_pointer = 0
    output_values = []
    
    while instruction_pointer < len(program) - 1:
        # Execute instruction and update state
        output, registerA, registerB, registerC, instruction_pointer = execute_instruction(
            registerA, registerB, registerC, instruction_pointer, program
        )

        if output is not None:
            output_values.append(output)
    
    return output_values


def find_best_input(program, cursor, current_value):
    """
    Recursively find the best input that generates a specific program output.
    
    Args:
        program (list): List of program instructions.
        cursor (int): Current position in the program to match.
        current_value (int): Current accumulated value.
    
    Returns:
        int or None: Best input value that matches program requirements.
    """
    for candidate in range(8):
        registerA = current_value * 8 + candidate
        # Check if running the program with candidate produces expected output
        if run_program(registerA, 0, 0, program) == program[cursor:]:
            if cursor == 0:
                return registerA
            
            # Recursive call to find previous best input
            result = find_best_input(program, cursor - 1, registerA)
            if result is not None:
                #print(candidate, registerA)
                return result
    
    return None


def solve_day_17(registers, program):
    registerA, registerB, registerC = registers
    
    # Part 1: Print program output
    print(",".join([str(x) for x in run_program(registerA, registerB, registerC, program)]))
    
    # Part 2: Find best input
    best_input = find_best_input(program, len(program) - 1, 0)
    print(best_input)


if __name__ == "__main__":
    registers, program = parse_input_file("input.txt")
    solve_day_17(registers, program)
