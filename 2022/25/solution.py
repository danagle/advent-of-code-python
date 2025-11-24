# Day 25: Full of Hot Air


def parse_snafu(s: str):
    """Convert a SNAFU-encoded string into a list of digit values (least significant first)."""
    mapping = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2,
    }
    # Reverse the string so index positions match powers of 5
    return [mapping[c] for c in reversed(s)]


def encode_snafu(v):
    """Convert a list of SNAFU digit values back into its string representation."""
    mapping = {
        2: '2',
        1: '1',
        0: '0',
        -1: '-',
        -2: '=',
    }
    # Reverse digits to restore normal left‑to‑right ordering
    return "".join(mapping[i] for i in reversed(v))


def to_int(v):
    """Convert a list of SNAFU digit values to a normal integer."""
    number = 0
    
    for i in reversed(v):  # highest place value first
        number *= 5
        number += i
    
    return number


def to_snafu(n: int):
    """Convert an integer into SNAFU digit form."""
    if n == 0:
        return [0]

    s = []
    while n != 0:
        r = n % 5
        # Map standard base‑5 remainders into SNAFU's balanced digit system
        if r in (0, 1, 2):
            a = r
        elif r in (3, 4):
            # 3 → -2, 4 → -1 (balanced representation)
            a = r - 5
        else:
            raise RuntimeError("unreachable")

        s.append(a)
        # Remove the chosen digit and continue
        n -= a
        n //= 5

    return s


def part_one():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    # Convert each SNAFU line to an int, sum them, re‑encode as SNAFU
    total = sum(to_int(parse_snafu(line)) for line in lines)

    print("Part 1:", encode_snafu(to_snafu(total)))


if __name__ == "__main__":
    part_one()
