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

    def ToDict(self) -> dict:
        dictRepr = {
            "Beat": self.Beat,
            "Duration": self.Duration,
            "Note": self.Note.ToDict(),
            "Velocity": self.Velocity
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
            Note=Note.FromDict(dictRepr["Note"])
        )

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads
        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)


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

    def ToDict(self) -> dict:
        dictRepr = {
            "SoundEvents": [se.ToDict() for se in self.SoundEvents]
        }
        return dictRepr

    def ToJSON(self) -> str:
        from json import dumps as _dumps
        return _dumps(self.ToDict())

    @classmethod
    def FromDict(cls, dictRepr: dict):
        return Bar([
            SoundEvent.FromDict(elem) for elem in dictRepr["SoundEvents"]
        ])

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads
        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)

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

    def append(self, other: Union[SoundEvent, List[SoundEvent]]):
        if type(other) == list:
            if type(other[0]) != SoundEvent:
                raise TypeError("Bar Class - The append method only accepts a SoundEvent object or a list of SoundEvent objects")
            else:
                self.SoundEvents += other
        elif type(other) == SoundEvent:
            self.SoundEvents.append(other)
        else:
            raise TypeError("Bar Class - The append method only accepts a SoundEvent object or a list of SoundEvent objects")


@dataclass
class Track:
    Name: str = "Untitled"
    Instrument: str = ""
    Bars: list = field(default_factory=list)
    IsDrumsTrack: bool = False
    BankUsed: int = 0

    def ToDict(self) -> dict:
        dictRepr = {
            "Name": self.Name,
            "Instrument": self.Instrument,
            "Bars": [b.ToDict() for b in self.Bars],
            "IsDrumsTrack": self.IsDrumsTrack,
            "BankUsed": self.BankUsed
        }
        return dictRepr

    def ToJSON(self) -> str:
        from json import dumps as _dumps
        return _dumps(self.ToDict())

    @classmethod
    def FromDict(cls, dictRepr: dict):
        return Track(
            Name=dictRepr["Name"],
            Instrument=dictRepr["Instrument"],
            Bars=[Bar.FromDict(elem) for elem in dictRepr["Bars"]],
            IsDrumsTrack=dictRepr["IsDrumsTrack"],
            BankUsed=dictRepr["BankUsed"]
        )

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads
        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)

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

    def append(self, other: Union[Bar, List[Bar]]):
        if type(other) == list:
            if type(other[0]) != Bar:
                raise TypeError("Track Class - The append method only accepts a Bar object or a list of Bar objects")
            else:
                self.Bars += other
        elif type(other) == Bar:
            self.Bars.append(other)
        else:
            raise TypeError("Track Class - The append method only accepts a Bar object or a list of Bar objects")


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

    def ToDict(self) -> dict:
        dictRepr = {
            "Tempo": self.Tempo,
            "BeatsPerBar": self.BeatsPerBar,
            "Tracks": [t.ToDict() for t in self.Tracks]
        }
        return dictRepr

    def ToJSON(self) -> str:
        from json import dumps as _dumps
        return _dumps(self.ToDict())

    @classmethod
    def FromDict(cls, dictRepr: dict):
        return Song(
            Tempo=dictRepr["Tempo"],
            BeatsPerBar=dictRepr["BeatsPerBar"],
            Tracks=[Track.FromDict(elem) for elem in dictRepr["Tracks"]],
        )

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads
        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)


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
