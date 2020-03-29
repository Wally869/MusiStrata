from .Notes import NoteNames, Note, ALL_NOTES

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


class ScaleModes(Enum):
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
        return "ScaleSpecs({})".format(self.RefNote + "-" + self.Type)

    def __repr__(self):
        return str(self)

    def GetScaleNotes(self, referenceOctave: int = 5) -> List[Note]:
        return self.GetScaleNotesFromMode(referenceOctave=referenceOctave, mode="Ionian")

    def GetScaleNotesFromMode(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
        # Get tone succession for the scale type
        tonesSuccession = TONES_SUCCESSION[self.Type]

        # Reorganize tones_succession according to ScaleModes value (in different mode, tones_succession changes)
        tonesSuccession = tonesSuccession[ScaleModes[mode].value:] + tonesSuccession[:ScaleModes[mode].value]

        # Create the reference note for the scale wanted and get notes
        scaleNotes = [
            Note(
                Name=self.RefNote,
                Octave=referenceOctave
            )
        ]
        for toneDelta in tonesSuccession:
            scaleNotes.append(
                scaleNotes[-1] + int(toneDelta * 2)
            )

        return scaleNotes

    def GetScaleNotesNames(self) -> List[str]:
        return [n.Name for n in self.GetScaleNotes()]

    def GetScaleNotesNamesFromMode(self, mode: str = "Ionian") -> List[str]:
        return [n.Name for n in self.GetScaleNotesFromMode(mode)]

