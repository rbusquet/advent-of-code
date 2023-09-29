from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


def man_dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Returns the Manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class sensor:
    """A sensor has its center position and its exclusion range"""

    def __init__(self, pos: tuple[int, int], beacon: tuple[int, int]) -> None:
        self.position: tuple[int, int] = pos
        self.range: int = man_dist(beacon, self.position)

    def in_exclusion_range(self, point: tuple[int, int]) -> bool:
        """Returns True if point is inside this sensor's exclusion range"""
        return self.range >= man_dist(self.position, point)


def parse(string: str) -> list[sensor]:
    """Parses the advent input and returns the list of sensors"""
    result: list[sensor] = []
    for line in string.splitlines():
        # line: "Sensor at x=2391367, y=3787759: closest beacon is at x=2345659, y=4354867"
        first, second = line.split(": ")

        # first:  "Sensor at x=2391367, y=3787759"
        sensor_x, sensor_y = first[12:].split(", ")
        sensor_x = int(sensor_x)
        sensor_y = int(sensor_y[2:])

        # second: "closest beacon is at x=2345659, y=4354867"
        beacon_x, beacon_y = second[23:].split(", ")
        beacon_x = int(beacon_x)
        beacon_y = int(beacon_y[2:])

        result.append(sensor((sensor_x, sensor_y), (beacon_x, beacon_y)))

    return result


def is_free(point: tuple[int, int], sensors: list[sensor]) -> bool:
    """Returns True if point is outside the exclusion range of every sensor in sensors"""
    for sensor in sensors:
        if sensor.in_exclusion_range(point):
            return False
    return True


def main(args: Arguments) -> int:
    search_area = 4000000
    sensors = parse(args.infile.read())
    lines: dict[tuple[bool, int], int] = {}

    for sensor in sensors:
        top_rising = (
            True,  # m is 1
            sensor.position[1] - sensor.range - 1 - sensor.position[0],  # this is q
        )

        top_descending = (
            False,  # m is -1
            sensor.position[1] - sensor.range - 1 + sensor.position[0],
        )

        bottom_rising = (
            True,
            sensor.position[1] + sensor.range + 1 - sensor.position[0],
        )

        bottom_descending = (
            False,
            sensor.position[1] + sensor.range + 1 + sensor.position[0],
        )

        for line in [top_rising, top_descending, bottom_rising, bottom_descending]:
            """I'm counting the occurrences of each line"""
            if line in lines:
                lines[line] += 1
            else:
                lines[line] = 1

    rising_lines: list[int] = []
    descending_lines: list[int] = []

    for line, count in lines.items():
        """
        I only keep the lines that appear at least two times.
        I do this because I know that the single free spot lies where 4 lines intersect
        (2 rising and 2 descending)
        """
        if count > 1:
            if line[0]:
                descending_lines.append(line[1])
            else:
                rising_lines.append(line[1])

    points: list[tuple[int, int]] = []

    for rising_q in rising_lines:
        for descending_q in descending_lines:
            """I calculate the intersections between all the rising and descending lines i got"""
            x = (rising_q - descending_q) // 2
            y = x + descending_q
            point = (x, y)
            points.append(point)

    for point in points:
        """I check which of the intersections is the free point"""
        if (
            (0 <= point[1] <= search_area)
            and (0 <= point[0] <= search_area)
            and is_free(point, sensors)
        ):
            return point[0] * 4000000 + point[1]

    raise ValueError  # If the point is not found then the input is wrong


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    print(main(args))
