

class Chord:
    def __init__(self) -> None:
        consonancesTypes = [interval.GetConsonanceType() for interval in chordIntervals]
        tempSumTypes = []
        for field in ["PerfectConsonance", "ImperfectConsonance", "Dissonance"]:
            tempSumTypes.append(
                len(
                    list(filter(lambda consoType: consoType == field, consonancesTypes))
                )
            )

        (
            self.NbPerfectConsonances,
            self.NbImperfectConsonances,
            self.NbDissonances,
        ) = tempSumTypes


class Interval:
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

    def GetConsonanceType(self) -> str:
        return self[-1].GetConsonanceType()