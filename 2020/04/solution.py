"""
Advent of Code 2020
Day 4: Passport Processing
https://adventofcode.com/2020/day/4
"""

import re
from pathlib import Path


def read_input_file(filename: str):
    """Load and parse the input file into a list of passport dictionaries."""
    data = Path(filename).read_text().strip()
    raw_passports = [block.replace("\n", " ") for block in data.split("\n\n")]
    passports = [dict(field.split(":") for field in p.split()) for p in raw_passports]
    return passports


# Required passport fields
REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def has_required_fields(passport: dict) -> bool:
    """Check that all required fields are present."""
    return REQUIRED_FIELDS.issubset(passport.keys())


def is_valid_passport(passport: dict) -> bool:
    """Validate a passport's fields according to the puzzle rules."""
    try:
        byr = int(passport["byr"])
        iyr = int(passport["iyr"])
        eyr = int(passport["eyr"])
        hgt = passport["hgt"]
        hcl = passport["hcl"]
        ecl = passport["ecl"]
        pid = passport["pid"]

        if not (1920 <= byr <= 2002):
            return False
        if not (2010 <= iyr <= 2020):
            return False
        if not (2020 <= eyr <= 2030):
            return False

        # Validate height
        if hgt.endswith("cm"):
            if not (150 <= int(hgt[:-2]) <= 193):
                return False
        elif hgt.endswith("in"):
            if not (59 <= int(hgt[:-2]) <= 76):
                return False
        else:
            return False

        # Validate hair color, eye color, and passport ID
        if not re.fullmatch(r"#[0-9a-f]{6}", hcl):
            return False
        if ecl not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
            return False
        if not re.fullmatch(r"\d{9}", pid):
            return False

        return True
    except (KeyError, ValueError):
        return False


def part_one(passports):
    """Count passports with all required fields."""
    return sum(has_required_fields(p) for p in passports)


def part_two(passports):
    """Count passports with valid field data."""
    valid_count = sum(
        has_required_fields(p) and is_valid_passport(p)
        for p in passports
    )
    return valid_count


if __name__ == "__main__":
    text = read_input_file("input.txt")
    print(part_one(text))
    print(part_two(text))
