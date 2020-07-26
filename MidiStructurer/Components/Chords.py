from __future__ import annotations
from typing import List, Tuple, Dict, Union

from .Notes import *
from .Intervals import *

from ..PrimitiveClassesUtils import *


# Using good old wikipedia as starting point
# https://en.wikipedia.org/wiki/Chord_(music)


# How do I define a chord? How many intervals it has, how many dissonants, how many consonants
class Chord(object):
    def __init__(self, chordIntervals: List[Interval]):
        self.Intervals = chordIntervals

        # rewrite to get all these parameters out, and into the library fields?
        self.Size = len(chordIntervals) + 1

        consonancesTypes = [interval.GetConsonanceType() for interval in chordIntervals]
        tempSumTypes = []
        for field in ["PerfectConsonance", "ImperfectConsonance", "Dissonance"]:
            tempSumTypes.append(
                len(
                    list(
                        filter(
                            lambda consoType: consoType == field,
                            consonancesTypes
                        )
                    )
                )
            )

        self.NbPerfectConsonances, self.NbImperfectConsonances, self.NbDissonances = tempSumTypes

    def __str__(self):
        outStr = "Chord("
        for k, val in enumerate(self.Intervals):
            outStr += val.ShortStr()
            if k != len(self.Intervals) - 1:
                outStr += "-"
        outStr += ")"
        return outStr

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.Intervals)

    def InvertIntervals(self, inversion: int = 0):
        inverted = self.Intervals
        for _ in range(inversion):
            inverted = inverted[1:] + [Interval(Intervals=[Interval(8, "Perfect"), inverted[0]])]
        return inverted

    # change __call__ to generating alternate chord, and add __radd__ with note?
    # just create new methods for now
    def __call__(self, rootNote: Note, inversion: int = 0, fromRoot: bool = True) -> Tuple[List[Note], List[Error]]:
        if type(rootNote) != Note:
            raise TypeError("Input must be of type Note.")
        currIntervals = self.InvertIntervals(inversion)
        outNotes = []
        errors = []
        for interval in currIntervals:
            if fromRoot:
                currNote, err = rootNote + interval
            else:
                currNote, err = rootNote + interval
                if len(outNotes) > 0:
                    currNote, err = outNotes[-1] + interval
            outNotes.append(currNote)
            errors.append(err)
        return outNotes, errors

    def Invert(self, inversions: int = 1):
        invertedIntervals = self.InvertIntervals(inversions)
        return Chord(invertedIntervals)

    def __radd__(self, other):
        if type(other) == Note:
            outNotes = []
            errors = []
            for interval in self.Intervals:
                currNote, err = other + interval
                outNotes.append(currNote)
                errors.append(err)
            return outNotes, errors
        raise NotImplementedError()


# using this, and a different approach I guess
# actually this nice: https://en.wikibooks.org/wiki/Music_Theory/Complete_List_of_Chord_Patterns
CHORD_TYPES = [
    "Major", "Minor", "Diminished", "MajorSeventh", "MinorSeventh", "DominantSeventh",
    "Suspended", "Augmented", "Extended"
]

RAW_CHORDS = []

MAJOR_CHORDS = [
    {
        "Name": "Major Triad",
        "Type": "Major",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Perfect")]
    },
    {
        "Name": "Major Seventh",
        "Type": "Major",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Perfect"), Interval(7, "Major")]
    }
]

DOMINANT_CHORDS = [
    {
        "Name": "Dominant Seventh",
        "Type": "Dominant",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Perfect"), Interval(7, "Minor")]
    }
]

MINOR_CHORDS = [
    {
        "Name": "Minor Triad",
        "Type": "Minor",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Perfect")]
    },
    {
        "Name": "Minor Seventh",
        "Type": "Minor",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Perfect"), Interval(7, "Major")]
    }
]

DIMINISHED_CHORDS = [
    {
        "Name": "Diminished Triad",
        "Type": "Diminished",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Diminished")]
    },
    {
        "Name": "Diminished Seventh",
        "Type": "Diminished",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Diminished"),
                      Interval(7, "Diminished")]
    }
]

AUGMENTED_CHORDS = [
    {
        "Name": "Augmented Triad",
        "Type": "Augmented",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Augmented")]
    },
    {
        "Name": "Augmented Seventh",
        "Type": "Augmented",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Augmented"), Interval(7, "Augmented")]
    }
]

RAW_CHORDS = MAJOR_CHORDS + MINOR_CHORDS + DOMINANT_CHORDS + DIMINISHED_CHORDS + AUGMENTED_CHORDS

for c in RAW_CHORDS:
    c["Chord"] = Chord(c["Intervals"])
    del c["Intervals"]


class ChordsLibraryClass(Library):
    BaseName: str = "ChordsLibrary"
    Records: List[Record] = None

    def GetChordsFromType(self, typeValue: str):
        records = self.GetFromValueInField("Type", typeValue)
        return [r.Chord for r in records]

    def GetChordsFromAttribute(self, attributeValue: str):
        records = self.GetFromValueInField("Attribute", attributeValue)
        return [r.Chord for r in records]

    def GetChordFromName(self, nameChord: str):
        record = self.GetFromValueInField("Name", nameChord)
        return record[0].Chord


ChordsLibrary = ChordsLibraryClass(RAW_CHORDS)
