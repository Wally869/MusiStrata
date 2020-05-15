from __future__ import annotations

from .Notes import *

ALL_POSSIBLE_QUALITIES = [
    "Minor", "Major", "Perfect", "Diminished", "Augmented", "DoublyDiminished", "DoublyAugmented"
]

# only use interval number and quality, which gives number semitones?
# still wtf do i do with tritones
# Just ignore it for now?
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
    def __init__(self, IntervalNumber: int, Quality: str):  # , TonalDistance: int):
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
        if self.Quality == "DoublyAugmented":
            qualityString = "DA"
        elif self.Quality == "DoublyDiminished":
            qualityString = "DD"
        elif self.Quality == "Minor":
            qualityString = "m"
        else:
            qualityString = self.Quality[0]
        return "{}{}".format(qualityString, self.IntervalNumber)

    @staticmethod
    def FindTonalDistanceFromNumberAndQuality(intervalNumber: int, quality: str) -> int:
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        for elem in ALL_INTERVALS_RAW:
            if elem[0] == intervalNumber:
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
        if self.Quality == "Perfect":
            return "PerfectConsonance"
        specs = [self.Quality, self.IntervalNumber]
        if self.Quality == "Major":
            if self.IntervalNumber in [2, 3, 6]:
                return "ImperfectConsonance"
        elif self.Quality == "Minor":
            if self.IntervalNumber in [7, 6, 3]:
                return "ImperfectConsonance"
        return "Dissonance"

    @classmethod
    def GetValidIntervals(cls, rootNote: Note, listIntervals: List[Interval] = []):
        if listIntervals == []:
            listIntervals = ALL_INTERVALS
        outIntervals = []
        for interval in listIntervals:
            _, err = rootNote + interval
            if err is None:
                outIntervals.append(interval)
        return outIntervals


# Handling the case where interval > octave
# Can rework interval as a specific case of CompoundInterval where len(self.Intervals) == 1?
# would be much much better
# will do that once I am more sure of what to do
class Interval(object):
    def __init__(self, IntervalNumber: int = -1, Quality: string = "", Intervals: List[Interval] = []):
        if IntervalNumber == -1 and Quality == "" and Intervals == []:
            raise ValueError("Interval: No empty constructor defined")
        self.Intervals = Intervals
        if IntervalNumber != -1:
            if Quality != "":
                self.Intervals = [
                    BaseInterval(IntervalNumber, Quality)
                ]

    # Properties exposing the sublying properties of the last interval in self.Intervals
    @property
    def TonalDistance(self) -> int:
        # return (len(self.Intervals) - 1) * 12 + self.Intervals[-1].TonalDistance
        return self.Intervals[-1].TonalDistance

    @property
    def Quality(self) -> str:
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

    # Added mathematical comparisons for easier computation of chords and potential subsetting
    # Purely based on tonal distance
    # Might have to change eq to use only tonal distance?
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
        # Have to assume other is Note, want to avoid circular import but seems rough
        # maybe can rewrite so that intervals stuff happens here and not in note?
        # seems more logical: intervals are based on notes, and not reverse
        if type(other) == Note:
            newNote = other
            for baseInterval in self.Intervals:
                # all intervals are combination of octave and sub octave
                # octave ALWAYS exist, so only need to keep last error
                # Looks like error not valid because of typing? check below
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
    def GetValidIntervals(cls, rootNote: Note, listIntervals: List[Interval] = [], toHigher: Bool = True):
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


# same as Instruments and Drums?
class IntervalsLibrary(object):
    pass


CHROMATIC_AND_DIATONIC_INTERVALS = [Interval(*spec[:2]) for spec in MINOR_MAJOR_PERFECT_INTERVALS]
PERTURBED_INTERVALS = [Interval(*spec[:2]) for spec in
                       (AUGMENTED_DIMINISHED_INTERVALS + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS)]
ALL_INTERVALS = [Interval(*spec[:2]) for spec in ALL_INTERVALS_RAW]
ALL_INTERVALS.sort(key=lambda x: x.TonalDistance)
