from typing import List

class INote(object):
    pass

class IInterval(object):
    pass

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






