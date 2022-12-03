from _typeshed import Incomplete

from . import Progress as Progress
from .colors import color as color

class Bar(Progress):
    width: int
    suffix: str
    bar_prefix: str
    bar_suffix: str
    empty_fill: str
    fill: str
    color: Incomplete
    def update(self) -> None: ...

class ChargingBar(Bar):
    suffix: str
    bar_prefix: str
    bar_suffix: str
    empty_fill: str
    fill: str

class FillingSquaresBar(ChargingBar):
    empty_fill: str
    fill: str

class FillingCirclesBar(ChargingBar):
    empty_fill: str
    fill: str

class IncrementalBar(Bar):
    phases: Incomplete
    def update(self) -> None: ...

class PixelBar(IncrementalBar):
    phases: Incomplete

class ShadyBar(IncrementalBar):
    phases: Incomplete
