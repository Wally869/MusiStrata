from typing import List, Tuple, Optional, Union, cast, TYPE_CHECKING
from typing_extensions import Self
from MusiStrata.Enums import IntervalQuality
from MusiStrata.Data.Intervals import INTERVALS_MAP, find_interval
from MusiStrata.Components import Note  # , Scale

from multimethod import multimethod

#from dataclasses import dataclass


#@dataclass
class Interval:
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
        return Interval(code)

    @multimethod
    def new(interval_number: int, quality: IntervalQuality, tonal_distance: int) -> Self:
        obj = Interval.__new__(Interval)
        (obj.interval_number, obj.quality,
            obj.tonal_distance) = find_interval(interval_number, quality, tonal_distance).unwrap()
        return obj

    @multimethod
    def new(quality: IntervalQuality, tonal_distance: int) -> Self:
        obj = Interval.__new__(Interval)
        (obj.interval_number, obj.quality,
            obj.tonal_distance) = find_interval(quality=quality, tonal_distance=tonal_distance).unwrap()
        return obj

    @multimethod
    def new(interval_number: int, quality: IntervalQuality) -> Self:
        obj = Interval.__new__(Interval)
        (obj.interval_number, obj.quality,
            obj.tonal_distance) = find_interval(interval_number, quality).unwrap()
        return obj
    
    def __radd__(self, note: Note) -> Note:
        return note + self.tonal_distance

    def __rsub__(self, note: Note) -> Note:
        return note - self.tonal_distance

    def __eq__(self, other: Self) -> bool:
        return self.tonal_distance == other.tonal_distance and self.interval_number == other.interval_number and self.quality == other.quality

    def __str__(self) -> str:
        return "Interval({})".format(self.quality.ToCode() + str(self.interval_number))
    
    def __repr__(self) -> str:
        return self.__str__()
