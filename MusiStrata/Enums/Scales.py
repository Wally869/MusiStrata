from typing import List, Union, cast
from typing_extensions import Self
from enum import Enum

from MusiStrata.Utils import EnumExtensions


class ScaleTones(Enum):
    Major = [2, 2, 1, 2, 2, 2, 1]
    Ionian = [2, 2, 1, 2, 2, 2, 1]
    Dorian = [2, 1, 2, 2, 2, 1, 2]
    Phrygian = [1, 2, 2, 2, 1, 2, 2]
    Lydian = [2, 2, 2, 1, 2, 2, 1]
    Mixolydian = [2, 2, 1, 2, 2, 1, 2]
    Minor = [2, 1, 2, 2, 1, 2, 2]
    MinorHarmonic = [2, 1, 2, 2, 1, 3, 1]
    Aeolian = [2, 1, 2, 2, 1, 2, 2]
    Locrian = [1, 2, 2, 1, 2, 2, 2]


class ScaleModes(Enum):
    Major = 0
    Ionian = 0
    Dorian = 1
    Phrygian = 2
    Lydian = 3
    Mixolydian = 4
    Minor = 5
    Aeolian = 5
    Locrian = 6
    MinorHarmonic = 7

    @classmethod
    def SafeFromStr(cls, name: Union[str, Self]) -> Self:
        if type(name) is ScaleModes:
            return name
        else:
            name = cast(str, name)
            name = name.capitalize()
            for member in cls._member_map_.keys():
                if name == member:
                    return cast(ScaleModes, cls._member_map_[name])
            raise KeyError("ScaleModes - SafeFromStr: {} is not a valid key", name)

    @classmethod
    def SafeFromInt(cls, value: Union[Self, int]) -> Self:
        if type(value) is ScaleModes:
            return value
        else:
            value = cast(int, value)
            return ScaleModes(value)
             
