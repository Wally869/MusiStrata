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

        # In modern theory, I actually need to switch the reference note for mode?
        refNote = Note(
            Name=self.RefNote,
            Octave=referenceOctave
        )

        """
        # Getting the mode ref note
        for toneDelta in tonesSuccession[:ScaleModes[mode].value]:
            refNote = refNote + int(toneDelta * 2)
        """

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
    def FindNeighbouringScales(self) -> List:
        return self.FindSameTypeNeighbours() + [self.FindDifferentTypeNeighbour()]

    def FindSameTypeNeighbours(self) -> List:
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

    def FindDifferentTypeNeighbour(self):
        if self.Type == "Major":
            return self.FindMinorFromMajorByRefNote(self.RefNote)
        else:
            return self.FindMajorFromMinorByRefNote(self.RefNote)

    @staticmethod
    def FindMinorFromMajorByRefNote(refNote: str):
        return ScaleSpecs(
            RefNote=MINOR_FROM_MAJOR[refNote],
            ScaleType="Minor"
        )

    @staticmethod
    def FindMajorFromMinorByRefNote(refNote: str):
        keys = list(MINOR_FROM_MAJOR.keys())
        for k in keys:
            if (MINOR_FROM_MAJOR[k] == refNote):
                return ScaleSpecs(RefNote=k, ScaleType="Major")
        return KeyError

    def GetPentatonicScaleNotesFromMode(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
        # pretty much same as GetScaleNotes
        tonesSuccession = TONES_SUCCESSION[self.Type]
        tonesSuccession = tonesSuccession[ScaleModes[mode].value:] + tonesSuccession[:ScaleModes[mode].value]

        # Create the reference note for the scale wanted and get notes
        scaleNotes = [
            Note(
                Name=self.RefNote,
                Octave=referenceOctave
            )
        ]

        for toneDelta in tonesSuccession:
            currNote = scaleNotes[-1] + int(toneDelta * 2)
            # Only add notes where the delta is 1
            if toneDelta == 1:
                scaleNotes.append(
                    currNote
                )

        return currNote

    def GetPentatonicScaleNotes(self, referenceOctave: int = 5):
        return GetPentatonicScaleNotesFromMode(
            referenceOctave=referenceOctave,
            mode="Ionian"
        )
