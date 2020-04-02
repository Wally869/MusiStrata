from enum import Enum

from .Intervals import *
from .utils import LoopingOrderedEnum, OrderedEnum

from typing import List, Dict

ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]

ALL_STAFF_POSITIONS = [
    "A", "B", "C", "D", "E", "F", "G"
]


# Values give the distance between notes in term of halftones
# s denotes a Sharp
class NoteNames(LoopingOrderedEnum):
    A = 0
    As = 1
    B = 2
    C = 3
    Cs = 4
    D = 5
    Ds = 6
    E = 7
    F = 8
    Fs = 9
    G = 10
    Gs = 11


class StaffPositions(LoopingOrderedEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6


# A note with a sharp is considered to belong to higher staff
NOTE_NAME_TO_STAFF = {
    "A": "A",
    "As": "B",
    "B": "B",
    "C": "C",
    "Cs": "D",
    "D": "D",
    "Ds": "E",
    "E": "E",
    "F": "F",
    "Fs": "G",
    "G": "G",
    "Gs": "G"
}


class Note(object):
    def __init__(self, Name: str = "A", Octave: int = 5):
        # can't call methods in init?
        if Name not in ALL_NOTES:
            raise KeyError("'{}' not a valid note name. Check Notes.ALL_NOTES for valid note names".format(Name))

        # Need to check max octave for Midi
        if type(Octave) != int:
            raise TypeError("Octave must be a non-negative integer.")

        if Octave < 0:
            raise ValueError("Octave must be a non-negative.")

        self.__Name = NoteNames[Name]
        self.__Octave = Octave

    @property
    def Name(self):
        return self.__Name

    @Name.setter
    def Name(self, newName: str):
        # raise KeyError("'{}' not a valid note name. Check Notes.ALL_NOTES for valid note names".format(newName))
        self.__Name = NoteNames[newName]

    @property
    def Octave(self):
        return self.__Octave

    @Octave.setter
    def Octave(self, newOctave: int):
        if type(newOctave) != int:
            raise TypeError("Octave must be a non-negative integer.")
        # Separating value checking from type checking
        if newOctave < 0:
            raise TypeError("Octave must be a non-negative integer.")
        self.__Octave = newOctave

    def __str__(self):
        return "Note({})".format(self.Name.name + str(self.Octave))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) is not Note:
            return False
        else:
            if self.Name == other.Name and self.Octave == other.Octave:
                return True
            else:
                return False

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() >= other.ComputeHeight()
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() > other.ComputeHeight()
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() <= other.ComputeHeight()
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() < other.ComputeHeight()
        return NotImplemented

    def __add__(self, other: int):
        if type(other) is not int:
            return NotImplemented
        else:
            # error if other is negative. Fixing this
            if (other < 0):
                return self.__sub__(abs(other))
            else:
                outName, deltaOctave = self.Name + other

                return Note(
                    Name=outName.name,
                    Octave=self.Octave + deltaOctave
                )

    def __sub__(self, other: int):
        if self.__class__ is other.__class__:
            return self.ComputeTonalDistance(other)
        elif type(other) == int:
            if (other < 0):
                return self.__add__(abs(other))
            else:
                outName, deltaOctave = self.Name - other

                return Note(
                    Name=outName.name,
                    Octave=self.Octave + deltaOctave
                )
        else:
            return NotImplemented

    def ComputeHeight(self) -> int:
        return self.Octave * 12 + self.Name.value

    # Return distance between this note and another in term of semitones
    def ComputeTonalDistance(self, other) -> int:
        if self.__class__ is other.__class__:
            return self.ComputeHeight() - other.ComputeHeight()
        return NotImplemented

    # Returning a positive tonal distance
    def ComputeRootedTonalDistance(self, other) -> int:
        if self.__class__ is other.__class__:
            return max(
                self.ComputeHeight() - other.ComputeHeight(),
                other.ComputeHeight() - self.ComputeHeight()
            )
        return NotImplemented

    def GetStaffPositionAsEnumElem(self):
        return StaffPositions[self.GetStaffPositionAsLetter()]

    def GetStaffPositionAsLetter(self) -> str:
        return NOTE_NAME_TO_STAFF[self.Name.name]

    def GetStaffPositionAsInteger(self) -> int:
        return StaffPositions[
            self.GetStaffPositionAsLetter()
        ].value

    # This is order dependent. Self should be the root note of the chord
    def GetIntervalNumber(self, other) -> int:
        if self.__class__ is other.__class__:
            staff1 = self.GetStaffPositionAsEnumElem()
            staff2 = other.GetStaffPositionAsEnumElem()

            outValue = staff2 - staff1

            # lowest note is root of chord and therefore the base for interval calculation
            # Incrementing by one so that it makes sense (a A - B chord is a second, but this return 1)
            outValue += 1

            # adding exception for octave
            if staff1 == staff2:
                if self != other:
                    outValue = 8

            return outValue

        return NotImplemented

    def GetIntervalSpecs(self, other):
        if self.__class__ is other.__class__:
            intervalNumber = self.GetIntervalNumber(other)
            deltaTone = self.ComputeRootedTonalDistance(other)

            return {
                "IntervalNumber": intervalNumber,
                "TonalDistance": deltaTone
            }

        return NotImplemented

    """
    specs has form: 
    {
        "IntervalNumber": (int) intervalNumber,
        "TonalDistance": (int) deltaTone
    }

    See GetIntervalSpecs above
    maybe not in this file?
    """

    def ComputeNoteFromIntervalSpecs(self, specs: Dict):
        pass


def CreateNoteFromHeight(height: int) -> Note:
    octave = height // 12
    name = NoteNames.GetElementFromValue(height - octave * 12).name

    return Note(Name=name, Octave=octave)
