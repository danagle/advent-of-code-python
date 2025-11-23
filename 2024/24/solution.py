"""
Advent of Code 2024
Day 24: Crossed Wires
https://adventofcode.com/2024/day/24
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Gate:
    a: str
    op: str
    b: str
    output: str


def parse_input(filepath: str) -> Tuple[Dict[str, Optional[int]], List[Gate]]:
    lines = Path(filepath).read_text().splitlines()
    # split at first blank line
    blank_index = lines.index("")
    wire_lines = lines[:blank_index]
    gate_lines = lines[blank_index + 1 :]

    wires: Dict[str, Optional[int]] = {}
    gates: List[Gate] = []

    for line in wire_lines:
        name, val = line.split(": ")
        wires[name] = int(val)

    for line in gate_lines:
        expr, out = line.split(" -> ")
        a, op, b = expr.split(" ")
        gates.append(Gate(a=a, op=op, b=b, output=out))
        # ensure all wires exist in the map
        wires.setdefault(a, None)
        wires.setdefault(b, None)
        wires.setdefault(out, None)

    return wires, gates


def evaluate_circuit(wires: Dict[str, Optional[int]], gates: List[Gate]) -> int:
    # Evaluate until all z-wires are filled
    while any(name.startswith("z") and val is None for name, val in wires.items()):
        for g in gates:
            if wires[g.a] is None or wires[g.b] is None:
                continue
            a, b = wires[g.a], wires[g.b]
            if g.op == "AND":
                wires[g.output] = a & b
            elif g.op == "OR":
                wires[g.output] = a | b
            elif g.op == "XOR":
                wires[g.output] = a ^ b

    # collect z wires sorted descending by name (z45 ... z00)
    z_list = sorted(((name, wires[name]) for name in wires if name.startswith("z")), key=lambda x: x[0], reverse=True)
    bit_str = "".join(str(val) for _, val in z_list)
    return int(bit_str, 2)


def find_gate(a: str, b: str, operator: str, gates: List[Gate]) -> str:
    """Return the output name of the gate matching inputs (a,b) and operator (order-insensitive)."""
    for g in gates:
        if g.op != operator:
            continue
        if (g.a == a and g.b == b) or (g.a == b and g.b == a):
            return g.output
    return ""


def swapped_wires(gates: List[Gate]) -> str:
    """
    Scan the 45-bit adder stages, discover swapped outputs by checking presence/
    absence of expected gates and record swaps.
    """
    swapped: List[str] = []
    c0 = ""  # previous carry wire name, empty string if none

    for i in range(45):
        n = f"{i:02d}"
        # find XOR and AND between x[n] and y[n]
        m1 = find_gate(f"x{n}", f"y{n}", "XOR", gates)  # sum without carry
        n1 = find_gate(f"x{n}", f"y{n}", "AND", gates)  # initial carry bit
        r1 = ""
        z1 = ""
        c1 = ""

        if c0 != "":
            # find AND between previous carry and current sum candidate
            r1 = find_gate(c0, m1, "AND", gates)
            if r1 == "":
                # XOR/AND pair reversed — swap m1 and n1 (post-swap append)
                m1, n1 = n1, m1
                swapped.append(m1)
                swapped.append(n1)
                # re-find r1 after swap
                r1 = find_gate(c0, m1, "AND", gates)

            # find XOR between previous carry and current m1
            z1 = find_gate(c0, m1, "XOR", gates)

            # If m1 is actually a z-wire, swap m1 and z1 (post-swap append)
            if m1.startswith("z"):
                m1, z1 = z1, m1
                swapped.append(m1)
                swapped.append(z1)

            # If n1 is actually a z-wire, swap n1 and z1 (post-swap append)
            if n1.startswith("z"):
                n1, z1 = z1, n1
                swapped.append(n1)
                swapped.append(z1)

            # If r1 is actually a z-wire, swap r1 and z1 (post-swap append)
            if r1.startswith("z"):
                r1, z1 = z1, r1
                swapped.append(r1)
                swapped.append(z1)

            # find the OR gate combining r1 and n1 to produce the carry out
            c1 = find_gate(r1, n1, "OR", gates)

        # If the carry-out looks like a z-wire and it's not the final z45,
        # swap carry and z (post-swap append)
        if c1.startswith("z") and c1 != "z45":
            c1, z1 = z1, c1
            swapped.append(c1)
            swapped.append(z1)

        # propagate carry
        if c0 == "":
            c0 = n1
        else:
            c0 = c1

    swapped.sort()
    return ",".join(swapped)


if __name__ == "__main__":
    wires, gates = parse_input("input.txt")

    p1 = evaluate_circuit(dict(wires), gates)  # pass a copy of wires
    print("Part 1:", p1)

    p2 = swapped_wires(gates)
    print("Part 2:", p2)
