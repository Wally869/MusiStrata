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

    def __str__(self):
        return "Interval({}-{}--{} semitones)".format(self.IntervalNumber, self.Quality, self.TonalDistance)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            if self.IntervalNumber == other.IntervalNumber:
                if self.Quality == other.Quality:
                    if self.TonalDistance == other.TonalDistance:
                        return True
            return False
        else:
            return NotImplemented

    @staticmethod
    def FindTonalDistanceFromOtherSpecs(intervalNumber: int, quality: str):
        # This function gets us the tonal distance, but also ensures that correct parameters have been input
        for elem in ALL_INTERVALS_RAW:
            if elem[0] == intervalNumber:
                if elem[1] == quality:
                    return elem[2]

        raise KeyError("Wrong Inputs: (IntervalNumber: {}, Quality: {}) is not a valid combination for an interval.".format(intervalNumber, quality))

    @classmethod
    def FindQualityFromOtherSpecs(cls, intervalNumber: int, tonalDistance: int):
        # Need to implement Augmented and Diminished intervals
        # function, or use bigger all_intervals_raw?
        for interval in ALL_INTERVALS:
            if interval.IntervalNumber == intervalNumber and interval.TonalDistance == tonalDistance:
                return interval.Quality
        return None


ALL_INTERVALS = [Interval(*spec[:2]) for spec in ALL_INTERVALS_RAW]

"""
Keeping all this for now, not sure yet what is the best way to handle intervals

# interval number, str name, type (minor/major/perfect), consonant/dissonant, perfect/imperfect consonance/dissonance,  nb semitones
# NEED TO BE ABLE TO COMPOSE INTERVALS, AS WELL AS INVERSIONS?
# or not, could be done in a chords module I guess, inversions have no direct link to intervals


# WHAT TO DO FOR TRITONE?
# chose to put 2nd major as dissonance unlike what wikipedia wrote
ALL_INTERVALS_RAW = [
    [1, "Unison", "Perfect", "Consonant", "Perfect", 0],
    [2, "Second", "Minor", "Dissonant", "Perfect", 1],
    [2, "Second", "Major", "Dissonant", "Perfect", 2],
    [3, "Third", "Minor", "Consonant", "Imperfect", 3],
    [3, "Third", "Major", "Consonant", "Imperfect", 4],
    [4, "Fourth", "Perfect", "Consonant", "Perfect", 5],

    # TRITONE? putting both augmented forth and dimnished fifth?
    [4, "Fourth", "Augmented", "Dissonant", "Perfect", 6],
    [5, "Fifth", "Dimnished", "Dissonant", "Perfect", 6],

    [5, "Fifth", "Perfect", "Consonant", "Perfect", 7],
    [6, "Sixth", "Minor", "Consonant", "Imperfect", 8],
    [6, "Sixth", "Major", "Consonant", "Imperfect", 9],
    [7, "Seventh", "Minor", "Dissonant", "Perfect", 10],
    [7, "Seventh", "Major", "Dissonant", "Perfect", 11],
    [8, "Octave", "Perfect", "Consonant", "Perfect", 12]
]




class Interval(object):
    def __init__(self,
                 intervalNumber: int,
                 intervalNumberStr: str,
                 intervalQuality: str,
                 consonance: str,
                 perfection: str,
                 distanceSemitones: int
                 ):
        self.IntervalNumber = intervalNumber
        self.IntervalNumberStr = intervalNumberStr
        self.Quality = intervalQuality
        self.Consonance = consonance
        self.Perfection = perfection
        self.DistanceSemitones = distanceSemitones

    def __str__(self):
        return "Interval({}-{})".format(self.IntervalNumberStr, self.Quality)

    def __repr__(self):
        return self.__str__()


ALL_INTERVALS = [
    Interval(
        *i
    ) for i in ALL_INTERVALS_RAW
]


"""
