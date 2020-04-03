from __future__ import annotations

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

ALL_INTERVALS_RAW = MINOR_MAJOR_PERFECT_INTERVALS + AUGMENTED_DIMINISHED_INTERVALS


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

    @staticmethod
    def FindTonalDistanceFromOtherSpecs(intervalNumber: int, quality: str) -> int:
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        for elem in ALL_INTERVALS_RAW:
            if elem[0] == intervalNumber:
                if elem[1] == quality:
                    return elem[2]

        raise KeyError("Wrong Inputs: (IntervalNumber: {}, Quality: {}) is not a valid combination for an interval.".format(intervalNumber, quality))

    @classmethod
    def FindQualityFromOtherSpecs(cls, intervalNumber: int, tonalDistance: int) -> str:
        # Need to implement Augmented and Diminished intervals
        # function, or use bigger all_intervals_raw?
        for interval in ALL_INTERVALS:
            if interval.IntervalNumber == intervalNumber and interval.TonalDistance == tonalDistance:
                return interval.Quality
        return None


ALL_INTERVALS = [Interval(*spec[:2]) for spec in ALL_INTERVALS_RAW]
ALL_INTERVALS.sort(key=lambda x: x.TonalDistance)
