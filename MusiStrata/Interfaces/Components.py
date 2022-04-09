from typing import List, Union

from MusiStrata.Enums import IntervalQuality

class INote(object):
    pass


class IInterval(object):
    def __init__(self, IntervalNumber: int, Quality: Union[str, IntervalQuality], TonalDistance: int = None):
        self.IntervalNumber: int = IntervalNumber
        self.Quality: IntervalQuality = IntervalQuality.SafeFromStr(Quality)
        self.TonalDistance: int = TonalDistance

    def ToInterval(self) -> "Interval":
        from MusiStrata.Components import Interval
        return Interval(self.IntervalNumber, self.Quality)


class IScale(object):
    pass

class IChord(object):
    pass

class ISoundEvent(object):
    Beat: float
    Duration: float
    Note: INote
    Velocity: int

class IBar(object):
    SoundEvents: List[ISoundEvent]

class ITrack(object):
    Name: str
    Instrument: str
    Bars: List[IBar]
    IsDrumsTrack: bool
    BankUsed: int






