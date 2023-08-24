from typing import List, Tuple, Optional, Union, cast, TYPE_CHECKING
from typing_extensions import Self
from MusiStrata.Enums import IntervalQuality
from MusiStrata.Data.Intervals2 import INTERVALS_MAP, REVERSE_INTERVALS_MAP, find_interval
from MusiStrata.Components import Note  # , Scale

from multimethod import multimethod

from dataclasses import dataclass


@dataclass
class Interval2:
    interval_number: int
    quality: IntervalQuality
    tonal_distance: int

    def __init__(self, code: str) -> None:
        if code in INTERVALS_MAP.keys():
            (self.interval_number, self.quality,
             self.tonal_distance) = INTERVALS_MAP[code]
        else:
            self.quality = IntervalQuality.SafeFromStr(code[0])
            self.tonal_distance = 0
            curr_val = int(code[1:])
            while curr_val > 8:
                curr_val -= 7
                self.tonal_distance += 12
            # return Interval([BaseInterval(*INTERVALS_MAP[code[0] + str(curr_val)]), BaseInterval(8, IntervalQuality.Perfect, 12)])
            temp = INTERVALS_MAP[code[0] + str(curr_val)]
            self.interval_number = int(code[1:])
            self.tonal_distance += temp[2]
            self.quality = temp[1]

    @multimethod
    def new(code: str) -> Self:
        return Interval2(code)

    @multimethod
    def new(interval_number: int, quality: IntervalQuality, tonal_distance: int) -> Self:
        obj = Interval2.__new__(Interval2)
        obj.interval_number = interval_number
        obj.quality = quality
        obj.tonal_distance = tonal_distance
        return obj

    @multimethod
    def new(interval_number: int, quality: IntervalQuality) -> Self:
        obj = Interval2.__new__(Interval2)
        obj.interval_number = interval_number
        obj.quality = quality
        # need to get tonal distance from somewhere else
        # obj.tonal_distance = tonal_distance
        raise Exception("not implemented")
        return obj

    """
    @classmethod
    def from_notes(cls, note_1: Note, note_2: Note, context: Optional[Scale] = None) -> Self:
        if context:
            return cls.__from_notes_ctx(note_1, note_2, context)
        else:
            return cls.__from_notes_no_ctx(note_1, note_2)
    """

    def __radd__(self, note: Note) -> Note:
        return note + self.tonal_distance

    def __rsub__(self, note: Note) -> Note:
        return note - self.tonal_distance

    def __eq__(self, other: Self) -> bool:
        return self.tonal_distance == other.tonal_distance and self.interval_number == other.interval_number and self.quality == other.quality
