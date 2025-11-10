# Day 17: Pyroclastic Flow

from collections import defaultdict
from pathlib import Path

# Rock shapes (4x4 grid, top-left anchored)
SHAPES = [
    [[1, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 0, 0, 0]],

    [[0, 1, 0, 0],
     [1, 1, 1, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0]],

    [[0, 0, 1, 0],
     [0, 0, 1, 0],
     [1, 1, 1, 0],
     [0, 0, 0, 0]],

    [[1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    [[1, 1, 0, 0],
     [1, 1, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
]

# Height offsets used to compute starting py for each piece type
HEIGHTS = [3, 1, 1, 0, 2]


def load_input_file(filepath: str = "input.txt") -> str:
    """Read the input file and return its contents as a string."""
    return Path(filepath).read_text().strip()


class PyroclasticSimulator:
    """Simulates falling rock pieces with jet stream influence."""

    def __init__(self, jet_pattern: str):
        self.jet_pattern = jet_pattern
        self.grid = defaultdict(int)      # (x,y) -> 1 if filled
        self.pid = 0                      # current piece id (index into PIECES)
        self.max_y = -1                   # highest occupied y; -1 means empty floor
        # px is horizontal position (left-most column of the piece's 4x4); initial = 2
        self.px = 2
        # IMPORTANT FIX: initialize py using rule used for subsequent spawns.
        self.py = self.max_y + 3 + 4 - HEIGHTS[self.pid]

    def _can_move(self, dx: int, dy: int) -> bool:
        """Check if the current piece can move by (dx, dy)."""
        npx, npy = self.px + dx, self.py + dy
        piece = SHAPES[self.pid]

        for i in range(4):
            for j in range(4):
                if piece[i][j] == 0:
                    continue
                rx, ry = npx + i, npy - j
                if not (0 <= rx < 7) or ry < 0 or self.grid[(rx, ry)]:
                    return False
        return True

    def _move_piece(self, dx: int, dy: int) -> bool:
        """Attempt to move the current piece; returns True if successful."""
        if self._can_move(dx, dy):
            self.px += dx
            self.py += dy
            return True
        return False

    def _lock_piece(self):
        """Fix the current piece into the grid."""
        piece = SHAPES[self.pid]
        for i in range(4):
            for j in range(4):
                if piece[i][j]:
                    rx, ry = self.px + i, self.py - j
                    self.grid[(rx, ry)] = 1

    def _move_down(self) -> bool:
        """Try moving the piece down; lock it if it cannot move."""
        if not self._move_piece(0, -1):
            self._lock_piece()
            return False
        return True

    def _top_profile(self) -> tuple:
        """Return a normalized profile of the top of the tower (7 ints)."""
        heights = [-17] * 7
        for (x, y), v in self.grid.items():
            if v == 1:
                heights[x] = max(heights[x], y)
        top = max(heights)
        return tuple(h - top for h in heights)

    def _spawn_new_piece(self):
        """Prepare for the next piece after one locks (update pid, px, py, max_y)."""
        self.max_y = max((y for (_, y), v in self.grid.items() if v == 1), default=-1)
        self.pid = (self.pid + 1) % len(SHAPES)
        self.px = 2
        self.py = self.max_y + 3 + 4 - HEIGHTS[self.pid]

    def simulate(self, target_pieces: int, use_cycle_detection: bool = False) -> int:
        """
        Run the simulation up to the target number of pieces.
        If use_cycle_detection is True, attempts to fast-forward using detected cycles.
        """
        seen = {}
        num_pieces = 0
        extra_height = 0
        jets = self.jet_pattern

        while num_pieces < target_pieces:
            for vid, jet in enumerate(jets):
                # apply jet push
                if jet == "<":
                    self._move_piece(-1, 0)
                else:
                    self._move_piece(1, 0)

                # try to move down; if can't, piece locks
                if not self._move_down():
                    # spawn next piece
                    self._spawn_new_piece()
                    num_pieces += 1

                    if num_pieces >= target_pieces:
                        break

                    if use_cycle_detection:
                        key = (self._top_profile(), self.pid, vid)
                        if key in seen:
                            old_num, old_max = seen[key]
                            delta_n = num_pieces - old_num
                            delta_h = self.max_y - old_max
                            # how many full repeats can we take
                            repeats = (target_pieces - num_pieces) // delta_n
                            num_pieces += delta_n * repeats
                            extra_height += delta_h * repeats
                            seen.clear()  # avoid repeating the same fast-forward
                        else:
                            seen[key] = (num_pieces, self.max_y)

            if num_pieces >= target_pieces:
                break

        final_height = max((y for (_, y), v in self.grid.items() if v == 1), default=-1)
        return final_height + 1 + extra_height


if __name__ == "__main__":
    pattern = load_input_file()
    part1 = PyroclasticSimulator(pattern).simulate(2022, use_cycle_detection=False)
    print("Part 1:", part1)
    part2 = PyroclasticSimulator(pattern).simulate(1_000_000_000_000, use_cycle_detection=True)
    print("Part 2:", part2)

"""
Expected:
Part 1: 3181
Part 2: 1570434782634
"""