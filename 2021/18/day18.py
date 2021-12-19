from __future__ import annotations
from typing import Union
import more_itertools.more

Number = tuple[Union["Number", int], Union["Number", int]]  # type: ignore[misc]


def addition(left: Number, right: Number) -> Number:
    return reduce((left, right))


def reduce(number: Number, level: int = 0) -> Number | int:
    if level == 4:
        match
    left, right = number
