from typing import List, Tuple, Optional, Union, cast, TYPE_CHECKING
from typing_extensions import Self
from dataclasses import dataclass

from MusiStrata.Components.Notes import Note
from MusiStrata.Components.Scales import Scale
from MusiStrata.Enums import IntervalQuality

from MusiStrata.Data.Intervals2 import INTERVALS_MAP, REVERSE_INTERVALS_MAP, find_interval


@dataclass
class BaseInterval:
    interval_number: int
    quality: IntervalQuality
    tonal_distance: int

    def __str__(self) -> str:
        return "Interval({}-{}--{} semitones)".format(
            self.interval_number, self.quality.name, self.tonal_distance
        )

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def new(cls, interval_number: int, quality: IntervalQuality) -> Self:
        return BaseInterval(
            *find_interval(interval_number=interval_number, quality=quality).unwrap()
        )

    @classmethod
    def from_notes(cls, note_1: Note, note_2: Note) -> Self:
        raise NotImplementedError()

    def to_tuple(self) -> Tuple[int, IntervalQuality, int]:
        return (self.interval_number, self.quality, self.tonal_distance)

    def to_code(self) -> str:
        return REVERSE_INTERVALS_MAP[self.to_tuple()]


class Interval:
    __inner: List[BaseInterval]

    def __init__(self, payload: Union[str, BaseInterval, List[BaseInterval]]) -> None:
        if type(payload) is str:
            self.__inner = [BaseInterval(*INTERVALS_MAP[payload])]
        elif type(payload) is BaseInterval:
            self.__inner = [payload]
        elif type(payload) is List[BaseInterval]:
            payload = cast(List[BaseInterval], payload)
            self.__inner = payload

    def __str__(self) -> str:
        if len(self.__inner) == 1:
            return self.__inner[-1].__str__()
        return "Interval({} Octaves + {})".format(
            len(self.__inner) - 1, self.__inner[-1]
        )

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_code(cls, code: str) -> Self:
        if code in INTERVALS_MAP.keys():
            return Interval(BaseInterval(*INTERVALS_MAP[code]))
        else:
            curr_val = int(code[1:])
            while curr_val > 8:
                curr_val -= 7
            return Interval([BaseInterval(*INTERVALS_MAP[code[0] + str(curr_val)]), BaseInterval(8, IntervalQuality.Perfect, 12)])

    def to_code(self) -> str:
        return self.__inner[-1].to_code()

    @property
    def tonal_distance(self) -> int:
        tonal_distance = 0
        for interval in self.__inner:
            tonal_distance += interval.tonal_distance
        return tonal_distance

    @classmethod
    def new(cls, interval_number: int, interval_quality: IntervalQuality) -> Self:
        return cls([BaseInterval.new(interval_number, interval_quality)])

    @classmethod
    def from_notes(cls, note_1: Note, note_2: Note, context: Optional[Scale] = None) -> Self:
        if context:
            return cls.__from_notes_ctx(note_1, note_2, context)
        else:
            return cls.__from_notes_no_ctx(note_1, note_2)

    @classmethod
    def __from_notes_ctx(cls, note_1: Note, note_2: Note, context: Scale) -> Self:
        raise NotImplementedError()

    @classmethod
    def __from_notes_no_ctx(cls, note_1: Note, note_2: Note) -> Self:
        # reorder notes if needed
        if note_1 > note_2:
            note_2, note_1 = note_1, note_2

        intervals: List[BaseInterval] = []
        while note_2.height - note_1.height > 12:  # tonal_distance > 12:
            intervals.append(
                BaseInterval.new(
                    8,
                    IntervalQuality.Perfect
                )
            )
            note_2 -= 12

        intervals.append(
            BaseInterval.from_notes(note_1, note_2)
        )
        return Interval(intervals)

    @classmethod
    def from_intervals(cls, intervals: List[Self], context: Optional[Scale] = None) -> Self:
        raise NotImplementedError()

    def __radd__(self, note: Note) -> Note:
        return note + self.tonal_distance

    def __rsub__(self, note: Note) -> Note:
        return note - self.tonal_distance

    def __eq__(self, other: Self) -> bool:
        return self.__inner == other.__inner
