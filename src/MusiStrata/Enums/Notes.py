from typing import List, Union, cast, Tuple
from typing_extensions import Self

from enum import Enum
from MusiStrata.Utils import EnumExtensions


class Alterations(Enum):
    Natural = 0,
    Sharp = 1,
    Flat = -1

    @classmethod
    def from_str(cls, val: str) -> Self:
        match val.lower():
            case "":
                return Alterations.Natural
            case "s":
                return Alterations.Sharp
            case "sharp":
                return Alterations.Sharp
            case "f":
                return Alterations.Flat
            case "flat":
                return Alterations.Flat
            case "b":
                return Alterations.Flat
            case default:
                raise KeyError(
                    "Alterations: from_str invalid key - {}".format(val))


class StaffPositions(EnumExtensions.LoopingOrderedEnum):
    C = 0  # "C"
    D = 1  # "D"
    E = 2  # "E"
    F = 3  # "F"
    G = 4  # "G"
    A = 5
    B = 6  # "B"


# need to rewrite NoteNames to handle sharps AND flats
class NoteNames(EnumExtensions.LoopingOrderedEnum):
    C = 0
    Cs = 1
    D = 2
    Ds = 3
    E = 4
    F = 5
    Fs = 6
    G = 7
    Gs = 8
    A = 9
    As = 10
    B = 11

    def get_circle_pos(self) -> Tuple[float, float]:
        """
            Convert note value to a circle position with radius of 1.
            Can be used in distance calculations.
        """
        from numpy import sin, cos, radians
        rads: float = radians(float(self.value) / 12.0 * 360.0)
        return (cos(rads), sin(rads))
    
    def get_circle_distance(self, other: Self) -> float:
        from numpy import sqrt
        self_pos = self.get_circle_pos()
        other_pos = other.get_circle_pos()
        return sqrt((self_pos[0] - other_pos[0]) ** 2 + (self_pos[1] - other_pos[1]) ** 2)

    @classmethod
    def SafeFromStr(cls, name: Union[str, Self]) -> Self:
        if type(name) is NoteNames:
            return name
        else:
            name = cast(str, name)
            name = name.capitalize()
            for member in cls._member_map_.keys():
                if name == member:
                    return cast(NoteNames, cls._member_map_[name])
            raise KeyError("NoteNames - FromStr: {} is not a valid key", name)

    def ToStaffPosition(self) -> StaffPositions:
        if self == NoteNames.A or self == NoteNames.Gs:
            return StaffPositions.A
        elif self == NoteNames.B or self == NoteNames.As:
            return StaffPositions.B
        elif self == NoteNames.C:
            return StaffPositions.C
        elif self == NoteNames.D or self == NoteNames.Cs:
            return StaffPositions.D
        elif self == NoteNames.E or self == NoteNames.Ds:
            return StaffPositions.E
        elif self == NoteNames.F:
            return StaffPositions.F
        else:  # self == NoteNames.G or self == NoteNames.Fs:
            return StaffPositions.G

    @classmethod
    def SafeFromInt(cls, value: Union[int, Self]) -> Self:
        if type(value) is NoteNames:
            return value
        else:
            value = cast(int, value)
            return cast(NoteNames, cls._value2member_map_[value])

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class NoteNames2(EnumExtensions.LoopingOrderedEnum):
    C = 0
    Cs = 1
    Db = 1
    D = 2
    Ds = 3
    Eb = 3
    E = 4
    F = 5
    Fs = 6
    Gb = 6
    G = 7
    Gs = 8
    Ab = 8
    A = 9
    As = 10
    Bb = 10
    B = 11

    @classmethod
    def SafeFromStr(cls, name: Union[str, Self]) -> Self:
        if type(name) is NoteNames2:
            return name
        else:
            name = cast(str, name)
            name = name.capitalize()
            for member in cls._member_map_.keys():
                if name == member:
                    return cast(NoteNames2, cls._member_map_[name])
            raise KeyError("NoteNames2 - FromStr: {} is not a valid key", name)

    def ToStaffPosition(self) -> StaffPositions:
        if self == NoteNames2.A or self == NoteNames2.Gs:
            return StaffPositions.A
        elif self == NoteNames2.B or self == NoteNames2.As:
            return StaffPositions.B
        elif self == NoteNames2.C:
            return StaffPositions.C
        elif self == NoteNames2.D or self == NoteNames2.Cs:
            return StaffPositions.D
        elif self == NoteNames2.E or self == NoteNames2.Ds:
            return StaffPositions.E
        elif self == NoteNames2.F:
            return StaffPositions.F
        else:  # self == NoteNames2.G or self == NoteNames2.Fs:
            return StaffPositions.G

    @classmethod
    def SafeFromInt(cls, value: Union[int, Self]) -> Self:
        if type(value) is NoteNames2:
            return value
        else:
            value = cast(int, value)
            return cast(NoteNames2, cls._value2member_map_[value])

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))
