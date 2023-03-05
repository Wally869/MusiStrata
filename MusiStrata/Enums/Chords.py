from typing import List, Union, cast
from typing_extensions import Self

from enum import Enum
from MusiStrata.Utils import EnumExtensions


class ChordBase(Enum):
    Major = [(1, "Perfect"), (3, "Major"), (5, "Perfect")]
    M = [(1, "Perfect"), (3, "Major"), (5, "Perfect")]
    Minor = [(1, "Perfect"), (3, "Minor"), (5, "Perfect")]
    m = [(1, "Perfect"), (3, "Minor"), (5, "Perfect")]
    Diminished = [(1, "Perfect"), (3, "Minor"), (5, "Diminished")]
    D = [(1, "Perfect"), (3, "Minor"), (5, "Diminished")]
    Suspended2 = [(1, "Perfect"), (2, "Major"), (5, "Perfect")]
    sus2 = [(1, "Perfect"), (2, "Major"), (5, "Perfect")]
    Sus2 = [(1, "Perfect"), (2, "Major"), (5, "Perfect")]
    Suspended4 = [(1, "Perfect"), (4, "Perfect"), (5, "Perfect")]
    sus4 = [(1, "Perfect"), (4, "Perfect"), (5, "Perfect")]
    Sus4 = [(1, "Perfect"), (4, "Perfect"), (5, "Perfect")]
    Augmented = [(1, "Perfect"), (3, "Major"), (5, "Augmented")]
    Aug = [(1, "Perfect"), (3, "Major"), (5, "Augmented")]
    aug = [(1, "Perfect"), (3, "Major"), (5, "Augmented")]

    @classmethod
    def SafeFromStr(cls, name: Union[Self, str]) -> Self:
        if type(name) is ChordBase:
            return name
        else:
            name = cast(str, name)
            for member in cls._member_map_.keys():
                if name == member:
                    return cast(ChordBase, cls._member_map_[name])
            raise KeyError("ChordBase - SafeFromStr: {} is not a valid key", name)            

