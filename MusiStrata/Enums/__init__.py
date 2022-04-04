from enum import Enum 

from MusiStrata.Utils import EnumExtensions



class ChordBase(Enum):
    Major = 0
    Minor = 1
    Diminished = 2
    Suspended2 = 3
    Suspended4 = 4
    Augmented = 5


class ChordExtension(Enum):
    SeventhMajor = 0
    SeventhMinor = 1
    Ninth = 2
    Eleventh = 3
    Thirteenth = 4


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
    Ionian = "Ionian" 
    Dorian ="Dorian" 
    Phrygian = "Phrygian" 
    Lydian = "Lydian"
    Mixolydian = "Mixolydian"
    Aeolian = "Aeolian"
    Locrian = "Locrian"    


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

