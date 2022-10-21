

from dataclasses import dataclass
from typing import List


@dataclass
class ChordDescription:
    """
        Raw description of chords.
        Tonal Intervals are the distance in semitones from the root
    """
    Name: str
    Code: str
    TonalIntervals: List[int]


CHORDS_DESCRIPTIONS: List[ChordDescription] = {
    "m": ChordDescription(
        "Minor",
        "m",
        [0, 3, 7]
    ),
    "M": ChordDescription(
        "Major",
        "M",
        [0, 4, 7]
    ),
    "m7": ChordDescription(
        "Minor 7th",
        "m7",
        [0, 3, 7, 10]
    ),
    "M7": ChordDescription(
        "Major 7th",
        "M7",
        [0, 4, 7, 11]
    )
}
