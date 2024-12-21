"""
Advent of Code 2024
Day 21: Keypad Conundrum
https://adventofcode.com/2024/day/21
"""
from collections import Counter
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


def calculate_manhattan_distance(point1, point2):
    """
    Calculate the Manhattan distance between two complex number points.
    
    Args:
        point1 (complex): First point in complex plane
        point2 (complex): Second point in complex plane
    
    Returns:
        float: Manhattan distance between the points
    """
    return abs(point1.real - point2.real) + abs(point1.imag - point2.imag)


def create_keypad_mapping(keypad_layout):
    """
    Convert a string representation of a keypad into a dictionary mapping characters to complex coordinates.
    
    Args:
        keypad_layout (str): Comma-separated string representing keypad layout
        
    Returns:
        dict: Mapping of characters to their complex number positions
    """
    return {
        char: row_idx + 1j * col_idx
        for row_idx, row in enumerate(keypad_layout.split(','))
        for col_idx, char in enumerate(row)
        if char != '_'
    }


def find_shortest_paths(start_pos, end_pos, keypad):
    """
    Find all shortest paths between two positions using DFS.
    
    Args:
        start_pos (complex): Starting position
        end_pos (complex): Target position
        keypad (dict): Mapping of valid positions
        
    Returns:
        list: List of possible direction sequences to reach the target
    """
    exploration_stack = [(start_pos, [])]
    valid_paths = []
    directions = (1, -1, 1j, -1j)
    direction_to_symbol = {1: 'v', -1: '^', 1j: '>', -1j: '<'}
    
    while exploration_stack:
        current_pos, path = exploration_stack.pop()
        
        if current_pos == end_pos:
            valid_paths.append(path)
            continue
            
        for direction in directions:
            next_pos = current_pos + direction
            if (calculate_manhattan_distance(next_pos, end_pos) >= 
                calculate_manhattan_distance(current_pos, end_pos) or 
                next_pos not in keypad.values()):
                continue
            exploration_stack.append((next_pos, path + [direction]))

    return [''.join(direction_to_symbol[d] for d in path) for path in valid_paths]


def generate_input_sequences(sequence, keypad):
    """
    Generate all possible shortest input sequences to type a given sequence on the keypad.
    
    Args:
        sequence (str): Target sequence to type
        keypad (dict): Keypad layout mapping
        
    Returns:
        list: All possible shortest input sequences
    """
    sequence = 'A' + sequence
    current_paths = ['']
    
    for i in range(len(sequence)-1):
        new_paths = []
        for current_path in current_paths:
            for shortest_path in find_shortest_paths(
                keypad[sequence[i]], 
                keypad[sequence[i+1]], 
                keypad
            ):
                new_paths.append(current_path + shortest_path + 'A')
        current_paths = new_paths
        
    return current_paths


def find_optimal_sequences(sequences, keypad):
    """
    Find all possible sequences of minimum length to type any of the given sequences.
    
    Args:
        sequences (list): List of (character, sequence) tuples
        keypad (dict): Keypad layout mapping
        
    Returns:
        list: Optimal sequences with minimum length
    """
    def calculate_sequence_length(seq):
        return sum(calculate_manhattan_distance(
            keypad[seq[i]], keypad[seq[i+1]]
        ) for i in range(len(seq)-1))

    min_length = float('inf')
    min_length_sequences = []
    
    for char, seq in sequences:
        current_length = calculate_sequence_length(seq)
        if current_length < min_length:
            min_length_sequences = [(char, seq)]
            min_length = current_length
        elif current_length == min_length:
            min_length_sequences.append((char, seq))

    return [
        (char, x) 
        for char, seq in min_length_sequences
        for x in generate_input_sequences(seq, keypad)
    ]


def precalculate_best_paths(direction_keypad):
    """
    Precalculate optimal paths between all direction pairs.
    
    Args:
        direction_keypad (dict): Direction keypad layout
        
    Returns:
        dict: Mapping of direction pairs to their optimal paths
    """
    valid_directions = "^<>vA"
    best_paths = {}
    
    for dir1 in valid_directions:
        for dir2 in valid_directions:
            paths = [(x, x) for x in find_shortest_paths(
                direction_keypad[dir1],
                direction_keypad[dir2],
                direction_keypad
            )]
            
            while len(set(x for x, _ in paths)) != 1:
                paths = find_optimal_sequences(paths, direction_keypad)
                
            best_paths[(dir1, dir2)] = paths[0][0]
            
    return best_paths


def optimize_sequence(sequence_data, best_paths):
    """
    Optimize the given sequence using pre-calculated best paths.
    
    Args:
        sequence_data (tuple): Tuple of (transitions Counter, first character)
        best_paths (dict): Precalculated optimal paths
        
    Returns:
        tuple: Optimized sequence data
    """
    transitions, first_char = sequence_data
    optimized_transitions = Counter()
    
    start_sequence = best_paths[('A', first_char)] + 'A'
    new_first_char = start_sequence[0]
    transitions[('A', first_char)] += 1
    optimized_transitions[('A', new_first_char)] -= 1
    
    for (char1, char2), count in transitions.items():
        path = 'A' + best_paths[(char1, char2)] + 'A'
        for i in range(len(path) - 1):
            optimized_transitions[(path[i], path[i+1])] += count

    return (optimized_transitions, new_first_char)


def convert_to_transition_counter(sequence):
    """
    Convert a sequence into a Counter of character transitions.
    
    Args:
        sequence (str): Input sequence
        
    Returns:
        tuple: (Counter of transitions, first character)
    """
    transitions = Counter()
    for i in range(len(sequence)-1):
        transitions[(sequence[i], sequence[i+1])] += 1
    return (transitions, sequence[0])


def solve_sequence(sequence, number_keypad, best_paths, iterations):
    """
    Solve the sequence optimization for given number of iterations.
    
    Args:
        sequence (str): Input sequence
        number_keypad (dict): Number keypad layout
        best_paths (dict): Precalculated optimal paths
        iterations (int): Number of optimization iterations
        
    Returns:
        int: Minimum number of steps required
    """
    sequences = [convert_to_transition_counter(seq) 
                for seq in generate_input_sequences(sequence, number_keypad)]
    
    for _ in range(iterations):
        sequences = [optimize_sequence(seq, best_paths) for seq in sequences]

    return min(sum(seq[0].values()) + 1 for seq in sequences)


@performance_profiler
def solve_day_21(codes):
    """
    Process input and solve for both parts of the problem.
    
    Args:
        codes (List[str]): List of codes
        
    Returns:
        tuple: Results for part 1 and part 2
    """
    # Create keypad mappings
    number_keypad = create_keypad_mapping("789,456,123,_0A")
    direction_keypad = create_keypad_mapping("_^A,<v>")
    
    # Precalculate optimal paths
    best_paths = precalculate_best_paths(direction_keypad)
    
    # Initialize results
    part1 = part2 = 0
    
    # Calculate results for each code
    for code in codes:
        multiplier = int(code[:3])
        part1 += int(multiplier * solve_sequence(code, number_keypad, best_paths, 2))
        part2 += int(multiplier * solve_sequence(code, number_keypad, best_paths, 25))

    return part1, part2


def parse_input(file_path):
    with open(file_path, "r") as f:
        lines = f.read().strip().splitlines()
    return lines


if __name__ == "__main__":
    codes = parse_input("input.txt")
    p1, p2 = solve_day_21(codes)
    print(f"Part 1:", p1)
    print(f"Part 2:", p2)
