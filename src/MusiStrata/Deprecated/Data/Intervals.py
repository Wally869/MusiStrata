from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Union

from MusiStrata.Enums import IntervalQuality



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
    [8, "Perfect", 12],  # Perfect Octave
]

# extend base interval by an octave
EXTENDED = [
    [interval[0] + 7, interval[1], interval[2] + 12]
    for interval in MINOR_MAJOR_PERFECT_INTERVALS[1:]
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
    [7, "Augmented", 12],  # Augmented Seventh
]


@dataclass
class IntervalDescription:
    """
        Raw description of Intervals.
        Tonal Intervals are the distance in semitones from the root
    """
    Name: str
    Code: str
    IntervalNumber: int
    Quality: IntervalQuality
    TonalDistance: int

INTERVALS: List[IntervalDescription] = list(map(lambda x: IntervalDescription(
    "{} {}".format(x[1], x[0]),
    "{}{}".format(x[1][0] if x[1] != "Minor" else "m", x[0]),
    x[0],
    IntervalQuality.SafeFromStr(x[1]),
    x[2]
), MINOR_MAJOR_PERFECT_INTERVALS + AUGMENTED_DIMINISHED_INTERVALS + EXTENDED))

MAP_INTERVALS = {
    x.Code: x for x in INTERVALS
}

# Will need to fill this?
DOUBLY_AUGMENTED_DIMINISHED_INTERVALS = [[3, "DoublyAugmented", 5]]

ALL_INTERVALS_RAW = (
    MINOR_MAJOR_PERFECT_INTERVALS
    + AUGMENTED_DIMINISHED_INTERVALS
    + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS
)
# Setting empty reference, filled after creating the Interval object.
# it is used in a method of Interval so using this trick
ALL_INTERVALS = []

def GetAllIntervals():
    global ALL_INTERVALS
    if len(ALL_INTERVALS) == 0:
        from MusiStrata.Components.Intervals import Interval    
        CHROMATIC_AND_DIATONIC_INTERVALS = [
            Interval(spec[0], spec[1]) for spec in MINOR_MAJOR_PERFECT_INTERVALS
        ]
        PERTURBED_INTERVALS = [
            Interval(spec[0], spec[1])
            for spec in (AUGMENTED_DIMINISHED_INTERVALS + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS)
        ]
        ALL_INTERVALS = [Interval(spec[0], spec[1]) for spec in ALL_INTERVALS_RAW]
        ALL_INTERVALS.sort(key=lambda x: x.tonal_distance) 
    return ALL_INTERVALS

