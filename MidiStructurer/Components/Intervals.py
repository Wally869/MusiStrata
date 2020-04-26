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


# Need to perform check on input arguments. Done in findtonaldistancefromotherspecs
# Here, can add checks to see if consonance, dissonance, perfect/imperfect?
class Interval(object):
    def __init__(self, IntervalNumber: int, Quality: str):  # , TonalDistance: int):
        self.IntervalNumber = IntervalNumber
        self.Quality = Quality
        self.TonalDistance = self.FindTonalDistanceFromOtherSpecs(IntervalNumber, Quality)

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
            newNote = other + self.TonalDistance
            generatedInterval = self.GetIntervalSpecs(newNote)
            if other == generatedInterval:
                return newNote, None
            else:
                return newNote, ValueError(
                    "Invalid Interval from given starting note. "
                    "Target Interval: {}, GeneratedInterval: {}".format(
                        other, generatedInterval))

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
    def FindTonalDistanceFromOtherSpecs(intervalNumber: int, quality: str) -> int:
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        for elem in ALL_INTERVALS_RAW:
            if elem[0] == intervalNumber:
                if elem[1] == quality:
                    return elem[2]

        raise KeyError("Wrong Inputs: (IntervalNumber: {}, Quality: {}) "
                       "is not a valid combination for an interval.".format(intervalNumber, quality))

    @classmethod
    def FindQualityFromOtherSpecs(cls, intervalNumber: int, tonalDistance: int) -> str:
        # Need to implement Augmented and Diminished intervals
        # function, or use bigger all_intervals_raw?

        for interval in ALL_INTERVALS:
            if interval.IntervalNumber == intervalNumber and interval.TonalDistance == tonalDistance:
                return interval.Quality
        return None

    def GetConsonanceType(self):
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
    def FromNotes(cls, note0, note1):
        if note0 > note1:
            note0, note1 = note1, note0
        intervalNumber = note0.GetIntervalNumber(note1)
        tonalDistance = note1 - note0
        quality = cls.FindQualityFromOtherSpecs(intervalNumber, tonalDistance)
        return Interval(intervalNumber, quality)


# Handling the case where interval > octave
# Can rework interval as a specific case of CompoundInterval where len(self.Intervals) == 1?
# would be much much better
# will do that once I am more sure of what to do
class CompoundInterval(object):
    def __init__(self, intervals: List[Interval]):
        self.Intervals = intervals

    def __str__(self):
        return "CompoundInterval({} Octaves - {})".format(len(self.Intervals) - 1, self.Intervals[-1])

    def __repr__(self):
        return self.__str__()

    def __radd__(self, other):
        # Have to assume other is Note, want to avoid circular import but seems rough
        # maybe can rewrite so that intervals stuff happens here and not in note?
        # seems more logical: intervals are based on notes, and not reverse
        pass

    @classmethod
    def CreateFrom(cls):
        pass


CHROMATIC_AND_DIATONIC_INTERVALS = [Interval(*spec[:2]) for spec in MINOR_MAJOR_PERFECT_INTERVALS]
PERTURBED_INTERVALS = [Interval(*spec[:2]) for spec in
                       (AUGMENTED_DIMINISHED_INTERVALS + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS)]

ALL_INTERVALS = [Interval(*spec[:2]) for spec in ALL_INTERVALS_RAW]
ALL_INTERVALS.sort(key=lambda x: x.TonalDistance)
