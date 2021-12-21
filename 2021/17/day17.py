# wip

import math
import re
from collections import defaultdict
from itertools import count
from pathlib import Path


def parse_input() -> tuple[int, int, int, int]:
    with open(Path(__file__).parent / "input.txt") as file:
        min_x, max_x, min_y, max_y = map(
            int, re.compile(r"[-\d]+").findall(file.readline())
        )
    return min_x, max_x, min_y, max_y


def quadratic(a: float, b: float, c: float) -> int:
    a1 = -b + pow(pow(b, 2) - 4 * a * c, 0.5)
    a2 = -b - pow(pow(b, 2) - 4 * a * c, 0.5)
    a1 /= 2 * a
    a2 /= 2 * a

    return math.floor(max(a1, a2))


def part_2() -> int:  # noqa: C901
    min_x, max_x, min_y, max_y = parse_input()

    # min_vx = quadratic(0.5, -0.5, -min_x)
    # max_vx = max_x  # lands on the top of the right side in one step

    valid_initial_x_speeds = list[tuple[int, int]]()
    hover_speeds = defaultdict(list)
    for velocity in range(0, 1000):
        ivx = velocity
        posx = 0

        for steps in count(1):
            posx += velocity
            if velocity > 0:
                velocity -= 1
            if velocity < 0:
                velocity += 1
            if min_x <= posx <= max_x:
                valid_initial_x_speeds.append((ivx, steps))
            if velocity == 0:
                if min_x <= posx <= max_x:
                    hover_speeds[steps].append(ivx)
                break
            if posx > max_x:
                break

    all_possible_steps = set[int]()
    initial_x_speeds_by_steps = defaultdict[int, list[int]](list)
    for t, v in valid_initial_x_speeds:
        all_possible_steps.add(v)
        initial_x_speeds_by_steps[v].append(t)

    valid_initial_y_speeds = list[tuple[int, int]]()

    for velocity in range(-3000, 3000):
        posy = 0
        ivy = velocity
        for steps in count(1):
            posy += velocity
            velocity -= 1
            if min_y <= posy <= max_y:
                valid_initial_y_speeds.append((steps, ivy))
            if posy < min_y:
                break
    initial_y_speeds_by_steps = defaultdict[int, list[int]](list)
    for t, v in valid_initial_y_speeds:
        all_possible_steps.add(t)
        initial_y_speeds_by_steps[t].append(v)

    all_velocities = set()
    for ystep, vys in initial_y_speeds_by_steps.items():
        vxs_hovering_at_step = initial_x_speeds_by_steps[ystep]
        for vx in vxs_hovering_at_step:
            for vy in vys:
                all_velocities.add((vx, vy))
        for hover_steps, velocities in hover_speeds.items():
            if hover_steps < ystep:
                for vx in velocities:
                    for vy in vys:
                        all_velocities.add((vx, vy))
    return len(all_velocities)


if __name__ == "__main__":
    print(part_2())
