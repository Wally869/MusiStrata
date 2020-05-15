from __future__ import annotations

from .Notes import NoteNames, Note, ALL_NOTES

from typing import List
from enum import Enum
from copy import deepcopy

from .utils import ExtendedEnum

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


class ScaleModes(ExtendedEnum):
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

    def GetScaleNotes(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
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

    def GetScaleNotesNames(self, mode: str = "Ionian") -> List[str]:
        return [n.Name for n in self.GetScaleNotes(mode=mode)]

    # Implementing circle of fifths here
    def FindNeighbouringScales(self) -> List[ScaleSpecs]:
        print("DEPRECATION WARNING - Use method starting in GET for Note methods")
        return self.GetNeighbouringScales()

    def GetNeighbouringScales(self) -> List[ScaleSpecs]:
        return self.FindSameTypeNeighbours() + [self.FindDifferentTypeNeighbour()]

    def FindSameTypeNeighbours(self) -> List[ScaleSpecs]:
        print("DEPRECATION WARNING - Use method starting in GET for Note methods")
        return self.GetSameTypeNeighbours()

    def GetSameTypeNeighbours(self) -> List[ScaleSpecs]:
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
        print("DEPRECATION WARNING - Use method starting in GET for Note methods")
        return self.GetDifferentTypeNeighbour()

    def GetDifferentTypeNeighbour(self) -> ScaleSpecs:
        if self.Type == "Major":
            return self.FindMinorFromMajorByRefNote(self.RefNote)
        else:
            return self.FindMajorFromMinorByRefNote(self.RefNote)

    @staticmethod
    def FindMinorFromMajorByRefNote(refNote: str) -> ScaleSpecs:
        print("DEPRECATION WARNING - Use method starting in GET for Note methods")
        return ScaleSpecs.GetMinorFromMajorByRefNote(refNote)

    @staticmethod
    def GetMinorFromMajorByRefNote(refNote: str) -> ScaleSpecs:
        return ScaleSpecs(
            RefNote=MINOR_FROM_MAJOR[refNote],
            ScaleType="Minor"
        )

    @staticmethod
    def FindMajorFromMinorByRefNote(refNote: str) -> ScaleSpecs:
        print("DEPRECATION WARNING - Use method starting in GET for Note methods")
        return ScaleSpecs.GetMajorFromMinorByRefNote(refNote)

    @staticmethod
    def GetMajorFromMinorByRefNote(refNote: str) -> ScaleSpecs:
        keys = list(MINOR_FROM_MAJOR.keys())
        for k in keys:
            if MINOR_FROM_MAJOR[k] == refNote:
                return ScaleSpecs(RefNote=k, ScaleType="Major")
        return KeyError

    def GetPentatonicScaleNotes(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
        # Make use of GetScaleNotes method
        allScaleNotes = self.GetScaleNotes(
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


def ExtendScaleNotes(scaleNotes: List[Note], extensionFactor: Union[int, float],
                     singleDirection: bool = False, direction: str = "+"):
    """
    Extend a list of note by a given factor by transposing them by N octaves.
    2 methods depending on type of extension factor:
        - if int, extension factor is the number of elements to be added
        - if float, extension factor is a percentage of length of scaleNotes to be added
    when passing a float, compute an int and recursively call ExtendScaleNotes
    """

    if type(extensionFactor) == float:
        intExtensionFactor = int(extensionFactor * len(scaleNotes))
        return ExtendScaleNotes(scaleNotes, intExtensionFactor, singleDirection, direction)

    # ensure scaleNotes are sorted in ascending order
    scaleNotes = sorted(scaleNotes, key=lambda x: x.ComputeHeight())

    directions = ["+", "-"]
    # Get number of elements
    if singleDirection:
        directions = [direction]

    outScaleNotes = deepcopy(scaleNotes)
    for currDirection in directions:
        addedElements = 0
        refNotes = scaleNotes
        nbOctaves = 1
        tonalDelta = 12
        if currDirection == "-":
            tonalDelta = -12
            # need to take order into account
            # if going down, pool note must be reversed
            refNotes = refNotes[::-1]

        while addedElements < extensionFactor:
            for note in refNotes:
                if addedElements > extensionFactor:
                    break
                outScaleNotes.append(note + nbOctaves * tonalDelta)
                addedElements += 1
            nbOctaves += 1

    # sort again and get rid of repeated notes
    outScaleNotes = sorted(outScaleNotes, key=lambda x: x.ComputeHeight())
    return FilterOutRepeatedNotes(outScaleNotes)


def FilterOutRepeatedNotes(notes: List[Note]):
    outNotes = []
    outNotesHeight = []
    for n in notes:
        if n.ComputeHeight() not in outNotesHeight:
            outNotes.append(n)
            outNotesHeight.append(n.ComputeHeight())
    return outNotes
