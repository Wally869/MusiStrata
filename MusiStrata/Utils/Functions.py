from typing import List, Tuple


class BaseNote(object):
    NoteName: str
    Octave: int
    Height: int


def MinimizeDistance(
    notes1: List[BaseNote], notes2: List[BaseNote], canPad: bool = True
):
    if canPad:
        return _MinimizeDistancePadded(notes1, notes2)
    else:
        return _MinimizeDistanceNotPadded(notes1, notes2)


def _MinimizeDistancePadded(
    notes1: List[BaseNote], notes2: List[BaseNote]
) -> Tuple[List[BaseNote]]:
    # only moving second list
    needsPadding = len(notes1) != len(notes2)
    # start by extracting heights
    # sort by height?
    # notes1.sort(key=lambda x: x.Height)


def _MinimizeDistanceNotPadded(
    notes1: List[BaseNote], notes2: List[BaseNote]
) -> Tuple[List[BaseNote]]:
    pass
