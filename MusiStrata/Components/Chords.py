from __future__ import annotations
from typing import List, Tuple, Dict, Union, Optional

from .Scales import Scale
from MusiStrata.Data.Chords import CHORDS_DESCRIPTIONS, ChordDescription

from .Notes import *
from .Intervals import *

from MusiStrata.Enums import ChordBase, ChordExtension, IntervalQuality, Mode




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
    def FromNotes(cls, notes: List[Note]) -> Chord:
        """
            Extract intervals from given notes and compose a chord. 
            Notes get sorted by height.
        """
        notes = sorted(notes, key=lambda x: x.Height)
        intervals = [Interval.FromNotes(notes[0], notes[id_note]) for id_note in range(len(notes))]
        return Chord(intervals)

    @classmethod
    def FromIntervals(cls, intervals: List[Interval]) -> Chord:
        """
            Same as base __init__
        """
        return Chord(intervals)

    @classmethod
    def FromScaleTones(cls, tones: List[int], scale: Scale, mode: str = "Ionian") -> Chord: #List[Note]:
        notes = [scale.GetNote(tone, 5, mode) for tone in tones]
        intervals = [Interval.FromNotes(notes[0], notes[id_note]) for id_note in range(len(notes))]
        return Chord(intervals)

    @classmethod
    def FromStr(cls, code: str) -> Chord:
        return cls.FromChordDescription(code)

    @classmethod
    def FromChordDescription(cls, chord_description: Union[str, ChordDescription]) -> Chord: #List[Note]:
        if chord_description.__class__ is str:
            return cls.FromChordDescription(CHORDS_DESCRIPTIONS[chord_description])
        else:
            # return [root_note + interval for interval in chord_description.TonalIntervals]
            return Chord([Interval.FromIntervalDescription(interval_description) for interval_description in chord_description.Intervals])

    @classmethod
    def GetScaleChords(cls, scale: Scale, extension: str = "", mode: str = "Ionian") -> List[Chord]:
        code_major = ["M", "m", "m", "M", "M", "m", "D"]
        code_minor = ["m", "D", "M", "m", "m", "M", "M"]
        match scale.Type:
            case Mode.Major:
                return [cls.FromStr(chord_code + str(extension)) for chord_code in code_major]
            case Mode.Minor:
                return [cls.FromStr(chord_code + str(extension)) for chord_code in code_minor]
        

    def CheckValidFromNote(self, root_note: Note) -> bool:
        _, errors = self.__safecall__(root_note)
        for err in errors:
            if err is not None:
                return False
        return True

    def __safecall__(
        self, root_note: Note, indices: Optional[List[Tuple[int, int]]] = None
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

    def __call__(
        self, root_note: Note, indices: Optional[List[Tuple[int, int]]] = None
    ) -> List[Note]:
        return self.__safecall__(root_note, indices)[0]

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


