from __future__ import annotations
from typing import List, Tuple, Dict, Union

from dataclasses import dataclass, field

from .Notes import *


"""
Dataclasses to represent song components
"""

# TypeStripper preprocessing tag below, do not remove
#NoTypeStripping


@dataclass
class SoundEvent:
    Beat: float = 0.0
    Duration: float = 1.0
    Note: Note = Note()
    Velocity: int = 60


def GenerateSoundEventsFromListNotes(beat: float, duration: float, notes: List[Note]):
    return [
        SoundEvent(
            Beat=beat,
            Duration=duration,
            Note=note
        ) for note in notes
    ]


@dataclass
class Bar:
    SoundEvents: list = field(default_factory=list)

    def __str__(self):
        return "Bar({} SoundEvents)".format(len(self.SoundEvents))

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if self.__class__ is other.__class__:
            return Bar(
                SoundEvents=self.SoundEvents + other.SoundEvents
            )
        elif type(other) == SoundEvent:
            return Bar(
                SoundEvents=self.SoundEvents + [other]
            )
        raise NotImplementedError()

    def __radd__(self, other):
        if type(other) == SoundEvent:
            return Bar(
                SoundEvents=self.SoundEvents + [other]
            )
        raise NotImplementedError()

    def __mul__(self, other: Union[int, float]):
        # Casting to int if passing a float
        other = int(other)
        return [self] * other


@dataclass
class Track:
    Name: str = "Untitled"
    Instrument: str = ""
    Bars: list = field(default_factory=list)
    IsDrumsTrack: bool = False
    BankUsed: int = 0

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
            outTrack = self
            outTrack.Bars = outTrack.Bars + other.Bars
            return outTrack
        else:
            return NotImplemented

    def DuplicateBars(self, duplicationFactor: Union[int, float]):
        # duplicate bars and append them to the track
        # casting float to int
        self.Bars = self.Bars * duplicationFactor


"""
@dataclass
class SongSegment:
    ScaleSegment: ScaleSpecs = ScaleSpecs()
    Bars: list = field(default_factory=list)
"""


# Do I really need a timesignature? For my implementation, beats per bar is enough?
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
