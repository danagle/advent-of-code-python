# Day 21: Monkey Math

from typing import Union, Dict, Tuple, Optional

# Expressions are either an integer or a tuple: (left_var, operator, right_var)
Expr = Union[int, Tuple[str, str, str]]


def read_input_file(filename: str = "input.txt") -> Dict[str, Expr]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    nodes = {}

    for line in lines:
        name, expr = line.split(": ")
        if expr.isdigit():
            # A pure digit becomes a constant value
            nodes[name] = int(expr)
        else:
            # Otherwise it's an expression "A + B"
            left, op, right = expr.split()
            nodes[name] = (left, op, right)

    return nodes


def const_propagate(nodes: Dict[str, Expr], node: str, ignore_humn: bool = False) -> Optional[int]:
    """
    Recursively evaluate nodes where possible
    If ignore_humn=True, treat 'humn' as symbolic instead of a constant.
    """
    if node == "humn" and ignore_humn:
        return None  # treat as unknown
    if node == "humn" and not ignore_humn:
        # If humn is a constant, return its value; otherwise default to 0
        return nodes[node] if isinstance(nodes[node], int) else 0

    val = nodes[node]
    if isinstance(val, int):
        return val# already a constant

    left, op, right = val
    
    # Try to evaluate both sides
    l = const_propagate(nodes, left, ignore_humn)
    r = const_propagate(nodes, right, ignore_humn)

    # If both sides are known, apply the operator
    if l is not None and r is not None:
        if op == '+': result = l + r
        elif op == '-': result = l - r
        elif op == '*': result = l * r
        elif op == '/': result = l // r
        else: raise ValueError(f"Unknown op {op}")

        nodes[node] = result  # cache result
        return result

    return None  # cannot fully evaluate


def solve_for_humn(nodes: Dict[str, Expr], node: str, target: int) -> int:
    """Solve the symbolic equation for humn by walking the tree."""
    if node == "humn":
        return target  # the solved value

    left, op, right = nodes[node]

    # Evaluate both sides ignoring humn
    l_val = const_propagate(nodes, left, ignore_humn=True)
    r_val = const_propagate(nodes, right, ignore_humn=True)

    if l_val is not None:
        # If left is fully known, solve for the right side
        if op == '+': return solve_for_humn(nodes, right, target - l_val)
        if op == '-': return solve_for_humn(nodes, right, l_val - target)
        if op == '*': return solve_for_humn(nodes, right, target // l_val)
        if op == '/': return solve_for_humn(nodes, right, l_val // target)
    else:
        # Otherwise solve for the left side
        if op == '+': return solve_for_humn(nodes, left, target - r_val)
        if op == '-': return solve_for_humn(nodes, left, target + r_val)
        if op == '*': return solve_for_humn(nodes, left, target // r_val)
        if op == '/': return solve_for_humn(nodes, left, target * r_val)

    raise ValueError("Cannot solve algebraically for this node")


def part_one(nodes):
    """Part 1: evaluate the root value normally, with humn treated as constant."""
    return const_propagate(nodes, "root", ignore_humn=False)
    

def part_two(nodes):
    """Part 2: treat humn as unknown, evaluate what you can, then solve for humn."""
    root = nodes["root"]

    if isinstance(root, tuple):
        left, _, right = root

        # Try evaluating each side; one should be solvable
        l_val = const_propagate(nodes, left, ignore_humn=True)
        r_val = const_propagate(nodes, right, ignore_humn=True)

        if isinstance(l_val, int):
            result = solve_for_humn(nodes, right, l_val)
        else:
            result = solve_for_humn(nodes, left, r_val)

        return result
    
    return -1  # invalid node structure


if __name__ == "__main__":
    nodes = read_input_file()

    print("Part 1:", part_one(nodes.copy()))
    print("Part 2:", part_two(nodes.copy()))
