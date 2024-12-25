from pathlib import Path

input = Path(__file__).parent / "input.txt"


class Key(list[int]):
    def __init__(self) -> None:
        super().__init__([0, 0, 0, 0, 0])


class Lock(list[int]):
    def __init__(self) -> None:
        super().__init__([0, 0, 0, 0, 0])

    def fits(self, key: Key) -> bool:
        for i, pin in enumerate(self):
            if key[i] + pin > 5:
                return False
        return True


def part_1() -> int:
    pieces = input.read_text().split("\n\n")

    locks = list[Lock]()
    keys = list[Key]()
    for piece in pieces:
        if piece.startswith("#####"):  # lock
            lock = Lock()
            for line in piece.splitlines()[1:]:
                for i, ch in enumerate(line):
                    lock[i] += ch == "#"
            locks.append(lock)
        elif piece.startswith("....."):
            key = Key()
            for line in piece.splitlines()[:-1]:
                for i, ch in enumerate(line):
                    key[i] += ch == "#"
            keys.append(key)

    count = 0
    for lock in locks:
        for key in keys:
            count += lock.fits(key)
    return count


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
