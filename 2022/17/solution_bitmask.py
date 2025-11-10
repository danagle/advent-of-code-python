# Day 17: Pyroclastic Flow

from pathlib import Path

WIDTH = 7

SHAPES = [
    [[1, 1, 1, 1]],                     # Horizontal line
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],  # Plus
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],  # Reverse L
    [[1], [1], [1], [1]],               # Vertical line
    [[1, 1], [1, 1]]                    # Square
]

OFFSETS = [3, 1, 1, 0, 2]  # precomputed bottom offsets (distance from top of 4x4 to "landing row")

def to_bitmask(shape):
    """Convert 2D shape to bitmask rows, top row first."""
    mask = []
    for row in shape:
        bits = 0
        for i, v in enumerate(row):
            if v:
                bits |= 1 << i
        mask.append(bits)
    return mask

MASKS = [to_bitmask(rock) for rock in SHAPES]

class PyroclasticSimulator:
    """Simulates falling rock pieces with jet stream influence."""
    def __init__(self, jets):
        self.rows = []
        self.height = -1
        self.jets = jets
        self.jet_index = 0
        self.shape_index = 0

    def _can_move(self, mask, x, y):
        for i, row_bits in enumerate(mask):
            ry = y - i
            if ry < 0:
                return False
            if ry < len(self.rows) and (self.rows[ry] & (row_bits << x)):
                return False
        return 0 <= x <= WIDTH - max(row_bits.bit_length() for row_bits in mask)

    def _place_rock(self, mask, x, y):
        for i, row_bits in enumerate(mask):
            ry = y - i
            while ry >= len(self.rows):
                self.rows.append(0)
            self.rows[ry] |= row_bits << x
        self.height = max(self.height, y)

    def _top_profile(self):
        tops = [0] * WIDTH
        for col in range(WIDTH):
            for y in range(self.height, -1, -1):
                if self.rows[y] & (1 << col):
                    tops[col] = self.height - y
                    break
        return tuple(tops)

    def simulate(self, target, use_cycles=False):
        n = 0
        extra_height = 0
        seen = {}

        while n < target:
            mask = MASKS[self.shape_index]
            y = self.height + 3 + 4 - OFFSETS[self.shape_index]
            x = 2

            while True:
                jet = self.jets[self.jet_index]
                self.jet_index = (self.jet_index + 1) % len(self.jets)
                nx = x + (-1 if jet == '<' else 1)
                if 0 <= nx <= WIDTH - max(row.bit_length() for row in mask) and self._can_move(mask, nx, y):
                    x = nx

                if self._can_move(mask, x, y - 1):
                    y -= 1
                else:
                    self._place_rock(mask, x, y)
                    n += 1
                    break

            if use_cycles:
                key = (self._top_profile(), self.shape_index, self.jet_index)
                if key in seen:
                    old_n, old_h = seen[key]
                    delta_n = n - old_n
                    delta_h = self.height - old_h
                    repeats = (target - n) // delta_n
                    n += delta_n * repeats
                    extra_height += delta_h * repeats
                    seen.clear()
                seen[key] = (n, self.height)

            self.shape_index = (self.shape_index + 1) % len(SHAPES)

        return self.height + 1 + extra_height


if __name__ == "__main__":
    jets = Path("input.txt").read_text().strip()

    part1 = PyroclasticSimulator(jets)
    print("Part 1:", part1.simulate(2022, use_cycles=False))

    part2 = PyroclasticSimulator(jets)
    print("Part 2:", part2.simulate(1_000_000_000_000, use_cycles=True))
