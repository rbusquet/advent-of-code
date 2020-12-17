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

def neighbors(*position):
    for diff in product([-1, 0, 1], repeat=len(position)):
        neighbor = tuple(pos + diff[i] for i, pos in enumerate(position))
        if neighbor == position:
            continue
        yield neighbor

    #     active_count += layout[neighbor] == '#'
    # if layout[position] == '#':
    #     if active_count not in [2, 3]:
    #         return '.'
    # else:
    #     if active_count == 3:
    #         return '#'
    # return layout[position]


space = defaultdict(lambda: '.')
for x, line in enumerate(initial.splitlines()):
    for y, state in enumerate(line):
        cube = x, y, 0
        space[cube] = state

def count_active(space):
    return len([1 for state in space.values() if state == '#'])

print(count_active(space))
for _ in range(6):
    cube_to_active_count = defaultdict(int)

    for cube in space:
        for n in neighbors(*cube):
            cube_to_active_count[n] += space[cube] == '#'
    for n, count in cube_to_active_count.items():
        if space[n] == '#':
            if count in [2, 3]:
                space[n] = '#'
            else:
                space[n] = '.'
        elif space[n] == '.':
            if count == 3:
                space[n] = '#'

    print(count_active(space))


space = defaultdict(lambda: '.')
for x, line in enumerate(initial.splitlines()):
    for y, state in enumerate(line):
        cube = x, y, 0, 0
        space[cube] = state

def count_active(space):
    return len([1 for state in space.values() if state == '#'])

print(count_active(space))
for _ in range(6):
    cube_to_active_count = defaultdict(int)

    for cube in space:
        for n in neighbors(*cube):
            cube_to_active_count[n] += space[cube] == '#'
    for n, count in cube_to_active_count.items():
        if space[n] == '#':
            if count in [2, 3]:
                space[n] = '#'
            else:
                space[n] = '.'
        elif space[n] == '.':
            if count == 3:
                space[n] = '#'

    print(count_active(space))
