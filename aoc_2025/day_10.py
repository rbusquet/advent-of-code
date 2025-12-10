import re
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

input = Path(__file__).parent / "input.txt"


regex = re.compile(
    r"\[(?P<indicators>[.#]+)\] (?P<buttons>[\s\(\)\d,]+) \{(?P<joltages>[\d,]+)\}"
)


def indicator_to_bit_mask(indicators: str) -> int:
    bit_mask = 0
    for i, char in enumerate(indicators):
        if char == "#":
            bit_mask |= 1 << i
    return bit_mask


def buttons_to_bit_mask(buttons: list[int], size: int) -> int:
    bit_mask = 0
    for button in buttons:
        bit_mask |= 1 << button
    return bit_mask


def find_min_presses(target: int, buttons: list[int]) -> int:
    n = len(buttons)

    for size in range(n + 1):
        for combo in combinations(range(n), size):
            result = 0
            for idx in combo:
                result ^= buttons[idx]
            if result == target:
                return size

    return -1


def part_1() -> int:
    count = 0
    for line in input.read_text().splitlines():
        match = regex.match(line)
        if not match:
            continue
        indicator_str = match.group("indicators")
        buttons_str = match.group("buttons")

        target = indicator_to_bit_mask(indicator_str)
        buttons = [
            buttons_to_bit_mask(
                list(map(int, button.strip("()").split(","))), size=len(indicator_str)
            )
            for button in buttons_str.split(" ")
        ]

        min_presses = find_min_presses(target, buttons)
        count += min_presses

    return count


def find_min_presses_joltage(targets: list[int], buttons: list[list[int]]) -> int:
    """
    Find minimum button presses using Mixed Integer Linear Programming.

    Minimize: sum(x_i)  -- total button presses
    Subject to: A @ x = targets  -- each counter reaches its target
    Where: x_i >= 0, x_i is integer
    """
    num_buttons = len(buttons)
    num_counters = len(targets)

    # Build constraint matrix: A[j][i] = 1 if button i affects counter j
    A = np.zeros((num_counters, num_buttons))
    for i, button in enumerate(buttons):
        for counter_idx in button:
            A[counter_idx][i] = 1

    c = np.ones(num_buttons)  # minimize sum of all presses
    constraints = LinearConstraint(A, targets, targets)  # A @ x = targets
    bounds = Bounds(lb=0.0, ub=np.inf)  # x >= 0
    integrality = np.ones(num_buttons, dtype=np.int32)  # all integers

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    if result.success and result.fun is not None:
        return int(round(result.fun))
    return -1


def part_2() -> int:
    count = 0
    for line in input.read_text().splitlines():
        match = regex.match(line)
        if not match:
            continue
        buttons_str = match.group("buttons")
        joltages_str = match.group("joltages")

        targets = list(map(int, joltages_str.split(",")))
        buttons = [
            list(map(int, button.strip("()").split(",")))
            for button in buttons_str.split(" ")
        ]

        min_presses = find_min_presses_joltage(targets, buttons)
        count += min_presses

    return count


print(part_1())
print(part_2())
