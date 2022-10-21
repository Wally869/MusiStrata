from __future__ import annotations
from typing import List, Tuple, Dict, Union

from Components.Scales import Scale
from Data.Chords import CHORDS_DESCRIPTIONS, ChordDescription

from .Notes import *
from .Intervals import *

from MusiStrata.Enums import ChordBase, ChordExtension, IntervalQuality

"""
    https://musiccrashcourses.com/lessons/intervals_maj_min.html#:~:text=Intervals%20in%20Major%20Scales,to%20the%20scale%20degree%20numbers.
"""

class Chord(object):
    def __init__(self, chord_intervals: List[Interval]):
        self.Intervals = chord_intervals
        # rewrite to get all these parameters out, and into the library fields?
        self.Size = len(chord_intervals) + 1

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
        base = ChordBase.SafeFromStr(base)
        for elem in base.value:
            intervals.append(Interval(*elem))
        for extension in extensions:
            extension = ChordExtension.SafeFromStr(extension)
            intervals.append(Interval(*extension.value))
        return Chord(intervals)

    @classmethod
    def FromIntervals(cls, root_note: Note, intervals: List[Interval]) -> List[Note]:
        chord = [root_note]
        return chord + [(root_note + interval)[0] for interval in intervals]

    @classmethod
    def FromScaleTones(cls, tones: List[int], octave: int, scale: Scale, mode: str = "Ionian") -> List[Note]:
        return [scale.GetNote(tone, octave, mode) for tone in tones]

    @classmethod
    def FromChordDescription(cls, root_note: Note, chord_description: Union[str, ChordDescription]) -> List[Note]:
        if chord_description.__class__ is str:
            return cls.FromChordDescription(CHORDS_DESCRIPTIONS[chord_description])
        else:
            return [root_note + interval for interval in chord_description.TonalIntervals]

    def CheckValidFromNote(self, root_note: Note) -> bool:
        _, errors = self(root_note)
        for err in errors:
            if err is not None:
                return False
        return True

    # change __call__ to generating alternate chord, and add __radd__ with note?
    # just create new methods for now
    def __call__(
        self, root_note: Note, indices: List[Tuple(int, int)] = None
    ) -> Tuple[List[Note], List[ValueError]]:
        """
        Get notes composing Chord, starting from rootNote and returns those specified by indices.
        Indices works by specifying 2 values: the index in the chord, and the octave shift compared to the base note.
        Octave shift can be negative.
        """
        if type(root_note) != Note:
            raise TypeError("Input must be of type Note.")
        if indices is None:
            indices = [(i, 0) for i in range(len(self.Intervals))]
        chord_notes = []
        errors = []
        chord_notes, errors = root_note + self
        out_notes = []
        out_errors = []
        for elem in indices:
            out_notes.append(chord_notes[elem[0]] + elem[1] * 12)
            out_errors.append(errors[elem[0]])
        return out_notes, errors

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
        self, root_note: Note, indices: List[Tuple(int, int)]
    ) -> Tuple[List[Note], List[ValueError]]:
        """
        Wrapping __call__ in another function to call it in Transcrypt. 
        """
        return self.__call__(root_note, indices)

    def add(self, other) -> Tuple[List[Note], List[ValueError]]:
        """
        Wrapping __radd__ in another function to call it in Transcrypt.
        """
        return self.__radd__(other)

