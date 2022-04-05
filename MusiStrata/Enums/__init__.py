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
    def FromStr(cls, name: str) -> "ChordBase":
        for member in cls._member_names_:
            if name == member:
                return cls._member_map_[name]


class ChordExtension(Enum):
    SeventhMajor = (7, "Major")
    M7 = (7, "Major")
    SeventhMinor = (7, "Minor")
    m7 = (7, "Minor")
    NinthMajor = (9, "Major")
    M9 = (9, "Major")
    NinthMinor = (9, "Minor")
    m9 = (9, "Minor")
    EleventhMajor = (11, "Major")
    M11 = (11, "Major")
    EleventhMinor = (11, "Minor")
    m11 = (11, "Minor")
    ThirteenthMajor = (13, "Major")
    M13 = (13, "Major")
    ThirteenthMinor = (13, "Minor")
    m13 = (13, "Minor")

    @classmethod
    def FromStr(cls, name: str) -> "ChordBase":
        for member in cls._member_names_:
            if name == member:
                return cls._member_map_[name]
        raise KeyError("ChordExtension - FromStr: {} is not a valid key", name)


class StaffPosition(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


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

    def ToStaffPosition(self):
        if self == NoteNames.A or self == NoteNames.Gs:
            return StaffPosition.A
        elif self == NoteNames.B or self == NoteNames.As:
            return StaffPosition.B
        elif self == NoteNames.C:
            return StaffPosition.C
        elif self == NoteNames.D or self == NoteNames.Cs:
            return StaffPosition.D
        elif self == NoteNames.E or self == NoteNames.Ds:
            return StaffPosition.E
        elif self == NoteNames.F:
            return StaffPosition.F
        elif self == NoteNames.G or self == NoteNames.Fs:
            return StaffPosition.G



class Mode(Enum):
    Major = 0,
    Minor = 1
    MinorMelodic = 2


class ScaleMode(Enum):
    Ionian = 0
    Dorian = 1 
    Phrygian = 2 
    Lydian = 3
    Mixolydian = 4
    Aeolian = 5
    Locrian = 6    

    @classmethod
    def ToString(cls) -> str:
        if cls == ScaleMode.Ionian:
            return "Ionian" 
        elif cls == ScaleMode.Ionian:
            return "Dorian" 
        elif cls == ScaleMode.Ionian:
            return "Phrygian" 
        elif cls == ScaleMode.Ionian:
            return "Lydian" 
        elif cls == ScaleMode.Ionian:
            return "Mixolydian" 
        elif cls == ScaleMode.Ionian:
            return "Aeolian" 
        elif cls == ScaleMode.Ionian:
            return "Locrian" 

    @classmethod
    def FromStr(cls, name: str) -> "ScaleMode":
        for member in cls._member_names_:
            if name == member:
                return cls._member_map_[name]
        raise KeyError("ScaleMode - FromStr: {} is not a valid key", name)


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
    def FromStr(cls, name: str):
        for member in cls._member_names_:
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

