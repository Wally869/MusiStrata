from typing import List, Optional
from typing_extensions import Self
from dataclasses import dataclass

from MusiStrata.Components.Notes2 import Note2
from MusiStrata.Components.Scales import Scale
from MusiStrata.Enums import IntervalQuality


@dataclass
class BaseInterval2:
    interval_number: int
    quality: IntervalQuality

    @classmethod
    def validate(cls) -> bool:
        pass


class Interval2:
    _inner: List[BaseInterval2]

    def __init__(self, interval_number: int, interval_quality: IntervalQuality) -> None:
        self._inner = [BaseInterval2(interval_number, interval_quality)]

    @classmethod
    def from_notes(cls, note_1: Note2, note_2: Note2, context: Optional[Scale] = None) -> Self:
        pass

    @classmethod
    def from_intervals(cls, intervals: List[Self], context: Optional[Scale] = None) -> Self:
        pass

