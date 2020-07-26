from __future__ import annotations
from typing import List, Tuple, Dict, Union

from .utils import LoopingOrderedEnum, OrderedEnum

from copy import deepcopy


ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]

ALL_STAFF_POSITIONS = [
    "A", "B", "C", "D", "E", "F", "G"
]


# Values give the distance between notes in term of halftones
# s denotes a Sharp
class NoteNames(LoopingOrderedEnum):
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


class StaffPositions(LoopingOrderedEnum):
    C = 0
    D = 1
    E = 2
    F = 3
    G = 4
    A = 5
    B = 6


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
    "Gs": "A"
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
            raise ValueError("Octave must be a non-negative integer.")

        self._Name = NoteNames[Name]
        self._Octave = Octave

    @property
    def Name(self) -> NoteNames:
        return self._Name

    @Name.setter
    def Name(self, newName: str) -> None:
        try:
            self._Name = NoteNames[newName]
        except TypeError:
            raise TypeError("'{}' is not a valid note name. Expected type is str.")
        except KeyError:
            raise KeyError("'{}' not a valid note name. Check Notes.ALL_NOTES for valid note names".format(newName))

    @property
    def Octave(self) -> int:
        return self._Octave

    @Octave.setter
    def Octave(self, newOctave: int) -> None:
        if type(newOctave) != int:
            raise TypeError("Octave must be a non-negative integer.")
        # Separating value checking from type checking
        if newOctave < 0:
            raise ValueError("Octave must be a non-negative integer.")
        self._Octave = newOctave

    def __hash__(self):
        return self.Height

    def __str__(self) -> str:
        return "Note({})".format(self.Name.name + str(self.Octave))

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if self.__class__ is not other.__class__:
            return False
        else:
            if self.Name == other.Name and self.Octave == other.Octave:
                return True
            else:
                return False

    def __ge__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height >= other.Height
        return NotImplemented

    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height > other.Height
        return NotImplemented

    def __le__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height <= other.Height
        return NotImplemented

    def __lt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height < other.Height
        return NotImplemented

    def __add__(self, other: int) -> Note:
        if type(other) == int:
            # error if other is negative. Fixing this
            if other < 0:
                return self.__sub__(abs(other))
            else:
                outName, deltaOctave = self.Name + other

                return Note(
                    Name=outName.name,
                    Octave=self.Octave + deltaOctave
                )
        else:
            return NotImplemented

    def __sub__(self, other: Union[int, Note]) -> Union[int, Note]:
        if self.__class__ is other.__class__:
            return self.GetTonalDistance(other)
        elif type(other) == int:
            if other < 0:
                return self.__add__(abs(other))
            else:
                outName, deltaOctave = self.Name - other

                return Note(
                    Name=outName.name,
                    Octave=self.Octave + deltaOctave
                )
        else:
            return NotImplemented

    # Added this to expand scales. Can also use Note + 12 for octave difference
    # but I thought additional method would be nice
    def NewFromOctaveDifference(self, octaveDiff: int) -> Note:
        newNote = deepcopy(self)
        newNote.Octave += octaveDiff
        return newNote

    @property
    def Height(self) -> int:
        return (self.Octave + 1) * 12 + self.Name.value

    @property
    def Frequency(self) -> float:
        # Using this as reference: https://pages.mtu.edu/~suits/notefreqs.html
        return 16.35 * (2 ** self.Octave) * (2 ** (1 / 12)) ** self.Name.value

    # Return distance between this note and another in term of semitones
    def GetTonalDistance(self, other) -> int:
        if self.__class__ is other.__class__:
            return self.Height - other.Height
        return NotImplemented

    # Returning a positive tonal distance
    def GetRootedTonalDistance(self, other) -> int:
        if self.__class__ is other.__class__:
            return max(
                self.Height - other.Height,
                other.Height - self.Height
            )
        return NotImplemented

    def GetStaffPositionAsEnumElem(self) -> StaffPositions:
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
            if outValue == 1:
                if abs(self - other) <= 2:
                    outValue = 1
                else:
                    outValue = 8

            return outValue

        return NotImplemented

    @classmethod
    def FromHeight(cls, height: int) -> Note:
        octave = height // 12
        name = NoteNames.GetElementFromValue(height - octave * 12).name
        return Note(Name=name, Octave=octave - 1)
