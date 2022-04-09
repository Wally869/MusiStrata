from __future__ import annotations
from typing import List, Tuple, Dict, Union

from MusiStrata.Enums import NoteNames, StaffPositions

from dataclasses import dataclass, field


class Note(object):
    def __init__(self, name: str = "A", octave: int = 5):
        self._Name = NoteNames.SafeFromStr(name)
        
        # Need to check max octave for Midi
        if type(octave) != int:
            raise TypeError("Octave must be a non-negative integer.")
        elif octave < 0:
            raise ValueError("Octave must be a non-negative integer.")

        self._Octave = octave

    @property
    def Name(self) -> NoteNames:
        return self._Name.name

    @Name.setter
    def Name(self, new_name: str) -> None:
        self._Name = NoteNames.SafeFromStr(new_name)

    @property
    def Octave(self) -> int:
        return self._Octave

    @Octave.setter
    def Octave(self, new_octave: int) -> None:
        if type(new_octave) != int:
            raise TypeError("Octave must be a non-negative integer.")
        # Separating value checking from type checking
        if new_octave < 0:
            raise ValueError("Octave must be a non-negative integer.")
        self._Octave = new_octave

    def __hash__(self):
        return self.Height

    def __str__(self) -> str:
        return "Note({})".format(self.Name + str(self.Octave))

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if self.__class__ is not other.__class__:
            return False
        else:
            if self.Name == other.Name and self.Octave == other.Octave:
                return True
            else:
                return False

    def __ge__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height >= other.Height
        return NotImplemented

    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height > other.Height
        return NotImplemented

    def __le__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height <= other.Height
        return NotImplemented

    def __lt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.Height < other.Height
        return NotImplemented

    def __add__(self, other: int) -> Note:
        if type(other) == int:
            # error if other is negative. Fixing this
            if other < 0:
                return self.__sub__(abs(other))
            else:
                outName, deltaOctave = self._Name + other

                return Note(name=outName.name, octave=self.Octave + deltaOctave)
        else:
            return NotImplemented

    def __sub__(self, other: Union[int, Note]) -> Union[int, Note]:
        if self.__class__ is other.__class__:
            return self.GetTonalDistance(other)
        elif type(other) == int:
            if other < 0:
                return self.__add__(abs(other))
            else:
                outName, deltaOctave = self._Name - other

                return Note(name=outName.name, octave=self.Octave + deltaOctave)
        else:
            return NotImplemented

    def ToDict(self):
        dict_repr = {"Name": self.Name, "Octave": self.Octave}
        return dict_repr

    def ToJSON(self):
        from json import dumps as _dumps

        dict_repr = self.ToDict()
        return _dumps(dict_repr)

    @classmethod
    def FromDict(cls, dict_repr: dict):
        return Note(dict_repr["Name"], dict_repr["Octave"])

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads

        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)

    # Added this to expand scales. Can also use Note + 12 for octave difference
    # but I thought additional method would be nice
    def NewFromOctaveDifference(self, octave_diff: int) -> Note:
        newNote = self + 12 * octave_diff
        return newNote

    @property
    def Height(self) -> int:
        return self.Octave * 12 + self._Name.value

    @property
    def Frequency(self) -> float:
        # Using this as reference: https://pages.mtu.edu/~suits/notefreqs.html
        return 16.35 * (2**self.Octave) * (2 ** (1 / 12)) ** self._Name.value

    # Return distance between this note and another in term of semitones
    def GetTonalDistance(self, other) -> int:
        if self.__class__ is other.__class__:
            return self.Height - other.Height
        return NotImplemented

    # Returning a positive tonal distance
    def GetRootedTonalDistance(self, other) -> int:
        if self.__class__ is other.__class__:
            return max(self.Height - other.Height, other.Height - self.Height)
        return NotImplemented

    def GetStaffPositionAsEnumElem(self) -> StaffPositions:
        return self._Name.ToStaffPosition()

    def GetStaffPositionAsLetter(self) -> str:
        return self._Name.ToStaffPosition().name

    def GetStaffPositionAsInteger(self) -> int:
        return StaffPositions(self.GetStaffPositionAsLetter()).value

    # This is order dependent. Self should be the root note of the chord
    def GetIntervalNumber(self, other: Note) -> int:
        if self.__class__ is other.__class__:
            staff1 = self.GetStaffPositionAsEnumElem()
            staff2 = other.GetStaffPositionAsEnumElem()

            outValue = 0
            while staff1.value != staff2.value:
                outValue += 1
                staff1 = (staff1 + 1)[0]

            # lowest note is root of chord and therefore the base for interval calculation
            # Incrementing by one so that it makes sense (a A - B chord is a second, but this return 1)
            outValue += 1
            # adding exception for octave
            if outValue == 1:
                if abs(self - other) <= 2:
                    outValue = 1
                else:
                    outValue = 8

            return outValue
        raise TypeError("Note - GetIntervalError requires Note input.")

    @classmethod
    def FromHeight(cls, height: int) -> Note:
        octave = height // 12
        name_height = height - octave * 12
        name = NoteNames.SafeFromInt(name_height).name
        return Note(name=name, octave=octave)

    # TRANSCRYPT: Wrapping methods to use this library in the browser
    def Add(self, other):
        return self + other

    def Sub(self, other):
        return self - other
