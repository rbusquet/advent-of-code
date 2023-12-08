from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def solve(times: list[int], distances: list[int]) -> int:
    total = 1
    for i, time in enumerate(times):
        distance_to_beat = distances[i]

        # distance = (total_time - time_holding) * time_holding
        #            ^ time left after holding     ^ speed after holding for time
        # distance = time_holding * total_time - time_holding ** 2
        ways_to_beat = 0

        for time_holding in range(time):
            distance = (time - time_holding) * time_holding
            if distance > distance_to_beat:
                ways_to_beat += 1
        total *= ways_to_beat
    return total


if __name__ == "__main__":
    print(solve([7, 15, 30], [9, 40, 200]))
    print(solve([61, 67, 75, 71], [430, 1036, 1307, 1150]))
    print(solve([71530], [940200]))
    print(solve([61677571], [430103613071150]))
