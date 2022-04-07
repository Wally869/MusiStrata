from __future__ import annotations
from typing import List, Tuple, Dict, Union

from .Notes import *
from .Intervals import *

from MusiStrata.Enums import ChordBase, ChordExtension, IntervalQuality

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
                    list(filter(lambda consoType: consoType == field, consonancesTypes))
                )
            )

        (
            self.NbPerfectConsonances,
            self.NbImperfectConsonances,
            self.NbDissonances,
        ) = tempSumTypes

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

    @classmethod
    def FromBaseExtensions(
        cls, base: ChordBase, extensions: List[ChordExtension] = []
    ) -> Chord:
        intervals = []
        if type(base) == str:
            base = ChordBase.FromStr(base)
        for elem in base.value:
            intervals.append(Interval(*elem))
        for extension in extensions:
            if extension is None:
                continue
            if type(extension) == str:
                extension = ChordExtension.FromStr(extension)
            intervals.append(Interval(*extension.value))
        return Chord(intervals)

    def CheckValidFromNote(self, rootNote: Note) -> bool:
        _, errors = self(rootNote)
        for err in errors:
            if err is not None:
                return False
        return True

    # change __call__ to generating alternate chord, and add __radd__ with note?
    # just create new methods for now
    def __call__(
        self, rootNote: Note, indices: List[Tuple(int, int)] = None
    ) -> Tuple[List[Note], List[ValueError]]:
        """
        Get notes composing Chord, starting from rootNote and returns those specified by indices.
        Indices works by specifying 2 values: the index in the chord, and the octave shift compared to the base note.
        Octave shift can be negative.
        """
        if type(rootNote) != Note:
            raise TypeError("Input must be of type Note.")
        if indices is None:
            indices = [(i, 0) for i in range(len(self.Intervals))]
        chordNotes = []
        errors = []
        chordNotes, errors = rootNote + self
        outNotes = []
        outErrors = []
        for elem in indices:
            outNotes.append(chordNotes[elem[0]] + elem[1] * 12)
            outErrors.append(errors[elem[0]])
        return outNotes, errors

    def __radd__(self, other) -> Tuple[List[Note], List[ValueError]]:
        if type(other) == Note:
            outNotes = []
            errors = []
            for interval in self.Intervals:
                currNote, err = other + interval
                outNotes.append(currNote)
                errors.append(err)
            return outNotes, errors
        elif type(other) == Interval:
            return Interval(Intervals=[self, other])
        raise NotImplementedError()

    def call(
        self, rootNote: Note, indices: List[Tuple(int, int)]
    ) -> Tuple[List[Note], List[ValueError]]:
        """
        Wrapping __call__ in another function to call it in Transcrypt.
        """
        return self.__call__(rootNote, indices)

    def add(self, other) -> Tuple[List[Note], List[ValueError]]:
        """
        Wrapping __radd__ in another function to call it in Transcrypt.
        """
        if type(other) == Note:
            outNotes = []
            errors = []
            for interval in self.Intervals:
                currNote, err = interval.add(other)
                outNotes.append(currNote)
                errors.append(err)
            return outNotes, errors
        elif type(other) == Interval:
            return Interval(Intervals=[self, other])
        raise NotImplementedError()
