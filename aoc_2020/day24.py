from typing import DefaultDict, NamedTuple


class Cube(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, cube: "Cube"):
        return Cube(self.x + cube.x, self.y + cube.y, self.z + cube.z)

    @classmethod
    def new(cls) -> "Cube":
        return Cube(0, 0, 0)


# https://www.redblobgames.com/grids/hexagons/#neighbors-cube
cube_directions = {
    "e": Cube(+1, -1, 0),
    "ne": Cube(+1, 0, -1),
    "nw": Cube(0, +1, -1),
    "w": Cube(-1, +1, 0),
    "sw": Cube(-1, 0, +1),
    "se": Cube(0, -1, +1),
}


def read_file():
    with open("./input.txt") as f:
        yield from (c.strip() for c in f.readlines())


hex_grid = DefaultDict(bool)


def find_cube(instruction):
    p = 0
    cube = Cube.new()
    while p < len(instruction):
        direction = instruction[p : p + 1]
        if direction not in cube_directions:
            direction = instruction[p : p + 2]
            p += 1
        p += 1
        offset = cube_directions[direction]
        cube += offset
        # print(cube)
    return cube


hex_grid = DefaultDict(bool)

for instruction in read_file():
    cube = find_cube(instruction)
    hex_grid[cube] = not hex_grid[cube]


print(sum(hex_grid.values()))


def neighborhood(cube: Cube):
    yield cube
    for direction in cube_directions:
        yield cube + cube_directions[direction]


def full_cycle(grid, days):
    for _ in range(days):
        cube_to_active_count = DefaultDict[Cube, int](int)

        for cube in grid:
            if not grid[cube]:
                continue
            for n in neighborhood(cube):
                # neighborhood contains cube and all its neighbors.
                # `cube_to_active_count[n] += n != cube` ensures
                # active cubes without active neighbors are counted
                # and proper deactivated by underpopulation in the
                # next for-loop.
                cube_to_active_count[n] += n != cube and grid[cube]
        for n, count in cube_to_active_count.items():
            if grid[n]:
                if count == 0 or count > 2:
                    grid[n] = False
            else:
                if count == 2:
                    grid[n] = True
    return grid


final = full_cycle(hex_grid, 100)
print(sum(final.values()))
