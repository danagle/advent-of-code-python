"""
Advent of Code 2024
Day 5: Print Queue
https://adventofcode.com/2024/day/5
"""
from collections import defaultdict

def read_input(file_path):
    with open(file_path, "r") as f:
        input = f.read()

    pages_order, updates = input.split("\n\n")
    page_ordering_rules = defaultdict(set)

    for rule in pages_order.split("\n"):
        if not rule:
            continue
        page_b, page_a = map(int, rule.split("|"))
        page_ordering_rules[page_b].add(page_a)
    
    sequence_list = []
    for sequence in updates.split("\n"):
        if not sequence: 
            continue
        sequence_list.append([int(page) for page in sequence.split(",")])
    
    return page_ordering_rules, sequence_list


def check(page_sequence, rules):
    for i, page in enumerate(page_sequence):
        if page in rules:
            before = rules[page]
            after = set(page_sequence[i+1:])
            for prev_page in before:
                if prev_page in page_sequence and prev_page not in after:
                    return False
    return True


def sort(page_sequence, rules):
    result = []
    seen = set()
    
    while len(result) < len(page_sequence):
        for p in page_sequence:
            if p in seen: 
                continue
            valid = True
            for q, pages_before in rules.items():
                if q not in page_sequence or q in seen: 
                    continue
                if p in pages_before and q not in seen:
                    valid = False
                    break
            if valid:
                result.append(p)
                seen.add(p)
                break
    return result


def day05(rules, sequences):
    part_1 = part_2 = 0
    for seq in sequences:
        middle_index = len(seq) // 2
        if (check(seq, rules)):
            part_1 += seq[middle_index]
        else:
            sorted_seq = sort(seq, rules)
            part_2 += sorted_seq[middle_index]
    return part_1, part_2


if __name__ == "__main__":
    rules, sequence = read_input("input.txt")
    p1, p2 = day05(rules, sequence)
    print("Part 1: ", p1)
    print("Part 2: ", p2)
