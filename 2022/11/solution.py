# Day 11: Monkey in the Middle

import math
from pathlib import Path
from typing import List, Tuple


class Monkey:
    """Represents a single monkey with its items, operation, and throw rules."""

    def __init__(self, description: str):
        """Parse the monkey definition block from the input."""
        self.items: List[int] = []
        self.operation: Tuple[str, str] = ("", "")
        self.test_divisor: int = 1
        self.if_true_target: int = -1
        self.if_false_target: int = -1
        self.activity_count: int = 0

        for line in description.splitlines():
            line = line.strip()
            if line.startswith("Starting items:"):
                self.items = list(map(int, line.replace("Starting items:", "").replace(",", "").split()))
            elif line.startswith("Operation:"):
                _, _, _, _, op, value = line.split()
                self.operation = (op, value)
            elif line.startswith("Test:"):
                self.test_divisor = int(line.split()[-1])
            elif line.startswith("If true:"):
                self.if_true_target = int(line.split()[-1])
            elif line.startswith("If false:"):
                self.if_false_target = int(line.split()[-1])

    def inspect_items(self, reduce_worry: bool = True) -> List[Tuple[int, int]]:
        """
        Perform a round of inspections.
        Returns a list of (target_monkey_index, new_item_value).
        """
        throw_list = []

        for old_value in self.items:
            self.activity_count += 1

            # Compute new worry level safely
            operand = old_value if self.operation[1] == "old" else int(self.operation[1])
            if self.operation[0] == "+":
                new_value = old_value + operand
            elif self.operation[0] == "*":
                new_value = old_value * operand
            else:
                raise ValueError(f"Unsupported operation: {self.operation}")

            if reduce_worry:
                new_value //= 3  # Part 1 rule

            target = self.if_true_target if new_value % self.test_divisor == 0 else self.if_false_target
            throw_list.append((target, new_value))

        # Clear items after inspection
        self.items.clear()
        return throw_list


def read_input_file(filepath: str = "input.txt") -> List[Monkey]:
    """Read and parse all monkeys from the input file."""
    content = Path(filepath).read_text().strip()
    return [Monkey(block) for block in content.split("\n\n")]


def part_one(monkeys: List[Monkey], rounds: int = 20) -> int:
    """Simulate 20 rounds of the monkey game."""
    for _ in range(rounds):
        for monkey in monkeys:
            for target, value in monkey.inspect_items(reduce_worry=True):
                monkeys[target].items.append(value)

    monkeys.sort(key=lambda m: m.activity_count, reverse=True)
    return monkeys[0].activity_count * monkeys[1].activity_count


def part_two(monkeys: List[Monkey], rounds: int = 10_000) -> int:
    """Simulate 10,000 rounds using modular arithmetic."""
    modulus = math.prod(m.test_divisor for m in monkeys)

    for _ in range(rounds):
        for monkey in monkeys:
            for target, value in monkey.inspect_items(reduce_worry=False):
                monkeys[target].items.append(value % modulus)

    monkeys.sort(key=lambda m: m.activity_count, reverse=True)
    return monkeys[0].activity_count * monkeys[1].activity_count


if __name__ == "__main__":
    monkeys = read_input_file()
    print("Part 1:", part_one(monkeys))
    # Reload to reset state
    monkeys = read_input_file()
    print("Part 2:", part_two(monkeys))
