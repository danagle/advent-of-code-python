
def read_input_file(filename="input.txt"):
    grid = []

    with open(filename) as f:
        text = f.read().strip()

    it = iter(text.splitlines())
    next(it)

    for s in it:
        if s[1] == '#':
            break
        row = []
        for c in s[1:]:
            if c == '#':
                break
            if c == '^':
                row.append(0b1)
            elif c == '>':
                row.append(0b10)
            elif c == 'v':
                row.append(0b100)
            elif c == '<':
                row.append(0b1000)
            elif c in ('.', '#'):
                row.append(0)
            else:
                raise ValueError(f"unknown char {c}")
        grid.append(row)

    return grid


# 0b1 = up, 0b10 = right, 0b100 = down, 0b1000 = left
def print_state(grid, state):
    for r, line in enumerate(grid):
        row = []
        for c, point in enumerate(line):
            if point == 0b1:
                row.append('^')
            elif point == 0b10:
                row.append('>')
            elif point == 0b100:
                row.append('v')
            elif point == 0b1000:
                row.append('<')
            elif point in (0b0011, 0b0101, 0b1001, 0b0110, 0b1010, 0b1100):
                row.append('2')
            elif point in (0b0111, 0b1011, 0b1101, 0b1110):
                row.append('3')
            elif point == 0b1111:
                row.append('4')
            elif point == 0:
                row.append('@' if state[r][c] else ' ')
            else:
                row.append('?')
        print(''.join(row))


def wrap(k, n):
    return k % n


def advance(grid, swap):
    n, m = len(grid), len(grid[0])
    for r in range(n):
        for c in range(m):
            up    = grid[wrap(r+1, n)][c] & 0b1
            down  = grid[wrap(r-1, n)][c] & 0b100
            left  = grid[r][wrap(c+1, m)] & 0b1000
            right = grid[r][wrap(c-1, m)] & 0b10

            swap[r][c] = up | down | left | right
    # swap references
    grid[:], swap[:] = swap[:], grid[:]


def iterate(grid, goals):
    n, m = len(grid), len(grid[0])
    swapgrid = [[0] * m for _ in range(n)]

    state = [[False] * m for _ in range(n)]
    swapstate = [[False] * m for _ in range(n)]

    n_i, m_i = n, m

    iterations = 0
    goals_iter = iter(goals)
    start_r, start_c = next(goals_iter)

    first_goal_met = False

    for goal_r, goal_c in goals_iter:
        # clear state
        for line in state:
            for i in range(m):
                line[i] = False

        while True:
            advance(grid, swapgrid)

            for r in range(n_i):
                for c in range(m_i):
                    empty = grid[r][c] == 0
                    reachable = (
                        state[r][c]
                        or (r >= 1 and state[r-1][c])
                        or (r+1 < n_i and state[r+1][c])
                        or (c >= 1 and state[r][c-1])
                        or (c+1 < m_i and state[r][c+1])
                    )
                    swapstate[r][c] = empty and reachable

            swapstate[start_r][start_c] = (grid[start_r][start_c] == 0)

            state, swapstate = swapstate, state
            iterations += 1

            if state[goal_r][goal_c]:
                break

        advance(grid, swapgrid)
        iterations += 1

        start_r, start_c = goal_r, goal_c
        if not first_goal_met:
            print("Part 1:", iterations)
            first_goal_met = True

    print("Part 2:", iterations)


if __name__ == "__main__":
    valley = read_input_file()
    n, m = len(valley), len(valley[0])
    iterate(valley, [(0, 0), (n-1, m-1), (0, 0), (n-1, m-1)])
