

"""
Dataclasses to represent song components


"""

from dataclasses import dataclass, field

from .Notes import *

from copy import deepcopy


@dataclass
class SoundEvent:
    Beat = 0.0
    Duration = 1.0
    Note = Note()
    Velocity = 60


def GenerateSoundEventsFromListNotes(beat, duration, notes):
    return [
        SoundEvent(
            Beat=beat,
            Duration=duration,
            Note=note
        ) for note in notes
    ]


@dataclass
class Bar:
    SoundEvents = field(default_factory=list)

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


@dataclass
class Track:
    Name = "Untitled"
    Instrument = ""
    Bars = field(default_factory=list)
    IsDrumsTrack = False
    BankUsed = 0

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
    def __add__(self, other):
        if self.__class__ is other.__class__:
            outTrack = deepcopy(self)
            outTrack.Bars = outTrack.Bars + other.Bars
            return outTrack
        else:
            return NotImplemented


"""
@dataclass
class SongSegment:
    ScaleSegment = ScaleSpecs()
    Bars = field(default_factory=list)
"""


# Do I really need a timesignature? For my implementation, beats per bar is enough?
@dataclass
class TimeSignature:
    BeatsPerBar = 4
    BeatUnit = 4

    def __str__(self):
        return "TimeSignature(BeatsPerBar={}, BeatUnit={})".format(self.BeatsPerBar, self.BeatUnit)

    def __repr__(self):
        return self.__str__()


@dataclass
class Song:
    Tempo = 80
    BeatsPerBar = 4
    Tracks = field(default_factory=list)

    def __str__(self):
        return "Song(Tempo={}, BeatsPerBar={}, {} Tracks)".format(self.Tempo, self.BeatsPerBar, len(self.Tracks))


# Structure Creators
def GenerateBarFromRhythmicPreset(rhythmicPreset):
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
