from enum import Enum

from .Intervals import *
from .utils import OrderedEnum

from typing import List, Dict


ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]

ALL_STAFF_POSITIONS = [
    "A", "B", "C", "D", "E", "F", "G"
]


# Values give the distance between notes in term of halftones
# s denotes a Sharp
class NoteNames(OrderedEnum):
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


class StaffPositions(OrderedEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6


class Note(object):
    def __init__(self, Name: str = "A", Octave: int = 5):
        # can't call methods in init?
        if Name not in ALL_NOTES:
            raise KeyError("'{}' not a valid note name. Check Notes.ALL_NOTES for valid note names".format(Name))

        # Need to check max octave for Midi
        if type(Octave) != int:
            raise TypeError("Octave must be a non-negative integer.")

        if Octave < 0 :
            raise ValueError("Octave must be a non-negative.")

        self.__Name = Name
        self.__Octave = Octave

    # Need to check name to see if correct
    @staticmethod
    def CheckNameCorrect(name: str):
        if name in ALL_NOTES:
            return True
        else:
            return False

    @property
    def Name(self):
        return self.__Name

    @Name.setter
    def Name(self, newName: str):
        if self.CheckNameCorrect(newName):
            self.__Name = newName
        else:
            raise KeyError("'{}' not a valid note name. Check Notes.ALL_NOTES for valid note names".format(newName))

    @property
    def Octave(self):
        return self.__Octave

    @Octave.setter
    def Octave(self, newOctave: int):
        if type(newOctave) != int:
            raise TypeError("Octave must be a non-negative integer")
        # Separating value checking from type checking
        if newOctave < 0:
            raise TypeError("Octave must be a non-negative integer")
        self.__Octave = newOctave

    def __str__(self):
        return "Note({})".format(self.Name + str(self.Octave))

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
                currNoteId = self.GetNoteId() + other
                deltaOctave = 0
                while currNoteId >= len(NoteNames):
                    deltaOctave += 1
                    currNoteId -= len(NoteNames)

                return Note(
                    Name=NoteNames[
                        self.GetNoteNameFromNamesEnum(currNoteId)
                    ].name,
                    Octave=self.Octave + deltaOctave
                )

    def __sub__(self, other: int):
        if self.__class__ is other.__class__:
            return self.ComputeTonalDistance(other)
        elif type(other) == int:
            if (other < 0):
                return self.__add__(abs(other))
            else:
                currNoteId = self.GetNoteId() - other
                deltaOctave = 0
                # handling negative values
                while currNoteId < 0:
                    deltaOctave -= 1
                    currNoteId += len(NoteNames)

                return Note(
                    Name=NoteNames[
                        self.GetNoteNameFromNamesEnum(currNoteId)
                    ].name,
                    Octave=self.Octave + deltaOctave
                )
        else:
            return NotImplemented

    def GetNoteId(self) -> int:
        for n in NoteNames:
            if n.name == self.Name:
                return n.value
        return KeyError

    def ComputeHeight(self) -> int:
        return self.Octave * 12 + self.GetNoteId()

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

    def GetStaffPositionAsLetter(self) -> str:
        # A sharp is considered as a higher staff position
        # we only used sharps, it's important to know this for right now
        if len(self.Name) == 1:
            return self.Name[:1]
        else:
            temp = self.Name[:1]
            for k, val in enumerate(ALL_STAFF_POSITIONS):
                if temp == val:
                    k += 1
                    break
            if k >= len(ALL_STAFF_POSITIONS):
                k -= len(ALL_STAFF_POSITIONS)

            return ALL_STAFF_POSITIONS[k]

    def GetStaffPositionAsInteger(self) -> int:
        # A sharp is considered as a higher staff position
        staffPosAsLetter = self.GetStaffPositionAsLetter()
        for k, val in enumerate(ALL_STAFF_POSITIONS):
            if val == staffPosAsLetter:
                return k
        return KeyError

    # This is order dependent. Self should be the root note of the chord
    def GetIntervalNumber(self, other) -> int:
        if self.__class__ is other.__class__:
            staff1 = self.GetStaffPositionAsLetter()
            staff2 = other.GetStaffPositionAsLetter()

            outValue = (
                StaffPositions[staff2].value - StaffPositions[staff1].value
            )

            if outValue < 0:
                outValue += len(StaffPositions)

            # lowest note is root of chord and therefore the base for interval calculation
            # Incrementing by one so that it makes sense (a A - B chord is a second, but this return 1)
            outValue += 1

            # adding exception for octave
            if staff1 == staff2:  # and self.Octave != other.Octave:
                # issue with sharp so need another check
                # (A5 and Gs5 would give interval 1 while it should be 8)
                # simple: check height. If different, it's an octave
                if self != other:
                    outValue = 8
                # still another error crept up if base note is A6 and other Gs5
                # was returning octave instead of second. This should fix it?
                # Actually not supposed to happen since this function is order dependent with root note as base object
                # should just perform a height check at start of function and throw error
                # so follow up here is unneeded?
                if abs(self.ComputeTonalDistance(other)) < 2:
                    outValue = 2

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

    @staticmethod
    def GetNoteNameFromNamesEnum(idNote: int) -> str:
        for n in NoteNames:
            if n.value == idNote:
                return n.name
        return KeyError


def CreateNoteFromHeight(height: int) -> Note:
    octave = height // 12
    name = Note.GetNoteNameFromNamesEnum(height - octave * 12)

    return Note(Name=name, Octave=octave)
