from typing import List, Optional
from typing_extensions import Self

from Components.Notes import Note
from Components.Intervals import Interval

from rustshed import Result, Ok, Err


class Chord:
    """
        Chord class. Resolve from components instead of tracking Intervals, allows to handle sus4 modifier
    """
    component_codes: List[str]
    intervals: List[Interval]

    def __init__(self, chord_code: str) -> None:
        from MusiStrata.Data.Chords import CHORDS_DESCRIPTIONS
        self.intervals = [
            Interval.from_code(code)
            for code in CHORDS_DESCRIPTIONS[chord_code].Intervals
        ]

    def __str__(self) -> str:
        return "Chord({})".format(self.intervals)
            
    def __repr__(self) -> str:
        return self.__str__()

    def add_interval_from_code(self, interval_code: str) -> None:
        self.component_codes.append(
            interval_code
        )

    def add_interval(self, interval: Interval) -> None:
        self.component_codes.append(
            interval.to_code()
        )

    @classmethod
    def from_interval_codes(cls, interval_codes: List[str]) -> Self:
        ch = Chord.__new__(Chord)
        ch.intervals = [Interval.from_code(code) for code in interval_codes]
        return ch
    
    @classmethod
    def from_intervals(cls, intervals: List[Interval]) -> Self:
        ch = Chord.__new__(Chord)
        ch.intervals = intervals
        return ch

    def resolve(self) -> Result[List[Interval], str]:
        intervals = []
        return Ok(intervals)

    def generate_notes(self, base_note: Note) -> List[Note]: #Result[List[Note], str]:
        return [
            base_note + interval for interval in self.intervals
        ]
    
    def get_notes(self, base_note: Note, inversion: int = 0) -> List[Note]:
        notes = [
            base_note + interval for interval in self.intervals
        ]
        for _ in range(inversion):
            notes = notes[1:] + [notes[0] + 12]
        return notes

    def __call__(self, base_note: Note, inversion: int = 0) -> List[Note]:
        return self.get_notes(base_note, inversion)

    
