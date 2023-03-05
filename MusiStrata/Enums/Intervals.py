from typing import List, Union, cast
from typing_extensions import Self
from enum import Enum

from MusiStrata.Utils import EnumExtensions


class IntervalQuality(Enum):
    Minor = "Minor"
    Major = "Major"
    Perfect = "Perfect"
    Diminished = "Diminished"
    Augmented = "Augmented"
    DoublyDiminished = "DoublyDiminished"
    DoublyAugmented = "DoublyAugmented"

    @classmethod    
    def SafeFromStr(cls, name: Union[Self, str]) -> Self:
        if type(name) is IntervalQuality:
            return name
        else:
            name = cast(str, name)
            for member in cls._member_map_.keys():
                if name == member:
                    return cast(IntervalQuality, cls._member_map_[name])
            match name:
                case "Doubly Diminished":
                    return cls.DoublyDiminished
                case "Doubly Augmented":
                    return cls.DoublyAugmented
                case "m":
                    return cls.Minor
                case "M":
                    return cls.Major
                case "P":
                    return cls.Perfect
                case "D":
                    return cls.Diminished
                case "A":
                    return cls.Augmented
                case _:
                    raise KeyError("Unknown Interval Quality - key: {}".format(name))

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
