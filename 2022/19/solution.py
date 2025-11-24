# Day 19: Not Enough Minerals

import math
import re
from pathlib import Path

# Constants
ORE, CLAY, OBSIDIAN, GEODE = range(4)
ROCKS = [ORE, CLAY, OBSIDIAN, GEODE]
TYPES = {"ore": ORE, "clay": CLAY, "obsidian": OBSIDIAN, "geode": GEODE}
TIMEOUT = 300

LineType = int
InputType = list[LineType]


def read_input_file(filepath: str = "input.txt") -> InputType:
    """Parse input data into blueprint structures."""
    blueprints = []
    pattern = re.compile(r"Each (.*) robot costs (.*)")
    base_costs = {t: 0 for t in TYPES.values()}

    for line in Path(filepath).read_text().strip().splitlines():
        _, line = line.split(": ")
        blueprint = {}
        for sentence in line.removesuffix(".").split(". "):
            costs = base_costs.copy()
            out, ins = pattern.match(sentence).groups()
            for a in ins.split(" and "):
                num, ore = a.split()
                costs[TYPES[ore]] = int(num)
            blueprint[TYPES[out]] = tuple(costs[i] for i in (ORE, CLAY, OBSIDIAN))
        blueprints.append(blueprint)

    return blueprints


from functools import lru_cache

def simulator(puzzle_input: InputType, minutes: int) -> list[int]:
    scores = []

    for blueprint in puzzle_input:
        # Precompute max spend for each material type
        max_ore_spend = max(cost[ORE] for cost in blueprint.values())
        max_clay_spend = max(cost[CLAY] for cost in blueprint.values())
        max_obs_spend = max(cost[OBSIDIAN] for cost in blueprint.values())

        best_geodes = 0
        best_seen = {}

        # Stack holds (time_left, ore_bots, clay_bots, obs_bots, geo_bots, ore, clay, obs, geodes)
        stack = [(minutes, 1, 0, 0, 0, 0, 0, 0, 0)]

        while stack:
            (
                time_left, ore_bots, clay_bots, obs_bots, geo_bots,
                ore, clay, obs, geodes
            ) = stack.pop()

            if time_left == 0:
                if geodes > best_geodes:
                    best_geodes = geodes
                continue

            # Theoretical upper bound — prune dead branches
            max_possible = geodes + geo_bots * time_left + (time_left * (time_left - 1)) // 2
            if max_possible <= best_geodes:
                continue

            # Cap resources — no point storing more than can be spent
            if ore > max_ore_spend * time_left:
                ore = max_ore_spend * time_left
            if clay > max_clay_spend * time_left:
                clay = max_clay_spend * time_left
            if obs > max_obs_spend * time_left:
                obs = max_obs_spend * time_left

            # Memoization key — drop 'geodes' (it’s derived)
            key = (
                time_left, ore_bots, clay_bots, obs_bots, geo_bots,
                ore, clay, obs
            )

            prev_best = best_seen.get(key)
            if prev_best is not None and prev_best >= geodes:
                continue
            best_seen[key] = geodes

            # Collect resources
            new_ore = ore + ore_bots
            new_clay = clay + clay_bots
            new_obs = obs + obs_bots
            new_geodes = geodes + geo_bots

            # Try to build in priority order
            # 1. Build GEODE bot if possible
            ore_cost, _, obs_cost = blueprint[GEODE]
            if ore >= ore_cost and obs >= obs_cost:
                stack.append((
                    time_left - 1,
                    ore_bots, clay_bots, obs_bots, geo_bots + 1,
                    new_ore - ore_cost, new_clay, new_obs - obs_cost, new_geodes
                ))
                # Skip exploring lower-priority builds; GEODE is best possible
                continue

            # 2. Build OBSIDIAN bot if useful
            ore_cost, clay_cost, _ = blueprint[OBSIDIAN]
            if (
                obs_bots < max_obs_spend
                and ore >= ore_cost and clay >= clay_cost
            ):
                stack.append((
                    time_left - 1,
                    ore_bots, clay_bots, obs_bots + 1, geo_bots,
                    new_ore - ore_cost, new_clay - clay_cost, new_obs, new_geodes
                ))

            # 3. Build CLAY bot if useful
            ore_cost, _, _ = blueprint[CLAY]
            if clay_bots < max_clay_spend and ore >= ore_cost:
                stack.append((
                    time_left - 1,
                    ore_bots, clay_bots + 1, obs_bots, geo_bots,
                    new_ore - ore_cost, new_clay, new_obs, new_geodes
                ))

            # 4. Build ORE bot if useful
            ore_cost, _, _ = blueprint[ORE]
            if ore_bots < max_ore_spend and ore >= ore_cost:
                stack.append((
                    time_left - 1,
                    ore_bots + 1, clay_bots, obs_bots, geo_bots,
                    new_ore - ore_cost, new_clay, new_obs, new_geodes
                ))

            # 5. Do nothing
            stack.append((
                time_left - 1,
                ore_bots, clay_bots, obs_bots, geo_bots,
                new_ore, new_clay, new_obs, new_geodes
            ))

        scores.append(best_geodes)

    return scores


def _simulator(puzzle_input: InputType, minutes: int) -> list[int]:
    scores = []

    for idx, blueprint in enumerate(puzzle_input, start=1):
        max_spend = {
            rock: max(cost[rock] for cost in blueprint.values())
            for rock in (ORE, CLAY, OBSIDIAN)
        }

        seen = set()
        todo = {(-minutes, 0, 0, 0, 0, 0, 0, 1, 0)}
        turns_to_bots = {1: -minutes}
        highest = 0

        while todo:
            cur = max(todo)
            todo.remove(cur)
            turns, rg, ig, rb, ib, rc, ic, rr, ir = cur

            if turns == 0:
                highest = max(highest, ig)
                continue

            # Prune paths that can’t catch up to current best
            if ig + rg * -turns + (turns * (turns + 1)) // 2 < highest:
                continue

            candidates = []

            # Try to build a geode bot
            if (
                blueprint[GEODE][ORE] <= ir
                and blueprint[GEODE][OBSIDIAN] <= ib
            ):
                candidates.append((
                    True, turns + 1,
                    rg + 1, ig + rg,
                    rb, ib + rb - blueprint[GEODE][OBSIDIAN],
                    rc, ic + rc,
                    rr, ir + rr - blueprint[GEODE][ORE],
                ))
            else:
                # Try to build obsidian bot
                max_obs_used = blueprint[GEODE][OBSIDIAN] * (-turns - 1)
                min_obs_avail = ib + rb * (-turns - 1)
                if (
                    rb < max_spend[OBSIDIAN]
                    and blueprint[OBSIDIAN][ORE] <= ir
                    and blueprint[OBSIDIAN][CLAY] <= ic
                    and max_obs_used > min_obs_avail
                ):
                    candidates.append((
                        True, turns + 1,
                        rg, ig + rg,
                        rb + 1, ib + rb,
                        rc, ic + rc - blueprint[OBSIDIAN][CLAY],
                        rr, ir + rr - blueprint[OBSIDIAN][ORE],
                    ))

                # Try to build clay bot
                max_clay_used = blueprint[OBSIDIAN][CLAY] * (-turns - 1)
                min_clay_avail = ic + rc * (-turns - 1)
                if (
                    rc < max_spend[CLAY]
                    and blueprint[CLAY][ORE] <= ir
                    and max_clay_used > min_clay_avail
                ):
                    candidates.append((
                        True, turns + 1,
                        rg, ig + rg,
                        rb, ib + rb,
                        rc + 1, ic + rc,
                        rr, ir + rr - blueprint[CLAY][ORE],
                    ))

                # Try to build ore bot
                if (
                    rr < max_spend[ORE]
                    and blueprint[ORE][ORE] <= ir
                    and blueprint[ORE][ORE] < -turns
                ):
                    candidates.append((
                        True, turns + 1,
                        rg, ig + rg,
                        rb, ib + rb,
                        rc, ic + rc,
                        rr + 1, ir + rr - blueprint[ORE][ORE],
                    ))

                # Do nothing this turn
                candidates.append((
                    False, turns + 1,
                    rg, ig + rg,
                    rb, ib + rb,
                    rc, ic + rc,
                    rr, ir + rr,
                ))

            # Process next states
            for building, *next_state in candidates:
                turns, rg, ig, rb, ib, rc, ic, rr, ir = next_state

                # Compact state hash
                bots = 0
                for i in (1, 3, 5, 7):
                    bots = (bots << 5) | next_state[i]
                hsh = (bots << 7) | -next_state[0]
                for i in (2, 4, 6, 8):
                    hsh = (hsh << 9) | next_state[i]

                if hsh in seen:
                    continue

                if building and bots in turns_to_bots and turns_to_bots[bots] < turns:
                    continue

                turns_to_bots[bots] = turns
                seen.add(hsh)
                todo.add(tuple(next_state))

        scores.append(highest)

    return scores


def part_one(puzzle_input: InputType) -> int:
    scores = simulator(puzzle_input, 24)
    return sum(idx * score for idx, score in enumerate(scores, start=1))


def part_two(puzzle_input: InputType) -> int:
    return math.prod(simulator(puzzle_input[:3], 32))


if __name__ == "__main__":
    blueprints = read_input_file()
    print("Part 1:", part_one(blueprints))
    print("Part 2:", part_two(blueprints))
