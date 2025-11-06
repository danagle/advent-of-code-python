"""
Advent of Code 2020
Day 21: Allergen Assessment
https://adventofcode.com/2020/day/21
"""
from pathlib import Path
from typing import Dict, List, Set, Tuple


def read_input_file(filepath: str = "input.txt") -> List[Tuple[Set[str], Set[str]]]:
    """Parse the input file into a list of (ingredients, allergens) tuples."""
    foods: List[Tuple[Set[str], Set[str]]] = []
    for line in Path(filepath).read_text().strip().splitlines():
        ingredients_part, allergens_part = line.split(" (contains ")
        ingredients = set(ingredients_part.split())
        allergens = set(allergens_part[:-1].split(", "))  # remove trailing ')'
        foods.append((ingredients, allergens))
    return foods


def deduce_allergens(foods: List[Tuple[Set[str], Set[str]]]) -> Dict[str, str]:
    """
    Deduce which ingredient contains which allergen.

    Returns a mapping: {allergen -> ingredient}.
    """
    # Possible ingredients for each allergen
    possible: Dict[str, Set[str]] = {}

    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in possible:
                possible[allergen] &= ingredients
            else:
                possible[allergen] = set(ingredients)

    confirmed: Dict[str, str] = {}

    # Iteratively narrow down allergens with a single possibility
    while possible:
        determined = [a for a, ing in possible.items() if len(ing) == 1]
        if not determined:
            raise RuntimeError("Could not fully resolve allergens — circular ambiguity.")
        for allergen in determined:
            ingredient = next(iter(possible[allergen]))
            confirmed[allergen] = ingredient
            del possible[allergen]
            # Remove that ingredient from all other sets
            for others in possible.values():
                others.discard(ingredient)

    return confirmed


def part_one(foods: List[Tuple[Set[str], Set[str]]], allergen_map: Dict[str, str]) -> int:
    """Count appearances of ingredients that cannot possibly contain any allergen."""
    all_ingredients = [ingredient for ingredients, _ in foods for ingredient in ingredients]
    allergenic = set(allergen_map.values())
    safe = [ing for ing in all_ingredients if ing not in allergenic]
    return len(safe)


def part_two(allergen_map: Dict[str, str]) -> str:
    """Return canonical dangerous ingredient list: allergens sorted alphabetically."""
    return ",".join(
        ingredient for _, ingredient in sorted(allergen_map.items(), key=lambda x: x[0])
    )


if __name__ == "__main__":
    foods = read_input_file()
    allergen_map = deduce_allergens(foods)
    p1 = part_one(foods, allergen_map)
    print("Part 1:", p1)
    p2 = part_two(allergen_map)
    print("Part 2:", p2)
