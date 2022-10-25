from __future__ import annotations
from typing import List, Tuple, Dict, Union

from Data.Intervals import IntervalDescription

from .Notes import *

from MusiStrata.Data.Intervals import ALL_INTERVALS, ALL_INTERVALS_RAW, MINOR_MAJOR_PERFECT_INTERVALS
from MusiStrata.Utils import Record, Library

from MusiStrata.Enums import IntervalQuality
from MusiStrata.Data.Intervals import GetAllIntervals, MAP_INTERVALS


# Need to perform check on input arguments. Done in findtonaldistancefromotherspecs
class BaseInterval(object):
    def __init__(
        self, interval_number: int, quality: IntervalQuality
    ):  # , TonalDistance: int):
        self.IntervalNumber = interval_number
        self.Quality = IntervalQuality.SafeFromStr(quality)
        self.TonalDistance = self.FindTonalDistanceFromNumberAndQuality(
            interval_number, quality
        )

    def __str__(self) -> str:
        return "Interval({}-{}--{} semitones)".format(
            self.IntervalNumber, self.Quality, self.TonalDistance
        )

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
                    "Target: {}, Generated: {}".format(self, generatedInterval)
                )
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
                    "Target: {}, Generated: {}".format(self, generatedInterval)
                )
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
    def FindTonalDistanceFromNumberAndQuality(
        interval_number: int, quality: IntervalQuality
    ) -> int:
        quality = IntervalQuality.SafeFromStr(quality)
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        for elem in ALL_INTERVALS_RAW:
            if elem[0] == interval_number:
                elem[1] = IntervalQuality.SafeFromStr(elem[1])
                if elem[1] == quality:
                    return elem[2]

        raise KeyError(
            "Wrong Inputs: (IntervalNumber: {}, Quality: {}) "
            "is not a valid combination for an interval.".format(
                interval_number, quality
            )
        )

    @classmethod
    def FindQualityFromNumberAndDistance(
        cls, interval_number: int, tonal_distance: int
    ) -> str:
        # Need to implement Augmented and Diminished intervals
        # function, or use bigger all_intervals_raw?
        for interval in GetAllIntervals():
            if (
                interval.IntervalNumber == interval_number
                and interval.TonalDistance == tonal_distance
            ):
                return interval.Quality
        return None

    @classmethod
    def GetValidIntervals(cls, root_note: Note, list_intervals: List[Interval] = []):
        if list_intervals == []:
            list_intervals = ALL_INTERVALS
        outIntervals = []
        for interval in list_intervals:
            _, err = interval.add(root_note)
            if err is None:
                outIntervals.append(interval)
        return outIntervals

    # TRANSCRYPT: Wrapping methods to use this library in the browser
    # Mathematical Operations on Notes, with enforced order
    def Add(self, other):
        return self.__radd__(other)

    def Sub(self, other):
        return self.__rsub__(other)


class Interval(object):
    def __init__(
        self,
        interval_number: int = -1,
        quality: IntervalQuality = IntervalQuality.Major,
        Intervals: List[Interval] = [],
    ):
        if interval_number == -1 and Intervals == []:
            raise ValueError("Interval: No empty constructor defined")
        if type(interval_number) == list:
            raise TypeError(
                "Invalid Arguments. IntervalNumber should be an int. \n Use NamedParameters when creating an interval from other Intervals"
            )
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
                while tonalDistance > 12:
                    validated.append(Interval(8, IntervalQuality.Perfect))
                    tonalDistance -= 12
                # iterate on minor/major/perfect intervals
                foundMatch = False
                for elem in MINOR_MAJOR_PERFECT_INTERVALS:
                    # tonal distance is 3rd elem (so 2 in 0-indexed)
                    # if found match, add to validated
                    if elem[2] == tonalDistance:
                        validated.append(
                            Interval(
                                IntervalNumber=elem[0],
                                Quality=IntervalQuality.SafeFromStr(elem[1]),
                            )
                        )
                        foundMatch = True
                        break
                # else, this means the Interval is a tritone
                if foundMatch == False:
                    validated.append(
                        Interval(IntervalNumber=5, Quality=IntervalQuality.Diminished)
                    )
                # set intervals
                Intervals = validated
            # last check: in case if is empty, or if only unison were given as inputs (so were pruned)
            if len(validated) == 0:
                validated.append(Interval(1, IntervalQuality.Perfect))

        self.Intervals = Intervals
        if interval_number > 8:
            self.Intervals = [
                Interval(8, "Perfect"),
                Interval(interval_number - 7, quality),
            ]
        elif interval_number != -1:
            self.Intervals = [BaseInterval(interval_number, quality)]

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
        return "Interval({} Octaves + {})".format(
            len(self.Intervals) - 1, self.Intervals[-1]
        )

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
                    "Target: {}, Generated: {}".format(self, generatedInterval)
                )

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
                    "Target: {}, Generated: {}".format(self, generatedInterval)
                )

            return newNote, err
        return NotImplemented

    def ShortStr(self) -> str:
        return self[-1].ShortStr()

    @classmethod
    def FromStr(cls, code: str) -> Interval:
        """
            From code such as P-5, m-3... First is letter, second is interval number 
        """
        quality = code[0]
        number = int(code[1:])
        return Interval(number, quality)
         

    @classmethod 
    def FromIntervalDescription(cls, interval_description: Union[str, IntervalDescription]) -> Interval:
        if interval_description.__class__ is str:
            return cls.FromIntervalDescription(MAP_INTERVALS[interval_description])
        else:
            return Interval(
                interval_description.IntervalNumber,
                interval_description.Quality
            )

    @staticmethod
    def FindTonalDistanceFromNumberAndQuality(interval_number: int, quality: str) -> int:
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        return BaseInterval.FindTonalDistanceFromNumberAndQuality(
            interval_number, quality
        )

    @classmethod
    def FindQualityFromNumberAndDistance(
        cls, interval_number: int, tonal_distance: int
    ) -> str:
        # Need to implement Augmented and Diminished intervals
        return BaseInterval.FindQualityFromNumberAndDistance(
            interval_number, tonal_distance
        )

    @classmethod
    def FromNotes(cls, note0: Note, note1: Note) -> Interval:
        intervals = []
        if note0 > note1:
            note0, note1 = note1, note0
        # check if there is more than one octave of difference
        while note1 - note0 > 12:
            intervals.append(Interval(8, "Perfect"))
            note1 = note1 - 12

        intervalNumber = note0.GetIntervalNumber(note1)
        tonalDistance = note1 - note0
        quality = BaseInterval.FindQualityFromNumberAndDistance(
            intervalNumber, tonalDistance
        )
        intervals.append(BaseInterval(intervalNumber, quality))
        return Interval(Intervals=intervals)

    @classmethod
    def GetValidIntervals(
        cls, root_note: Note, intervals: List[Interval] = [], toHigher: bool = True
    ) -> List[Interval]:
        if intervals == []:
            intervals = ALL_INTERVALS
        out_intervals = []
        for interval in intervals:
            if toHigher:
                _, err = root_note + interval
            else:
                _, err = root_note - interval
            if err is None:
                out_intervals.append(interval)
        return out_intervals


