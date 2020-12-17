from itertools import product
from collections import defaultdict

initial = """
####.#..
.......#
#..#####
.....##.
##...###
#..#.#.#
.##...#.
#...##..
""".strip()


def neighborhood(*position):
    for diff in product([-1, 0, 1], repeat=len(position)):
        neighbor = tuple(pos + diff[i] for i, pos in enumerate(position))
        yield neighbor


def full_cycle(initial, dimensions):
    space = defaultdict(lambda: ".")
    padding = (0,) * (dimensions - 2)
    for x, line in enumerate(initial.splitlines()):
        for y, state in enumerate(line):
            cube = (x, y) + padding
            space[cube] = state

    for _ in range(6):
        cube_to_active_count = defaultdict(int)

        for cube in space:
            if space[cube] == ".":
                continue
            for n in neighborhood(*cube):
                # neighborhood contains cube and all its neighbors.
                # `cube_to_active_count[n] += n != cube` ensures
                # active cubes without active neighbors are counted
                # and proper deactivated by underpopulation in the
                # next for-loop.
                cube_to_active_count[n] += n != cube and space[cube] == "#"
        for n, count in cube_to_active_count.items():
            if space[n] == "#":
                if count in [2, 3]:
                    space[n] = "#"
                else:
                    space[n] = "."
            elif space[n] == ".":
                if count == 3:
                    space[n] = "#"

    return sum(state == "#" for state in space.values())


print("--- part 1 ---")
print(full_cycle(initial, 3))
print("--- part 2 ---")
print(full_cycle(initial, 4))
