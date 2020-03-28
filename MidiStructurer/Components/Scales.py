from Notes import NoteNames, Note, ALL_NOTES

from utils import OrderedEnum

from typing import List
from enum import Enum

TONES_SUCCESSION = {
    "Major": [
        1, 1, 0.5, 1, 1, 1, 0.5
    ],
    "Minor": [
        1, 0.5, 1, 1, 0.5, 1, 1
    ],
    "MinorMelodic": [
        1, 0.5, 1, 1, 0.5, 1.5, 0.5
    ]
}


class ScaleTypes(Enum):
    Major = 0
    Minor = 1
    MinorMelodic = 2


class ScaleModes(OrderedEnum):
    Ionian = 0
    Dorian = 1
    Phrygian = 2
    Lydian = 3
    Mixolydian = 4
    Aeolian = 5
    Locrian = 6


class ScaleSpecs(object):
    def __init__(self, refNote: str = "A", type: str = "Major"):
        self.RefNote = refNote
        self.Type = type

    def __str__(self):
        return "ScaleSpecs({})".format(self.RefNote + self.Type)

    def __repr__(self):
        return str(self)

    def GetScaleNotes(self, referenceOctave: int = 5):
        return self.GetScaleNotesFromMode(referenceOctave=referenceOctave, mode="Ionian")

    def GetScaleNotesFromMode(self, referenceOctave: int = 5, mode: str = "Ionian"):
        # Get tone succession for the scale type
        tonesSuccession = TONES_SUCCESSION[self.Type]

        # Reorganize tones_succession according to ScaleModes value (in different mode, tones_succession changes)
        tonesSuccession = tonesSuccession[ScaleModes[mode].value:] + tonesSuccession[:ScaleModes[mode].value]

        # Create the reference note for the Ioanian mode of the scale wanted and get notes
        scaleNotes = [
            Note(
                name=self.RefNote,
                octave=referenceOctave
            )
        ]
        for toneDelta in tonesSuccession:
            scaleNotes.append(
                scaleNotes[-1] + int(toneDelta * 2)
            )

        return scaleNotes

    def GetScaleNotesName(self) -> List[str]:
        return [n.name in self.GetScaleNotes()]

    def GetScaleNotesNameFromMode(self, mode: str = "Ionian"):
        return [n.name in self.GetScaleNotesFromMode(mode)]

