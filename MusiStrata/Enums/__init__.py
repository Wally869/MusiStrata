from typing import List, Union
from enum import Enum

from MusiStrata.Utils import EnumExtensions


class TrackType(Enum):
    Instrument = 0,
    Drums = 1,
    Sample = 2


class Alterations(Enum):
    Natural = 0,
    Sharp = 1,
    Flat = -1


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
    def SafeFromStr(cls, name: str) -> "ChordBase":
        if name.__class__ is ChordBase:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]


class ScaleChordExtension(Enum):
    Seventh = 7
    Ninth = 9
    Eleventh = 11
    Thirteenth = 13

    @classmethod
    def SafeFromStr(cls, name: str) -> "ScaleChordExtension":
        if name.__class__ is ScaleChordExtension:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]
        raise KeyError("ScaleChordExtension - SafeFromStr: {} is not a valid key", name)

    @classmethod
    def SafeFromInt(cls, val: int) -> "ScaleChordExtension":
        if val.__class__ is ScaleChordExtension:
            return val        
        if val == 7:
            return cls.Seventh
        elif val == 9:
            return cls.Ninth
        elif val == 11:
            return cls.Eleventh
        elif val == 13:
            return cls.Thirteenth
        else:
            raise ValueError("ScaleChordExtension - SafeFromInt: {} is not a valid value", val)


class ChordExtension(Enum):
    SeventhMajor = (7, "Major")
    M7 = (7, "Major")
    SeventhMinor = (7, "Minor")
    m7 = (7, "Minor")
    NinthMajor = (9, "Major")
    M9 = (9, "Major")
    NinthMinor = (9, "Minor")
    m9 = (9, "Minor")
    EleventhPerfect = (11, "Perfect")
    P11 = (11, "Perfect")
    EleventhDiminished = (11, "Diminished")
    D11 = (11, "Diminished")
    ThirteenthMajor = (13, "Major")
    M13 = (13, "Major")
    ThirteenthMinor = (13, "Minor")
    m13 = (13, "Minor")

    @classmethod
    def SafeFromStr(cls, name: Union[str, "ChordExtension"]) -> "ChordExtension":
        if name.__class__ is ChordExtension:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]
        raise KeyError("ChordExtension - FromStr: {} is not a valid key", name)


class StaffPositions(EnumExtensions.LoopingOrderedEnum):
    C = 0  #"C"
    D = 1  #"D"
    E = 2  #"E"
    F = 3  #"F"
    G = 4  #"G"
    A = 5
    B = 6  #"B"


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

    @classmethod
    def SafeFromStr(cls, name: Union[str, "NoteNames"]) -> "NoteNames":
        if name.__class__ is NoteNames:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]
        raise KeyError("NoteNames - FromStr: {} is not a valid key", name)

    def ToStaffPosition(self):
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
        elif self == NoteNames.G or self == NoteNames.Fs:
            return StaffPositions.G

    @classmethod
    def SafeFromInt(cls, value: Union[int, "NoteNames"]) -> "NoteNames":
        if value.__class__ is NoteNames:
            return value
        return cls._value2member_map_[value]
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class ScaleModes(Enum):
    Ionian = 0
    Dorian = 1
    Phrygian = 2
    Lydian = 3
    Mixolydian = 4
    Aeolian = 5
    Locrian = 6

    @classmethod
    def ToString(cls) -> str:
        # not useful since can use property name  
        if cls == ScaleModes.Ionian:
            return "Ionian"
        elif cls == ScaleModes.Dorian:
            return "Dorian"
        elif cls == ScaleModes.Phrygian:
            return "Phrygian"
        elif cls == ScaleModes.Lydian:
            return "Lydian"
        elif cls == ScaleModes.Mixolydian:
            return "Mixolydian"
        elif cls == ScaleModes.Aeolian:
            return "Aeolian"
        elif cls == ScaleModes.Locrian:
            return "Locrian"

    @classmethod
    def SafeFromStr(cls, name: str) -> "ScaleModes":
        if name.__class__ is ScaleModes:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]
        raise KeyError("ScaleModes - SafeFromStr: {} is not a valid key", name)

    @classmethod
    def SafeFromInt(cls, value: int) -> "ScaleModes":
        if value.__class__ is ScaleModes:
            return value
        for elem in cls:
            if elem.value == value:
                return elem
        raise KeyError("ScaleModes - SafeFromInt: {} is not a valid key", value)
             


class Mode(Enum):
    Major = [1, 1, 0.5, 1, 1, 1, 0.5]
    Minor = [1, 0.5, 1, 1, 0.5, 1, 1]
    MinorMelodic = [1, 0.5, 1, 1, 0.5, 1.5, 0.5]

    @classmethod
    def SafeFromStr(cls, name: str) -> "Mode":
        if name.__class__ is Mode:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]
        raise KeyError("Mode - SafeFromStr: {} is not a valid key", name)


class ScaleTones(Enum):
    Major = [1, 1, 0.5, 1, 1, 1, 0.5]
    Minor = [1, 0.5, 1, 1, 0.5, 1, 1]
    MinorMelodic = [1, 0.5, 1, 1, 0.5, 1.5, 0.5]


class IntervalQuality(Enum):
    Minor = "Minor"
    Major = "Major"
    Perfect = "Perfect"
    Diminished = "Diminished"
    Augmented = "Augmented"
    DoublyDiminished = "DoublyDiminished"
    DoublyAugmented = "DoublyAugmented"

    @classmethod
    def SafeFromStr(cls, name: str):
        if name.__class__ is IntervalQuality:
            return name
        for member in cls._member_map_.keys():
            if name == member:
                return cls._member_map_[name]
        if name == "Doubly Diminished":
            return cls.DoublyDiminished
        elif name == "Doubly Augmented":
            return cls.DoublyDiminished
        else:
            raise KeyError("Unknown Interval Quality - key: {}".format(name))

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
