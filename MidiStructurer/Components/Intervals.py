# only use interval number and quality, which gives number semitones?
# still wtf do i do with tritones
# Just ignore it for now?
ALL_INTERVALS_RAW = [
    [1, "Perfect", 0],
    [2, "Minor", 1],
    [2, "Major", 2],
    [3, "Minor", 3],
    [3, "Major", 4],
    [4, "Perfect", 5],
    [4, "Augmented", 6],
    [5, "Perfect", 7],
    [6, "Minor", 8],
    [6, "Major", 9],
    [7, "Minor", 10],
    [7, "Major", 11],
    [8, "Perfect", 12]
]


class Interval(object):
    def __init__(self, intervalNumber: int, quality: str, semitones: int):
        self.IntervalNumber = intervalNumber
        self.Quality = quality
        self.NumberSemitones = semitones

    def __str__(self):
        return "Interval({}-{})".format(self.IntervalNumber, self.Quality)

    def __repr__(self):
        return self.__str__()


ALL_INTERVALS = [Interval(*spec) for spec in ALL_INTERVALS_RAW]


# Associated functions
def FindQualityFromOtherSpecs(intervalNumber: int, semitones: int) -> str:
    for interval in ALL_INTERVALS:
        if interval.IntervalNumber == intervalNumber and interval.NumberSemitones == semitones:
            return interval.Quality
    return None


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
