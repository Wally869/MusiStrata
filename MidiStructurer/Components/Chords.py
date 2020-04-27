from __future__ import annotations

from .Notes import *
from .Intervals import *

# Using good old wikipedia as starting point
# https://en.wikipedia.org/wiki/Chord_(music)


dychordsIntervals = [
    [interval] for interval in list(
        filter(
            lambda x: x.TonalDistance > 0, ALL_INTERVALS
        )
    )
]

trichordsIntervals = []
for interval0 in ALL_INTERVALS:
    for interval1 in ALL_INTERVALS:
        if interval1 > interval0:
            trichordsIntervals.append(
                [interval0, interval1]
            )

quadchordsIntervals = []
for interval0 in ALL_INTERVALS:
    for interval1 in ALL_INTERVALS:
        for interval2 in ALL_INTERVALS:
            if interval0 < interval1 < interval2:
                quadchordsIntervals.append(
                    [interval0, interval1, interval2]
                )


# How do I define a chord? How many intervals it has, how many dissonants, how many consonants
# how many disturbed... lotsa params I guess
class Chord(object):
    def __init__(self, chordIntervals: List[Interval]):
        self.Intervals = chordIntervals
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

    def GenerateFromRootNote(self, rootNote: Note, rootInOutput: bool = True) -> Tuple[List[Note], List[Error]]:
        if type(rootNote) != Note:
            raise TypeError("Input must be of type Note.")
        outNotes = []
        if rootInOutput:
            outNotes.append(rootNote)
        errors = []
        for interval in self.Intervals:
            currNote, err = rootNote + interval
            outNotes.append(currNote)
            errors.append(err)
        return outNotes, errors

    def GenerateConsecutively(self, rootNote: Note, rootInOutput: bool = True) -> Tuple[List[Note], List[Error]]:
        if type(rootNote) != Note:
            raise TypeError("Input must be of type Note.")
        outNotes = []
        if rootInOutput:
            outNotes.append(rootNote)
        errors = []
        currNote = rootNote
        for interval in self.Intervals:
            currNote, err = currNote + interval
            outNotes.append(currNote)
            errors.append(err)
        return outNotes, errors

    def __call__(self, rootNote: Note, fromRoot: bool = True, rootInOutput: bool = True, excludeErrors: bool = False):
        if fromRoot:
            notes, err = self.GenerateFromRootNote(rootNote, rootInOutput)
        else:
            notes, err = self.GenerateConsecutively(rootNote, rootInOutput)
        if excludeErrors:
            return notes
        return notes, err


# I'd like to avoid loading all chords are runtime, but I think list does not work with global?
# so using class emulating list
class ChordsList(object):
    def __init__(self):
        self.Chords = []

    def __repr__(self):
        return self.Chords.__repr__()

    def __len__(self):
        return len(self.Chords)

    def __getitem__(self, item):
        return self.Chords[item]


ALL_CHORDS = ChordsList()


# Use this function to load all chords from defined at start of file
def LoadAllChords():
    global ALL_CHORDS
    ALL_CHORDS.Chords = [
        Chord(intervals)
        for intervals
        in dychordsIntervals + trichordsIntervals + quadchordsIntervals
    ]


LoadAllChords()
