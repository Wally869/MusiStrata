"""
Dataclasses to represent song components


"""

from dataclasses import dataclass, field

from .Notes import *


@dataclass
class SoundEvent:
    Beat: float = 0.0
    Duration: float = 0.0
    Note: Note = Note()


@dataclass
class Bar:
    SoundEvents: list = field(default_factory=list)

    def __str__(self):
        return "Bar({} SoundEvents)".format(len(self.SoundEvents))

    def __repr__(self):
        return str(self)


@dataclass
class Track:
    Name: str = "Untitled"
    Instrument: str = ""
    Bars: list = field(default_factory=list)
    Velocity: int = 60
    IsDrumsTrack: bool = False

    def __str__(self):
        if self.IsDrumsTrack:
            outStr = "Drum Track - "
        else:
            outStr = "Track - "

        return outStr + self.Name + " - " + self.Instrument

    def __repr__(self):
        return str(self)


"""
@dataclass
class SongSegment:
    ScaleSegment: ScaleSpecs = ScaleSpecs()
    Bars: list = field(default_factory=list)
"""


@dataclass
class Song:
    Tempo: int = 80
    BeatsPerBar: int = 4
    Tracks: list = field(default_factory=list)

    def __str__(self):
        return "Song(Tempo={}, BeatsPerBar={}, {} Tracks)".format(self.Tempo, self.BeatsPerBar, len(self.Tracks))

