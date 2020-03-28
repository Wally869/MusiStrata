"""
Dataclasses to represent song components


"""

from dataclasses import dataclass, field

@dataclass
class Scale:
    RefNote: str = "A"
    Type: str = "Major"
    Mode: str = "Ionian"


@dataclass
class Note:
    Beat: float = 0.0
    Duration: float = 0.0
    Octave: int = 0
    NoteName: str = "A"


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





"""
Component Generators

"""


def NoteFromSpecs(specs: dict) -> Note:
    return Note(Beat=specs["beat"], Duration=specs["duration"])


def BarFromPreset(preset: list) -> Bar:
    bar = Bar()
    for specs in preset:
        bar.Notes.append(NoteFromSpecs(specs))
    return bar


# def ComputeHeightNote(note):
#    return note.Octave * 12 + sc.FindNoteIdInAllNotes(note.NoteName)
