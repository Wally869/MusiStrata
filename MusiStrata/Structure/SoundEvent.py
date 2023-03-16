from typing import List, TYPE_CHECKING
from typing_extensions import Self

from dataclasses import dataclass

from MusiStrata.Components.Notes import Note

if TYPE_CHECKING:
    from .Bar import Bar
    from .Track import Track
    from .Song import Song


class SoundEvent:
    def __init__(self, beat: float = 0.0, duration: float = 1.0, note: Note = Note(), velocity: int = 60) -> None:
        self.Beat = beat
        self.Duration = duration
        self.Note = note
        self.Velocity = velocity

    def ToDict(self) -> dict:
        dictRepr = {
            "Beat": self.Beat,
            "Duration": self.Duration,
            "Note": self.Note.to_dict(),
            "Velocity": self.Velocity,
        }
        return dictRepr

    def ToJSON(self) -> str:
        from json import dumps as _dumps

        return _dumps(self.ToDict())

    @classmethod
    def FromDict(cls, dictRepr: dict):
        return SoundEvent(
            Beat=dictRepr["Beat"],
            Duration=dictRepr["Duration"],
            Note=Note.from_dict(dictRepr["Note"]),
        )

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads

        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)

    @classmethod
    def FromNotes(cls, beat: float, duration: float, notes: List[Note]) -> List[Self]:
        return [SoundEvent(beat, duration, note) for note in notes]

    def to_bar(self) -> "Bar":
        from .Bar import Bar
        return Bar([self])
    
    def to_track(self, instrument: str = "") -> "Track":
        from .Track import Track
        return Track(
            Instrument=instrument,
            Bars=[Bar(self)]
        )

    def to_song(self, tempo: int = 80, beats_per_bar: int = 4, instrument: str = "") -> "Song":
        from .Song import Song
        return Song(
            tempo,
            beats_per_bar,
            [self.to_track(instrument)]
        )
