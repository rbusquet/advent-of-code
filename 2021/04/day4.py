from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


def csv_to_ints(line: str, separator: str = " ") -> tuple[int, ...]:
    return tuple(map(int, (i for i in line.strip().split(separator) if i)))


BOARD_SIZE = 5


@dataclass
class Board:
    numbers: dict[tuple[int, int], int] = field(default_factory=dict)
    checked: dict[tuple[int, int], bool] = field(init=False, default_factory=dict)
    all_numbers: dict[int, tuple[int, int]] = field(default_factory=dict, init=False)
    _winner: bool = field(default=False, init=False)

    def add_square(self, i: int, j: int, number: int) -> None:
        self.numbers[i, j] = number
        self.checked[i, j] = False
        self.all_numbers[number] = (i, j)

    def unchecked(self) -> Iterator[int]:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.checked[i, j]:
                    yield self.numbers[i, j]

    def winner(self) -> bool:
        if self._winner:
            return self._winner
        for i in range(BOARD_SIZE):
            row_checked = all(self.checked[i, j] for j in range(BOARD_SIZE))
            column_checked = all(self.checked[j, i] for j in range(BOARD_SIZE))
            if row_checked or column_checked:
                self._winner = True
                return self._winner
        return False

    def check(self, number) -> None:
        if self.winner():
            return
        if number not in self.all_numbers:
            return
        i, j = self.all_numbers[number]
        self.checked[i, j] = True


def part_1():
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        boards, numbers = build_game(file)

        for number in numbers:
            for board in boards:
                board.check(number)
                if board.winner():
                    score = sum(board.unchecked()) * number
                    return score


def part_2():
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        boards, numbers = build_game(file)

        winners = []
        for number in numbers:
            for board in boards:
                board.check(number)
                if board.winner() and board not in winners:
                    winners.append(board)
                if len(winners) == len(boards):
                    return sum(winners[-1].unchecked()) * number


def build_game(file):
    numbers = csv_to_ints(next(file), ",")
    next(file)
    board = Board()
    boards = [board]
    ii = 0
    for line in file:
        line = line.strip()
        if not line:
            board = Board()
            boards.append(board)
            ii = 0
            continue
        for jj, number in enumerate(csv_to_ints(line)):
            board.add_square(ii, jj, number)
        ii += 1
    return boards, numbers


if __name__ == "__main__":
    print(part_1())
    print(part_2())
