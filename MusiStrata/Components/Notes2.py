from typing import Union, Optional
from typing_extensions import Self
from dataclasses import dataclass

from MusiStrata.Enums import NoteNames


class Note2:
    __name: NoteNames
    octave: int

    def __init__(self, name: Union[str, NoteNames], octave: int) -> None:
        self.__name = NoteNames.SafeFromStr(name)
            
        # Need to check max octave for Midi
        if type(octave) != int or octave < 0:
            raise TypeError("Octave must be a non-negative integer.")
        self.octave = octave

    def __hash__(self):
        return "note{}".format(self.height)

    def __str__(self) -> str:
        return "Note({}{})".format(self.__name.name, str(self.octave))

    def __repr__(self) -> str:
        return str(self)

    @property
    def name(self) -> str:
        return self.__name.name
    
    @property
    def height(self) -> int:
        return self.octave * 12 + self.__name.value

    def __ge__(self, other: Self) -> bool:
        if self.__class__ is other.__class__:
            return self.height >= other.height
        raise TypeError()

    def __gt__(self, other: Self) -> bool:
        if self.__class__ is other.__class__:
            return self.height > other.height
        raise TypeError()

    def __le__(self, other: Self) -> bool:
        if self.__class__ is other.__class__:
            return self.height <= other.height
        raise TypeError()

    def __lt__(self, other: Self) -> bool:
        if self.__class__ is other.__class__:
            return self.height < other.height
        raise TypeError()

    def __eq__(self, other: Self) -> bool:
        if self.__class__ is not other.__class__:
            raise TypeError()
        else:
            if self.__name == other.__name and self.octave == other.octave:
                return True
            else:
                return False

    def __add__(self, delta: int) -> Self:
        name, delta_octave = self.__name + delta
        return Note2(
            name,
            self.octave + delta_octave
        )

    def __sub__(self, delta: int) -> Self:
        name, delta_octave = self.__name - delta
        return Note2(
            name,
            self.octave + delta_octave
        )

    @classmethod
    def from_height(cls, height: int) -> Self:
        octave = height // 12
        name_height = height - octave * 12
        name = NoteNames.SafeFromInt(name_height).name
        return Note2(name=name, octave=octave)

    