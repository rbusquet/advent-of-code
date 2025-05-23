from collections.abc import Iterator


def partition(code: str, count: int, lower_ch: str, upper_ch: str) -> int:
    left = 0
    right = 2**count

    for i in range(count):
        ch = code[i]
        mid = (right - left) // 2 + left
        if ch == lower_ch:
            right = mid
        elif ch == upper_ch:
            left = mid
    return min(left, right)


def read_file() -> Iterator[str]:
    with open("./input.txt") as f:
        yield from (c.strip() for c in f.readlines())


def to_int(code: str, zero: str, one: str) -> int:
    code = code.replace(zero, "0").replace(one, "1")
    return int(code, base=2)


def part_1_thanks_alex() -> int:
    max_id = 0
    for code in read_file():
        row = to_int(code[:7], "F", "B")
        col = to_int(code[-3:], "L", "R")
        seat_id = row * 8 + col
        if seat_id > max_id:
            max_id = seat_id
    return max_id


def part_1() -> int:
    max_id = 0
    for code in read_file():
        row = partition(code[:7], 7, "F", "B")
        col = partition(code[-3:], 3, "L", "R")
        seat_id = row * 8 + col
        if seat_id > max_id:
            max_id = seat_id
    return max_id


def part_2_visualization() -> None:
    """
    Will print something like this with my input

    ...
    086 -> ['#', '#', '#', '#', '#', '#', '#', '#']
    087 -> ['#', '#', '#', '#', '#', '#', '#', '#']
    088 -> ['#', '.', '#', '#', '#', '#', '#', '#']
    089 -> ['#', '#', '#', '#', '#', '#', '#', '#']
    090 -> ['#', '#', '#', '#', '#', '#', '#', '#']
    ...

    meaning the free seat is in row 88, col 1.
    """
    aircraft = [["." for _ in range(8)] for _ in range(128)]
    for code in read_file():
        row = partition(code[:7], 7, "F", "B")
        col = partition(code[-3:], 3, "L", "R")
        aircraft[row][col] = "#"
    for i, x in enumerate(aircraft):
        print(f"{i:0>3} -> {x}")


def part_2_for_real_now() -> int:
    ids = set()
    for code in read_file():
        row = partition(code[:7], 7, "F", "B")
        col = partition(code[-3:], 3, "L", "R")

        ids.add(row * 8 + col)
    seat = set(range(min(ids), max(ids))) - ids
    return seat.pop()


if __name__ == "__main__":
    print("--- part 1 ---")
    print(part_1())
    assert part_1() == part_1_thanks_alex()
    part_2_visualization()
    # from vizualization:
    row = 88
    col = 1
    print("--- part 2 ---")
    print(f"result {row * 8 + col} found using aircraft visualization")
    print(f"result {part_2_for_real_now()} found programatically")
