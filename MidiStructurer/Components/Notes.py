from enum import Enum
from utils import OrderedEnum

ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]


# Values give the distance between notes in term of halftones
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


class Note(object):
    def __init__(self, name: str = "A", octave: int = 5):
        self.Name = name
        self.Octave = octave

    def __str__(self):
        return "Note({})".format(self.Name + str(self.Octave))

    def __repr__(self):
        return str(self)

    def __add__(self, other: int):
        if type(other) != int:
            return NotImplemented
        else:
            currNoteId = self.GetNoteId() + other
            deltaOctave = 0
            while currNoteId >= len(NoteNames):
                deltaOctave += 1
                currNoteId -= len(NoteNames)

            return Note(
                name=NoteNames[
                    self.GetNoteNameFromNamesEnum(currNoteId)
                ].name,
                octave=self.Octave + deltaOctave
            )

    def __sub__(self, other: int):
        if type(other) != int:
            return NotImplemented
        else:
            currNoteId = self.GetNoteId() - other
            deltaOctave = 0
            while currNoteId <= 0:
                deltaOctave -= 1
                currNoteId += len(NoteNames)

            return Note(
                name=NoteNames[
                    self.GetNoteNameFromNamesEnum(currNoteId)
                ].name,
                octave=self.Octave + deltaOctave
            )

    def GetNoteId(self) -> int:
        for n in NoteNames:
            if n.name == self.Name:
                return n.value
        return KeyError

    def GetNoteNameFromNamesEnum(self, idNote: int) -> str:
        for n in NoteNames:
            if n.value == idNote:
                return n.name
        return KeyError

    def ComputeHeight(self) -> int:
        return self.Octave * 12 + self.GetNoteId()

    # Return distance between this note and another in term of semitones
    def ComputeTonalDistance(self, otherNote) -> int:
        return self.ComputeHeight() - otherNote.ComputeHeight()
