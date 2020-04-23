from __future__ import annotations

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

# not using flats coz of implementation restrictions
MAJOR_NEIGHBOURS = {
    "C": ["F", "G"],
    "G": ["C", "D"],
    "D": ["G", "A"],
    "A": ["D", "E"],
    "E": ["A", "B"],
    "B": ["E", "Fs"],
    "Fs": ["B", "Cs"],
    "Cs": ["Fs", "Gs"],
    "Gs": ["Cs", "Ds"],
    "Ds": ["Gs", "As"],
    "As": ["Ds", "F"],
    "F": ["As", "C"]
}

# Minors have same neighbours as majors
MINOR_NEIGHBOURS = MAJOR_NEIGHBOURS

MINOR_FROM_MAJOR = {
    "C": "A",
    "G": "E",
    "D": "B",
    "A": "Fs",
    "E": "Cs",
    "B": "Gs",
    "Fs": "Ds",
    "Cs": "As",
    "Gs": "F",
    "Ds": "C",
    "As": "G",
    "F": "D"
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
    def __init__(self, RefNote: str = "A", ScaleType: str = "Major"):
        self.RefNote = RefNote
        self.Type = ScaleType

    def __str__(self):
        return "ScaleSpecs({})".format(self.RefNote + "-" + self.Type)

    def __repr__(self):
        return str(self)

    def GetScaleNotes(self, referenceOctave: int = 5) -> List[Note]:
        return self.GetScaleNotesFromMode(referenceOctave=referenceOctave, mode="Ionian")

    def GetScaleNotesFromMode(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
        # Get tone succession for the scale type
        tonesSuccession = TONES_SUCCESSION[self.Type]

        refNote = Note(
            Name=self.RefNote,
            Octave=referenceOctave
        )

        # Reorganize tones_succession according to ScaleModes value (in different mode, tones_succession changes)
        tonesSuccession = tonesSuccession[ScaleModes[mode].value:] + tonesSuccession[:ScaleModes[mode].value]

        # Create the reference note for the scale wanted and get notes
        scaleNotes = [refNote]
        for toneDelta in tonesSuccession:
            scaleNotes.append(
                scaleNotes[-1] + int(toneDelta * 2)
            )

        return scaleNotes

    def GetScaleNotesNames(self) -> List[str]:
        return [n.Name for n in self.GetScaleNotes()]

    def GetScaleNotesNamesFromMode(self, mode: str = "Ionian") -> List[str]:
        return [n.Name for n in self.GetScaleNotesFromMode(mode)]

    # Implementing circle of fifths here
    def FindNeighbouringScales(self) -> List[ScaleSpecs]:
        return self.FindSameTypeNeighbours() + [self.FindDifferentTypeNeighbour()]

    def FindSameTypeNeighbours(self) -> List[ScaleSpecs]:
        # Minors and Majors have the same neighbours, but differentiating anyway
        if self.Type == "Major":
            neighboursRefNotes = MAJOR_NEIGHBOURS[self.RefNote]
        else:
            neighboursRefNotes = MINOR_NEIGHBOURS[self.RefNote]

        return [
            ScaleSpecs(
                RefNote=refNote,
                ScaleType=self.Type
            ) for refNote in neighboursRefNotes
        ]

    def FindDifferentTypeNeighbour(self) -> ScaleSpecs:
        if self.Type == "Major":
            return self.FindMinorFromMajorByRefNote(self.RefNote)
        else:
            return self.FindMajorFromMinorByRefNote(self.RefNote)

    @staticmethod
    def FindMinorFromMajorByRefNote(refNote: str) -> ScaleSpecs:
        return ScaleSpecs(
            RefNote=MINOR_FROM_MAJOR[refNote],
            ScaleType="Minor"
        )

    @staticmethod
    def FindMajorFromMinorByRefNote(refNote: str) -> ScaleSpecs:
        keys = list(MINOR_FROM_MAJOR.keys())
        for k in keys:
            if MINOR_FROM_MAJOR[k] == refNote:
                return ScaleSpecs(RefNote=k, ScaleType="Major")
        return KeyError

    def GetPentatonicScaleNotesFromMode(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
        # Make use of GetScaleNotes method
        allScaleNotes = self.GetScaleNotesFromMode(
            referenceOctave=referenceOctave,
            mode=mode
        )

        # only keep notes where there is a difference of a whole tone 
        # compared to previous in scale
        pentatonicScaleNotes = [allScaleNotes[0]]
        for idn in range(1, len(allScaleNotes)):
            if (allScaleNotes[idn] - allScaleNotes[idn - 1]) == 2:
                pentatonicScaleNotes.append(
                    allScaleNotes[idn]
                )

        # only 5 notes in pentatonic scale
        return pentatonicScaleNotes[:5]

    def GetPentatonicScaleNotes(self, referenceOctave: int = 5) -> List[Note]:
        return self.GetPentatonicScaleNotesFromMode(
            referenceOctave=referenceOctave,
            mode="Ionian"
        )
