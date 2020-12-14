from __future__ import annotations
from typing import List, Tuple, Dict, Union

from .Notes import NoteNames, Note, ALL_NOTES

from .Chords import MINOR_TRIAD, MAJOR_TRIAD, DIMINISHED_TRIAD, MINOR_SEVENTH, MAJOR_SEVENTH, DIMINISHED_SEVENTH

# from .utils import ExtendedEnum
from .EnumManager import EnumManager_Ordered

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

ALL_SCALE_MODES = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]


class ScaleModes(EnumManager_Ordered):
    KeyValuesMap = {ALL_SCALE_MODES[i]: i for i in range(len(ALL_SCALE_MODES))}
    KeyList = ALL_SCALE_MODES
    ValuesList = [i for i in range(len(ALL_SCALE_MODES))]


class ScaleSpecs(object):
    def __init__(self, RefNote: str = "A", ScaleType: str = "Major"):
        self.RefNote = RefNote
        if (type(ScaleType) != str):
            raise TypeError("In ScaleSpecs constructor: ScaleType argument must be a string")
        self.Type = ScaleType

    def __str__(self):
        return "ScaleSpecs({})".format(self.RefNote + "-" + self.Type)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        else:
            if self.RefNote == other.RefNote and self.Type == other.Type:
                return True
            else:
                return False
    
    def GetScaleNotes(self, referenceOctave: int = 5, mode: str = "Ionian") -> List[Note]:
        # Get tone succession for the scale type
        tonesSuccession = TONES_SUCCESSION[self.Type]

        refNote = Note(
            Name=self.RefNote,
            Octave=referenceOctave
        )

        # Reorganize tones_succession according to ScaleModes value (in different mode, tones_succession changes)
        tonesSuccession = tonesSuccession[ScaleModes(mode).value:] + tonesSuccession[:ScaleModes(mode).value]

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
    def GetNeighbouringScales(self) -> List[ScaleSpecs]:
        return self.GetSameTypeNeighbours() + [self.GetDifferentTypeNeighbour()]

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

    def GetDifferentTypeNeighbour(self) -> ScaleSpecs:
        if self.Type == "Major":
            return self.GetMinorFromMajorByRefNote(self.RefNote)
        else:
            return self.GetMajorFromMinorByRefNote(self.RefNote)

    @staticmethod
    def GetMinorFromMajorByRefNote(refNote: str) -> ScaleSpecs:
        return ScaleSpecs(
            RefNote=MINOR_FROM_MAJOR[refNote],
            ScaleType="Minor"
        )

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

    def GetScaleChordsProgression(self, mode="Ionian"):
        progression = [
            MAJOR_TRIAD, MINOR_TRIAD, MINOR_TRIAD, MAJOR_TRIAD, MAJOR_TRIAD, MINOR_TRIAD, DIMINISHED_TRIAD
        ]
        if self.Type == "Minor":
            progression = [
                MINOR_TRIAD, MINOR_SEVENTH, MAJOR_TRIAD, MINOR_TRIAD, MINOR_TRIAD, MAJOR_TRIAD, MAJOR_TRIAD
            ]
        return progression[ScaleModes(mode).value:] + progression[:ScaleModes(mode).value]
    
    def GetScaleChordsNotes(self, referenceOctave: int = 5, mode="Ionian"):
        chords = self.GetScaleChordsProgression(mode=mode)
        notes = self.GetScaleNotes(referenceOctave=referenceOctave, mode=mode)
        output = []
        for idElem in range(len(chords)):
            temp, _ = chords[idElem](notes[idElem])
            output.append(temp)
        return output


def ExtendScaleNotes(scaleNotes: List[Note], extensionFactor: Union[int, float],
                     singleDirection: bool = False, direction: str = "+") -> List[Note]:
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
    scaleNotes = sorted(scaleNotes, key=lambda x: x.Height)

    directions = ["+", "-"]
    # Get number of elements
    if singleDirection:
        directions = [direction]

    outScaleNotes = [n for n in scaleNotes]
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
    outScaleNotes = sorted(outScaleNotes, key=lambda x: x.Height)
    return FilterOutRepeatedNotes(outScaleNotes)


def FilterOutRepeatedNotes(notes: List[Note]) -> List[Note]:
    return list(set(notes))
