from itertools import count, product


def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


layout = {}

max_i = 0
max_j = 0
for i, row in enumerate(read_file()):
    for j, seat in enumerate(row):
        layout[i, j] = seat
        max_j = j + 1
    max_i = i + 1

last_count = 0


def check_adj(i, j, layout):
    base = [-1, 0, 1]
    for x, y in product(base, base):
        if (x, y) == (0, 0):
            continue
        for step in count(1):
            ii = x * step + i
            jj = y * step + j
            looking_at = layout.get((ii, jj))
            if looking_at is None or looking_at == "L":
                # outer bounds or see an empty seat
                break
            if looking_at == "#":
                return True

    return False


def count_occupied(i, j, layout):
    occupied = 0
    base = [-1, 0, 1]

    for x, y in product(base, base):
        if (x, y) == (0, 0):
            continue
        for step in count(1):
            ii = x * step + i
            jj = y * step + j
            looking_at = layout.get((ii, jj))
            if looking_at is None or looking_at == "L":
                break
            if looking_at == "#":
                occupied += 1
                break
    return occupied >= 5


while True:
    new_layout = {}
    occupied_count = 0
    for seat, state in layout.items():
        i, j = seat
        new_layout[i, j] = state
        if state == "L":
            has_adj = check_adj(i, j, layout)
            if not has_adj:
                new_layout[i, j] = "#"
                occupied_count += 1
        elif state == "#":
            occupied = count_occupied(i, j, layout)
            if occupied:
                new_layout[i, j] = "L"
            else:
                occupied_count += 1

    if occupied_count == last_count:
        print(occupied_count)
        break
    last_count = occupied_count
    layout = new_layout
