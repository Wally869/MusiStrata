from __future__ import annotations

"""
Dataclasses to represent song components


"""

from dataclasses import dataclass, field

from .Notes import *

from copy import deepcopy


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

    # Adding an __add__ overload to allow concatenating bars in a simple way
    # this is to make easier to generate sections and then appending them
    def __add__(self, other: Track) -> Track:
        if self.__class__ is other.__class__:
            outTrack = deepcopy(self)
            outTrack.Bars = outTrack.Bars + other.Bars
            return outTrack
        else:
            return NotImplemented


"""
@dataclass
class SongSegment:
    ScaleSegment: ScaleSpecs = ScaleSpecs()
    Bars: list = field(default_factory=list)
"""


@dataclass
class TimeSignature:
    BeatsPerBar: int = 4
    BeatUnit: int = 4

    def __str__(self):
        return "TimeSignature(BeatsPerBar={}, BeatUnit={})".format(self.BeatsPerBar, self.BeatUnit)

    def __repr__(self):
        return self.__str__()


@dataclass
class Song:
    Tempo: int = 80
    BeatsPerBar: int = 4
    Tracks: list = field(default_factory=list)

    def __str__(self):
        return "Song(Tempo={}, BeatsPerBar={}, {} Tracks)".format(self.Tempo, self.BeatsPerBar, len(self.Tracks))


# Structure Creators
def GenerateBarFromRhythmicPreset(rhythmicPreset: List[Dict[str, Union[float, int]]]) -> Bar:
    """
    :param rhythmicPreset: {
        "Beat": float,
        "Duration": float,
        "NoteName": str (facultative),
        "Octave": int (facultative)
    }
    :return: Bar
    """
    outBar = Bar()
    for rp in rhythmicPreset:
        newEvent = SoundEvent(
            Beat=rp["Beat"],
            Duration=rp["Duration"]
        )

        rpKeys = list(rp.keys())
        if "NoteName" in rpKeys and "Octave" in rpKeys:
            newEvent.Note = Note(
                Name=rp["NoteName"],
                Octave=rp["Octave"]
            )
        outBar.SoundEvents.append(newEvent)

    return outBar
