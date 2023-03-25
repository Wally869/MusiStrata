from typing import List, Union, TYPE_CHECKING
from typing_extensions import Self

from dataclasses import dataclass, field

from .SoundEvent import SoundEvent

if TYPE_CHECKING:
    from .Track import Track
    from .Song import Song


@dataclass
class Bar:
    SoundEvents: List[SoundEvent] = field(default_factory=list)

    def ToDict(self) -> dict:
        dictRepr = {"SoundEvents": [se.ToDict() for se in self.SoundEvents]}
        return dictRepr

    def ToJSON(self) -> str:
        from json import dumps as _dumps
        return _dumps(self.ToDict())

    def to_track(self, instrument: str = "") -> "Track":
        from .Track import Track
        return Track(
            Instrument=instrument,
            Bars=[self]
        )
    
    def to_song(self, tempo: int = 80, beats_per_bar: int = 4, instrument: str = "") -> "Song":
        from .Song import Song
        return Song(
            tempo,
            beats_per_bar,
            [self.to_track(instrument)]
        )
    
    @classmethod
    def FromDict(cls, dictRepr: dict):
        return Bar([SoundEvent.FromDict(elem) for elem in dictRepr["SoundEvents"]])

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
            return Bar(SoundEvents=self.SoundEvents + other.SoundEvents)
        elif type(other) == SoundEvent:
            return Bar(SoundEvents=self.SoundEvents + [other])
        raise NotImplementedError()

    def __radd__(self, other):
        if type(other) == SoundEvent:
            return Bar(SoundEvents=self.SoundEvents + [other])
        raise NotImplementedError()

    def __mul__(self, other: Union[int, float]):
        # Casting to int if passing a float
        other = int(other)
        return [self] * other

    def append(self, other: Union[SoundEvent, List[SoundEvent]]):
        if type(other) is list:
            if type(other[0]) != SoundEvent:
                raise TypeError(
                    "Bar Class - The append method only accepts a SoundEvent object or a list of SoundEvent objects"
                )
            else:
                self.SoundEvents += other
        elif type(other) == SoundEvent:
            self.SoundEvents.append(other)
        else:
            raise TypeError(
                "Bar Class - The append method only accepts a SoundEvent object or a list of SoundEvent objects"
            )

    def copy(self) -> Self:
        return Bar(
            [se.copy() for se in self.SoundEvents]
        )