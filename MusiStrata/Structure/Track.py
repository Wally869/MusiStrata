from typing import List, Union, TYPE_CHECKING
from typing_extensions import Self

from dataclasses import dataclass, field

from .Bar import Bar

if TYPE_CHECKING:
    from .Song import Song


@dataclass
class Track:
    Name: str = "Untitled"
    Instrument: str = ""
    Bars: list = field(default_factory=list)
    IsDrumsTrack: bool = False
    BankUsed: int = 0
    # Automation: np.ndarray[float]

    def to_song(self, tempo: int = 80, beats_per_bar: int = 4) -> "Song":
        from .Song import Song
        return Song(
            tempo,
            beats_per_bar,
            [self]
        )

    def ToDict(self) -> dict:
        dictRepr = {
            "Name": self.Name,
            "Instrument": self.Instrument,
            "Bars": [b.ToDict() for b in self.Bars],
            "IsDrumsTrack": self.IsDrumsTrack,
            "BankUsed": self.BankUsed,
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
            BankUsed=dictRepr["BankUsed"],
        )

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads

        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)

    def __str__(self):
        if self.IsDrumsTrack:
            outStr = "DrumsTrack("
        else:
            outStr = "Track("
        
        return outStr + self.Name + " - " + ("NA" if self.Instrument == "" else self.Instrument) + ")"

    def __repr__(self):
        return str(self)

    # Adding an __add__ overload to allow concatenating bars in a simple way
    # this is to make easier to generate sections and then appending them
    def __add__(self, other: Union[Self, Bar]) -> Self:
        """
            Add other to self.Bars
        """
        if type(other) is Track:
            outTrack = self
            outTrack.Bars = outTrack.Bars + other.Bars
            return outTrack
        elif other.__class__ is Bar:
            outTrack = Track(self.Name, self.Instrument, self.Bars[:] + [other], self.IsDrumsTrack, self.BankUsed)
            return outTrack
        else:
            return NotImplemented

    def DuplicateBars(self, duplication_factor: int):
        # duplicate bars and append them to the track
        # casting float to int
        self.Bars = self.Bars * duplication_factor

    def append(self, other: Union[Bar, List[Bar]]):
        if type(other) is list:
            if type(other[0]) != Bar:
                raise TypeError(
                    "Track Class - The append method only accepts a Bar object or a list of Bar objects"
                )
            else:
                self.Bars += other
        elif type(other) == Bar:
            self.Bars.append(other)
        else:
            raise TypeError(
                "Track Class - The append method only accepts a Bar object or a list of Bar objects"
            )


# Do I really need a timesignature? For my implementation, beats per bar is enough?
@dataclass
class TimeSignature:
    BeatsPerBar: int = 4
    BeatUnit: int = 4

    def __str__(self):
        return "TimeSignature(BeatsPerBar={}, BeatUnit={})".format(
            self.BeatsPerBar, self.BeatUnit
        )

    def __repr__(self):
        return self.__str__()

