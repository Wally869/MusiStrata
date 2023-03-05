from typing import Union, Optional, Dict
from typing_extensions import Self
from dataclasses import dataclass

from MusiStrata.Enums import NoteNames

@dataclass
class Note:
    name: NoteNames
    octave: int

    def __init__(self, name: Union[str, NoteNames] = "C", octave: int = 5) -> None:
        self.name = NoteNames.SafeFromStr(name)
            
        # Need to check max octave for Midi
        if type(octave) != int or octave < 0:
            raise TypeError("Octave must be a non-negative integer.")
        self.octave = octave

    def to_dict(self) -> Dict: 
        return {"name": self.name.name, "octave": self.octave}
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return Note(data["name"], data["octave"])

    def __hash__(self):
        return "note{}".format(self.height)

    def __str__(self) -> str:
        return "Note({}{})".format(self.name.name, str(self.octave))

    def __repr__(self) -> str:
        return str(self)

    @property
    def height(self) -> int:
        """
            Get the note semitonal height. Starts at C0 = 0.
        """
        return self.octave * 12 + self.name.value

    @property
    def Frequency(self) -> float:
        """
            Using this as reference: https://pages.mtu.edu/~suits/notefreqs.html
        """
        return 16.35 * (2 ** self.octave) * (2 ** (1 / 12)) ** self.name.value
    
    def __ge__(self, other: Self) -> bool:
        return self.height >= other.height

    def __gt__(self, other: Self) -> bool:
        return self.height > other.height

    def __le__(self, other: Self) -> bool:
        return self.height <= other.height

    def __lt__(self, other: Self) -> bool:
        return self.height < other.height

    def __eq__(self, other: Self) -> bool:
        return self.name == other.name and self.octave == other.octave

    def __add__(self, delta: int) -> Self:
        name, delta_octave = self.name + delta
        return Note(
            name,
            self.octave + delta_octave
        )

    def __sub__(self, delta: int) -> Self:
        name, delta_octave = self.name - delta
        return Note(
            name,
            self.octave + delta_octave
        )

    def get_tonal_distance(self, other: Self) -> int:
        """
            Return the tonal distance in semitones between two notes.
        """
        return abs(self.height - other.height)

    @classmethod
    def from_height(cls, height: int) -> Self:
        """
            Create a note from its semitonal height.
        """
        octave = height // 12
        name_height = height - octave * 12
        name = NoteNames.SafeFromInt(name_height)
        return Note(name=name, octave=octave)

    