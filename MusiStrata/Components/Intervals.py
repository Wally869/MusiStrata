from __future__ import annotations
from typing import List, Tuple, Dict, Union

from .Notes import *

#from MusiStrata.Data.Intervals import *
from MusiStrata.Utils import Record, Library

from MusiStrata.Enums import IntervalQuality

"""
from .EnumManager import EnumManager_Ordered

class NoteNames(EnumManager_Ordered):
    KeyValuesMap={ALL_NOTES[i]: i for i in range(len(ALL_NOTES))}
    KeyList=ALL_NOTES
    ValuesList=[i for i in range(len(ALL_NOTES))]
"""

ALL_POSSIBLE_QUALITIES = [
    "Minor", "Major", "Perfect", "Diminished", "Augmented", "DoublyDiminished", "DoublyAugmented"
]


# Based on wikipedia table at https://en.wikipedia.org/wiki/Interval_(music)#Main_intervals
MINOR_MAJOR_PERFECT_INTERVALS = [
    [1, "Perfect", 0],  # Perfect Unison
    [2, "Minor", 1],  # Minor Second
    [2, "Major", 2],  # Major Second
    [3, "Minor", 3],  # Minor Third
    [3, "Major", 4],  # Major Third
    [4, "Perfect", 5],  # Perfect Fourth
    [5, "Perfect", 7],  # Perfect Fifth
    [6, "Minor", 8],  # Minor Sixth
    [6, "Major", 9],  # Major Sixth
    [7, "Minor", 10],  # Minor Seventh
    [7, "Major", 11],  # Major Seventh
    [8, "Perfect", 12]  # Perfect Octave
]

AUGMENTED_DIMINISHED_INTERVALS = [
    [2, "Diminished", 0],  # Diminished Second
    [1, "Augmented", 1],  # Augmented Unison
    [3, "Diminished", 2],  # Diminished Third
    [2, "Augmented", 3],  # Augmented Second
    [4, "Diminished", 4],  # Diminished Fourth
    [5, "Diminished", 6],  # Diminished Fifth, aka Tritone
    [4, "Augmented", 6],  # Augmented Fourth, aka Tritone
    [6, "Diminished", 7],  # Diminished Sixth
    [5, "Augmented", 8],  # Augmented Fifth
    [7, "Diminished", 9],  # Diminished Seventh
    [6, "Augmented", 10],  # Augmented Sixth
    [8, "Diminished", 11],  # Diminished Octave
    [7, "Augmented", 12]  # Augmented Seventh
]

# Will need to fill this?
DOUBLY_AUGMENTED_DIMINISHED_INTERVALS = [
    [3, "DoublyAugmented", 5]
]

ALL_INTERVALS_RAW = MINOR_MAJOR_PERFECT_INTERVALS + AUGMENTED_DIMINISHED_INTERVALS + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS
# Setting empty reference, filled after creating the Interval object.
# it is used in a method of Interval so using this trick
ALL_INTERVALS = []






# Need to perform check on input arguments. Done in findtonaldistancefromotherspecs
# Here, can add checks to see if consonance, dissonance, perfect/imperfect?
class BaseInterval(object):
    def __init__(self, IntervalNumber: int, Quality: IntervalQuality):  # , TonalDistance: int):
        if type(Quality) is str:
            Quality = IntervalQuality.FromStr(Quality)
        self.IntervalNumber = IntervalNumber
        self.Quality = Quality
        self.TonalDistance = self.FindTonalDistanceFromNumberAndQuality(IntervalNumber, Quality)

    def __str__(self) -> str:
        return "Interval({}-{}--{} semitones)".format(self.IntervalNumber, self.Quality, self.TonalDistance)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ is other.__class__:
            if self.IntervalNumber == other.IntervalNumber:
                if self.Quality == other.Quality:
                    if self.TonalDistance == other.TonalDistance:
                        return True
            return False
        else:
            return NotImplemented

    # Added mathematical comparisons for easier computation of chords and potential subsetting
    # Purely based on tonal distance?
    def __ge__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.TonalDistance >= other.TonalDistance
        return NotImplemented

    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.TonalDistance > other.TonalDistance
        return NotImplemented

    def __le__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.TonalDistance <= other.TonalDistance
        return NotImplemented

    def __lt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.TonalDistance < other.TonalDistance
        return NotImplemented

    # Mathematical Operations on Notes, with enforced order
    def __radd__(self, other):
        if type(other) == Note:
            # Return Note, None if no error
            # else return Note, ValueError
            newNote = other + self.TonalDistance
            generatedInterval = Interval.FromNotes(other, newNote)
            if generatedInterval == self:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))
        return NotImplemented

    def __rsub__(self, other):
        if type(other) == Note:
            # Return Note, None if no error
            # else return Note, ValueError
            newNote = other - self.TonalDistance
            generatedInterval = Interval.FromNotes(other, newNote)
            if generatedInterval == self:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))
        return NotImplemented

    def ShortStr(self):
        if self.Quality == IntervalQuality.DoublyAugmented:
            qualityString = "DA"
        elif self.Quality == IntervalQuality.DoublyDiminished:
            qualityString = "DD"
        elif self.Quality == IntervalQuality.Minor:
            qualityString = "m"
        else:
            qualityString = self.Quality.value[0]
        return "{}{}".format(qualityString, self.IntervalNumber)

    @staticmethod
    def FindTonalDistanceFromNumberAndQuality(intervalNumber: int, quality: IntervalQuality) -> int:
        if type(quality) is str:
            quality = IntervalQuality.FromStr(quality)
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        for elem in ALL_INTERVALS_RAW:
            if elem[0] == intervalNumber:
                if type(elem[1]) is str:
                    elem[1] = IntervalQuality.FromStr(elem[1])
                if elem[1] == quality:
                    return elem[2]

        raise KeyError("Wrong Inputs: (IntervalNumber: {}, Quality: {}) "
                       "is not a valid combination for an interval.".format(intervalNumber, quality))

    @classmethod
    def FindQualityFromNumberAndDistance(cls, intervalNumber: int, tonalDistance: int) -> str:
        # Need to implement Augmented and Diminished intervals
        # function, or use bigger all_intervals_raw?
        for interval in ALL_INTERVALS:
            if interval.IntervalNumber == intervalNumber and interval.TonalDistance == tonalDistance:
                return interval.Quality
        return None

    def GetConsonanceType(self) -> str:
        # https://en.wikipedia.org/wiki/Consonance_and_dissonance#Consonance
        # perfect consonances: unisons, octaves, perfect fourths, perfect fifths
        # imperfect consonances: major 2nd, minor 7th, major 3rd, minor sixths, minor 3rd, major sixth
        if self.Quality == IntervalQuality.Perfect:
            return "PerfectConsonance"
        specs = [self.Quality, self.IntervalNumber]
        if self.Quality == IntervalQuality.Major:
            if self.IntervalNumber in [2, 3, 6]:
                return "ImperfectConsonance"
        elif self.Quality == IntervalQuality.Minor:
            if self.IntervalNumber in [7, 6, 3]:
                return "ImperfectConsonance"
        return "Dissonance"

    @classmethod
    def GetValidIntervals(cls, rootNote: Note, listIntervals: List[Interval] = []):
        if listIntervals == []:
            listIntervals = ALL_INTERVALS
        outIntervals = []
        for interval in listIntervals:
            _, err = interval.add(rootNote)
            if err is None:
                outIntervals.append(interval)
        return outIntervals

    # TRANSCRYPT: Wrapping methods to use this library in the browser
    # Mathematical Operations on Notes, with enforced order
    def add(self, other):
        if type(other) == Note:
            # Return Note, None if no error
            # else return Note, ValueError
            newNote = other + self.TonalDistance
            generatedInterval = Interval.FromNotes(other, newNote)
            if generatedInterval == self:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))
        return NotImplemented

    def sub(self, other):
        if type(other) == Note:
            # Return Note, None if no error
            # else return Note, ValueError
            newNote = other - self.TonalDistance
            generatedInterval = Interval.FromNotes(other, newNote)
            if generatedInterval == self:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))
        return NotImplemented


class Interval(object):
    def __init__(self, IntervalNumber: int = -1, Quality: IntervalQuality = IntervalQuality.Major, Intervals: List[Interval] = []):
        if IntervalNumber == -1 and Intervals == []:
            raise ValueError("Interval: No empty constructor defined")
        if type(IntervalNumber) == list:
            raise TypeError("Invalid Arguments. IntervalNumber should be an int. \n Use NamedParameters when creating an interval from other Intervals")
        if len(Intervals) >= 2:
            # check the intervals given: aim to only have octaves + 1 non-octave as intervals, so need to perform checks
            validated = []
            disputed = []
            for interval in Intervals:
                if interval == Interval(1, IntervalQuality.Perfect):
                    # skip the unison
                    continue
                elif interval == Interval(8, IntervalQuality.Perfect):
                    # octave is ok
                    validated.append(interval)
                else:
                    # the rest need to be reconciliated
                    disputed.append(interval)
            if len(disputed) == 1 or (len(validated) > 0 and len(disputed) == 0):
                Intervals = validated + disputed
            else:
                # try to find nearest interval, based on number of semitones
                tonalDistance = 0
                for interval in disputed:
                    tonalDistance += interval.TonalDistance
                while (tonalDistance > 12):
                    validated.append(Interval(8, IntervalQuality.Perfect))
                    tonalDistance -= 12
                # iterate on minor/major/perfect intervals
                foundMatch = False
                for elem in MINOR_MAJOR_PERFECT_INTERVALS:
                    # tonal distance is 3rd elem (so 2 in 0-indexed)
                    # if found match, add to validated
                    if elem[2] == tonalDistance:
                        validated.append(Interval(IntervalNumber=elem[0], Quality=IntervalQuality.FromStr(elem[1])))
                        foundMatch = True
                        break
                # else, this means the Interval is a tritone
                if foundMatch == False:
                    validated.append(Interval(IntervalNumber=5, Quality=IntervalQuality.Diminished))
                # set intervals
                Intervals = validated
            # last check: in case if is empty, or if only unison were given as inputs (so were pruned)
            if len(validated) == 0:
                validated.append(Interval(1, IntervalQuality.Perfect))
        
        self.Intervals = Intervals
        if IntervalNumber != -1:
            self.Intervals = [
                BaseInterval(IntervalNumber, Quality)
            ]

    # Properties exposing the sublying properties of the last interval in self.Intervals
    @property
    def TonalDistance(self) -> int:
        # return (len(self.Intervals) - 1) * 12 + self.Intervals[-1].TonalDistance
        return self.Intervals[-1].TonalDistance

    @property
    def Quality(self) -> IntervalQuality:
        return self.Intervals[-1].Quality

    @property
    def IntervalNumber(self) -> int:
        return self.Intervals[-1].IntervalNumber

    def __len__(self) -> int:
        return len(self.Intervals)

    def __getitem__(self, id: int) -> Interval:
        return self.Intervals[id]

    def __str__(self) -> str:
        if len(self) == 1:
            return self[-1].__str__()
        return "Interval({} Octaves + {})".format(len(self.Intervals) - 1, self.Intervals[-1])

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ is other.__class__:
            selfBase = self[-1]
            otherBase = other[-1]
            if selfBase.IntervalNumber == otherBase.IntervalNumber:
                if selfBase.Quality == otherBase.Quality:
                    if selfBase.TonalDistance == otherBase.TonalDistance:
                        return True
            return False
        else:
            return NotImplemented

    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            # if 2 compound intervals
            if len(self) > len(other):
                return True
            elif len(self) < len(other):
                return False
            else:
                if self[-1].TonalDistance <= other[-1].TonalDistance:
                    return False
                else:
                    return True
        return NotImplemented

    def __ge__(self, other) -> bool:
        if self.__class__ is other.__class__:
            # if 2 compound intervals
            if self > other:
                return True
            elif self[-1].TonalDistance == other[-1].TonalDistance:
                return True
            else:
                return False
        return NotImplemented

    def __lt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return not self >= other
        return NotImplemented

    def __le__(self, other) -> bool:
        if self.__class__ is other.__class__:
            if self < other:
                return True
            elif self[-1].TonalDistance == other[-1].TonalDistance:
                return True
            else:
                return False
        return NotImplemented

    def __radd__(self, other) -> Tuple[Note, ValueError]:
        if type(other) == Note:
            newNote = other
            for baseInterval in self.Intervals:
                newNote, _ = newNote + baseInterval
            generatedInterval = Interval.FromNotes(newNote, other)
            if generatedInterval == self:
                err = None
            else:
                err = ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))

            return newNote, err
        return NotImplemented

    def __rsub__(self, other) -> Tuple[Note, ValueError]:
        if type(other) == Note:
            newNote = other
            for baseInterval in self.Intervals:
                newNote, _ = newNote - baseInterval
            generatedInterval = Interval.FromNotes(newNote, other)
            if generatedInterval == self:
                err = None
            else:
                err = ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))

            return newNote, err
        return NotImplemented

    def ShortStr(self) -> str:
        return self[-1].ShortStr()

    def GetConsonanceType(self) -> str:
        return self[-1].GetConsonanceType()

    @staticmethod
    def FindTonalDistanceFromNumberAndQuality(intervalNumber: int, quality: str) -> int:
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        return BaseInterval.FindTonalDistanceFromNumberAndQuality(intervalNumber, quality)

    @classmethod
    def FindQualityFromNumberAndDistance(cls, intervalNumber: int, tonalDistance: int) -> str:
        # Need to implement Augmented and Diminished intervals
        return BaseInterval.FindQualityFromNumberAndDistance(intervalNumber, tonalDistance)

    @classmethod
    def FromNotes(cls, note0: Note, note1: Note) -> Interval:
        intervals = []
        if note0 > note1:
            note0, note1 = note1, note0
        # check if there is more than one octave of difference
        while note1 - note0 > 12:
            intervals.append(
                Interval(8, "Perfect")
            )
            note1 = note1 - 12

        intervalNumber = note0.GetIntervalNumber(note1)
        tonalDistance = note1 - note0
        quality = BaseInterval.FindQualityFromNumberAndDistance(intervalNumber, tonalDistance)
        intervals.append(BaseInterval(intervalNumber, quality))
        return Interval(Intervals=intervals)

    @classmethod
    def GetValidIntervals(cls, rootNote: Note, listIntervals: List[Interval] = [], toHigher: bool = True) -> List[Interval]:
        if listIntervals == []:
            listIntervals = ALL_INTERVALS
        outIntervals = []
        for interval in listIntervals:
            if toHigher:
                _, err = rootNote + interval
            else:
                _, err = rootNote - interval
            if err is None:
                outIntervals.append(interval)
        return outIntervals

    # TRANSCRYPT: Wrapping methods to use this library in the browser
    def Add(self, other) -> List[Note, ValueError]:
        if type(other) == Note:
            # Return Note, None if no error
            # else return Note, ValueError
            newNote = other + self.TonalDistance
            generatedInterval = Interval.FromNotes(other, newNote)
            if generatedInterval == self:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))
        raise NotImplementedError()

    def Sub(self, other) -> List[Note, ValueError]:
        if type(other) == Note:
            # Return Note, None if no error
            # else return Note, ValueError
            newNote = other - self.TonalDistance
            generatedInterval = Interval.FromNotes(other, newNote)
            if generatedInterval == self:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid from given starting note. "
                    "Target: {}, Generated: {}".format(
                        self, generatedInterval))
        return NotImplemented


# same as Instruments and Drums?
# could be nice to easily access diatonic and chromatic intervals, and filter on interval number
class IntervalsLibrary(object):
    BaseName: str = "IntervalsLibrary"
    Records: List[Record] = None


CHROMATIC_AND_DIATONIC_INTERVALS = [Interval(*spec[:2]) for spec in MINOR_MAJOR_PERFECT_INTERVALS]
PERTURBED_INTERVALS = [Interval(*spec[:2]) for spec in
                       (AUGMENTED_DIMINISHED_INTERVALS + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS)]
ALL_INTERVALS = [Interval(*spec[:2]) for spec in ALL_INTERVALS_RAW]
ALL_INTERVALS.sort(key=lambda x: x.TonalDistance)
