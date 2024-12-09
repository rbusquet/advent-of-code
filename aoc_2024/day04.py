from pathlib import Path

input = Path(__file__).parent / "input.txt"


point = tuple[int, int]


def manhattan_distance(a: point, b: point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def man_slope(a: point, b: point) -> float:
    if a[1] == b[1]:
        return float("inf")
    return abs(a[0] - b[0]) / abs(a[1] - b[1])


def word(grid: list[str], x: point, s: point, slope: point):
    word = []
    while x != s:
        word.append(grid[x[0]][x[1]])
        x = (x[0] + slope[0], x[1] + slope[1])
    word.append(grid[x[0]][x[1]])
    return "".join(word)


def unit_vector(a: point, b: point) -> point | None:
    x1, y1 = a
    x2, y2 = b
    x_diff = x2 - x1
    y_diff = y2 - y1
    if y1 == y2:
        return (x_diff // abs(x_diff), 0)
    if x1 == x2:
        return (0, y_diff // abs(y_diff))
    if abs(x_diff) == abs(y_diff):
        return (x_diff // abs(x_diff), y_diff // abs(y_diff))
    return None


def part_1() -> int:
    x_positions = set()
    s_positions = set()
    grid = input.read_text().splitlines()
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "X":
                x_positions.add((i, j))
            if char == "S":
                s_positions.add((i, j))

    count = 0
    for x in x_positions:
        for s in s_positions:
            distance = manhattan_distance(x, s)
            if distance not in (3, 6):
                continue
            slope = unit_vector(x, s)
            if not slope:
                continue
            count += word(grid, x, s, slope) == "XMAS"

    return count


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
