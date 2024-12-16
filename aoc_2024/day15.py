import curses
import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

input = Path(__file__).parent / "input.txt"


class Direction(enum.StrEnum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


Position = tuple[int, int]


class Universe(dict[Position, "Movable"]):
    def print(self):
        maxx, maxy = max(self)
        for x in range(maxx + 1):
            for y in range(maxy + 1):
                print(self.get((x, y), "."), end="")
            print()

    def wide_print(self, pad: curses.window, instruction: Direction) -> None:
        grid = self
        maxx, maxy = max(grid)

        for x in range(0, maxx + 1):
            y = 0
            while y < maxy + 2:
                label = str(self.get((x, y)) or ".")
                if label == "@":
                    label = instruction.value
                pad.addstr(x + 1, y, label)

                y += len(label)

    def gps(self, label: str) -> int:
        calculated = []
        gps = 0
        for m in self.values():
            if m in calculated or m.label != label:
                continue
            gps += m.gps()
            calculated.append(m)
        return gps


@dataclass
class Movable(ABC):
    x: int
    y: int
    universe: Universe = field(repr=False)

    label: ClassVar[str]

    def __str__(self) -> str:
        return self.label

    def __post_init__(self):
        self.universe[self.position] = self

    def update_position(self, position: Position) -> None:
        self.universe.pop(self.position)
        self.position = position
        self.universe[position] = self

    @property
    def position(self) -> Position:
        return self.x, self.y

    @position.setter
    def position(self, pos: Position) -> None:
        self.x, self.y = pos

    def next_position(self, direction: Direction) -> Position:
        match direction:
            case Direction.LEFT:
                return self.x, self.y - 1
            case Direction.RIGHT:
                return self.x, self.y + 1
            case Direction.UP:
                return self.x - 1, self.y
            case Direction.DOWN:
                return self.x + 1, self.y

    def undo(self, direction: Direction) -> Position:
        match direction:
            case Direction.LEFT:
                return self.x, self.y + 1
            case Direction.RIGHT:
                return self.x, self.y - 1
            case Direction.UP:
                return self.x + 1, self.y
            case Direction.DOWN:
                return self.x - 1, self.y

    @abstractmethod
    def move(self, direction: Direction, moved: list["Movable"]) -> bool: ...

    def is_over(self, position: Position) -> bool:
        return self.position == position

    def gps(self) -> int:
        return 100 * self.x + self.y


@dataclass
class Wall(Movable):
    label = "#"

    def move(self, direction: Direction, moved: list["Movable"]) -> bool:
        return False


@dataclass
class WideWall(Wall):
    label = "##"

    def is_over(self, position: Position) -> bool:
        ys = (position[1], position[1] - 1)
        return self.x == position[0] and self.y in ys

    def __post_init__(self):
        self.universe[self.position] = self
        self.universe[self.x, self.y + 1] = self


@dataclass
class Box(Movable):
    label = "O"

    def move(self, direction: Direction, moved: list[Movable]) -> bool:
        position = self.next_position(direction)
        obstacle = self.universe.get(position)
        if not obstacle or obstacle.move(direction, moved):
            self.universe.pop(self.position)
            self.position = position
            self.universe[position] = self
            moved.append(self)
            return True
        return False


class WideBox(Movable):
    label = "[]"

    def __post_init__(self):
        self.universe[self.position] = self
        self.universe[self.x, self.y + 1] = self

    def update_position(self, position: Position) -> None:
        self.universe.pop(self.position)
        self.universe.pop((self.x, self.y + 1))
        self.position = position
        self.universe[self.position] = self
        self.universe[self.x, self.y + 1] = self

    def next_position_range(self, direction: Direction) -> tuple[Position, Position]:
        match direction:
            case Direction.LEFT:
                return (self.x, self.y - 1), (self.x, self.y)
            case Direction.RIGHT:
                return (self.x, self.y + 1), (self.x, self.y + 2)
            case Direction.UP:
                return (self.x - 1, self.y), (self.x - 1, self.y + 1)
            case Direction.DOWN:
                return (self.x + 1, self.y), (self.x + 1, self.y + 1)

    def move(self, direction: Direction, moved: list[Movable]) -> bool:
        positions = self.next_position_range(direction)

        obstacles = list[Movable]()
        for position in positions:
            obstacle = self.universe.get(position)
            if obstacle and obstacle != self:
                obstacles.append(obstacle)
        # if any is wall, do nothing
        if any(o.label == "##" for o in obstacles):
            return False

        for obstacle in obstacles:
            if obstacle in moved:  # already moved
                continue
            if not obstacle.move(direction, moved):
                return False
        self.update_position(positions[0])
        moved.append(self)
        return True

    def is_over(self, position: Position) -> bool:
        ys = (position[1], position[1] - 1)
        return self.x == position[0] and self.y in ys


@dataclass
class Robot(Movable):
    label = "@"

    def move(self, direction: Direction, moved: list[Movable]) -> bool:
        position = self.next_position(direction)
        obstacle = self.universe.get(position)
        if not obstacle or obstacle.move(direction, moved):
            self.update_position(position)

            return True
        while moved:
            movable = moved.pop()
            movable.update_position(movable.undo(direction))
        return False


def part_1() -> int:
    universe = Universe()
    robot: Robot | None = None
    done_mapping = False
    instructions = list[Direction]()
    for x, line in enumerate(input.read_text().splitlines()):
        if not line:
            done_mapping = True
            continue
        if done_mapping:
            instructions.extend(Direction(d) for d in line)
            continue
        for y, label in enumerate(line):
            match label:
                case "#":
                    Wall(x, y, universe)
                case "@":
                    robot = Robot(x, y, universe)
                case "O":
                    Box(x, y, universe)

    assert robot

    for instruction in instructions:
        # print(f"Instruction: {instruction.value}")
        # universe.print()
        robot.move(instruction, [])

    return universe.gps("O")


# def part_2(stdscr: curses.window) -> int:
def part_2() -> int:
    universe = Universe()
    robot: Robot | None = None
    done_mapping = False
    instructions = list[Direction]()
    for x, line in enumerate(input.read_text().splitlines()):
        if not line:
            done_mapping = True
            continue
        if done_mapping:
            instructions.extend(Direction(d) for d in line)
            continue
        for y, label in enumerate(line):
            match label:
                case "#":
                    WideWall(x, y * 2, universe)
                case "@":
                    robot = Robot(x, y * 2, universe)
                case "O":
                    WideBox(x, y * 2, universe)

    assert robot

    # pad = curses.newpad(120, 120)
    for instruction in instructions:
        # pad.addstr(0, 0, f"Instruction: {instruction.value}")
        # rows, cols = stdscr.getmaxyx()
        # universe.wide_print(pad, instruction)
        # pad.refresh(0, 0, 0, 0, rows - 1, cols - 1)
        # pad.getkey()
        robot.move(instruction, [])
    # universe.wide_print(pad, instruction)
    # while True:
    # pad.addstr(0, 0, f"GPS: {universe.gps('[]')}")
    # rows, cols = stdscr.getmaxyx()
    # pad.refresh(0, 0, 0, 0, rows - 1, cols - 1)
    # if pad.getkey() == "\n":
    # break

    return universe.gps("[]")


print(part_1())
# curses.wrapper(part_2)
print(part_2())
