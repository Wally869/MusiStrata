"""
Dataclasses to represent song components


"""


from dataclasses import dataclass, field

from Notes import *

@dataclass
class SoundEvent:
    Beat: float = 0.0
    Duration: float = 0.0
    Note: Note = Note()


@dataclass
class Bar:
    Notes: list = field(default_factory=list)


@dataclass
class Track:
    Name: str = "Untitled"
    Instrument: str = ""
    Bars: list = field(default_factory=list)
    Velocity: int = 60
    IsDrumsTrack: bool = False

    def __str__(self):
        if self.IsDrumTrack:
            outStr =  "Drum Track - "
        else:
            outStr = "Track - "

        return outStr + self.Name + " - " + self.Instrument


@dataclass
class SongSegment:
    ScaleSegment: Scale = Scale()
    Bars: list = field(default_factory=list)


@dataclass
class Song:
    Tempo: int = 80
    BeatsPerBar: int = 4
    Tracks: list = field(default_factory=list)


