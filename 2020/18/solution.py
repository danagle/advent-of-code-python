"""
Advent of Code 2020
Day 18: Operation Order
https://adventofcode.com/2020/day/18
"""
from functools import reduce
import operator
from pathlib import Path
from typing import Iterator, List, Union, Callable


def read_input_file(filepath: str = "input.txt") -> List[str]:
    """Read input file and return list of stripped expressions."""
    return Path(filepath).read_text().strip().replace(" ", "").splitlines()


def _apply_operator(stack: List[Union[int, Callable[[int, int], int]]], value: int) -> None:
    """Apply + or * if present on stack, else push value."""
    if stack and callable(stack[-1]):
        op = stack.pop()
        left = stack.pop()
        stack.append(op(left, value))  # type: ignore
    else:
        stack.append(value)


def _apply_addition(stack: List[Union[int, Callable[[int, int], int]]], value: int) -> None:
    """Apply + immediately (since it has higher precedence in part 2)."""
    if stack and stack[-1] == operator.add:
        stack.pop()
        left = stack.pop()
        stack.append(left + value)  # type: ignore
    else:
        stack.append(value)


def _evaluate_multiplication(stack: List[Union[int, Callable[[int, int], int]]]) -> int:
    """Multiply all integer values on the stack (ignore operators)."""
    result = 1
    for v in stack:
        if isinstance(v, int):
            result *= v
    return result


def parse_equal_precedence(expr_iter: Iterator[str]) -> int:
    """Evaluate expression where + and * have equal precedence (Part 1)."""
    stack: List[Union[int, Callable[[int, int], int]]] = []

    for c in expr_iter:
        if c == "(":
            value = parse_equal_precedence(expr_iter)
            _apply_operator(stack, value)
        elif c == ")":
            break
        elif c.isdigit():
            _apply_operator(stack, int(c))
        elif c == "+":
            stack.append(operator.add)
        elif c == "*":
            stack.append(operator.mul)

    return stack[0] if len(stack) == 1 else reduce(lambda a, b: b(a), stack)  # type: ignore


def parse_addition_precedence(expr_iter: Iterator[str]) -> int:
    """Evaluate expression where + has higher precedence than * (Part 2)."""
    stack: List[Union[int, Callable[[int, int], int]]] = []

    for c in expr_iter:
        if c == "(":
            value = parse_addition_precedence(expr_iter)
            _apply_addition(stack, value)
        elif c == ")":
            break
        elif c.isdigit():
            _apply_addition(stack, int(c))
        elif c == "+":
            stack.append(operator.add)
        elif c == "*":
            stack.append(operator.mul)

    return _evaluate_multiplication(stack)


def part_one(expressions: List[str]) -> int:
    """Sum all evaluated expressions (Part 1)."""
    return sum(parse_equal_precedence(iter(expr)) for expr in expressions)


def part_two(expressions: List[str]) -> int:
    """Sum all evaluated expressions (Part 2)."""
    return sum(parse_addition_precedence(iter(expr)) for expr in expressions)


if __name__ == "__main__":
    expressions = read_input_file()
    p1 = part_one(expressions)
    print("Part 1:", p1)
    p2 = part_two(expressions)
    print("Part 2:", p2)
