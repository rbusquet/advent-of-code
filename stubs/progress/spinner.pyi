from _typeshed import Incomplete

from . import Infinite as Infinite

class Spinner(Infinite):
    phases: Incomplete
    hide_cursor: bool
    def update(self) -> None: ...

class PieSpinner(Spinner):
    phases: Incomplete

class MoonSpinner(Spinner):
    phases: Incomplete

class LineSpinner(Spinner):
    phases: Incomplete

class PixelSpinner(Spinner):
    phases: Incomplete
