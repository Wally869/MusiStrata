from __future__ import annotations
from typing import List, Tuple, Dict, Union

# from MusiStrata.Components import Interval
from MusiStrata.Utils import Record, Library

from MusiStrata.Enums import IntervalQuality

from MusiStrata.Interfaces.Components import IInterval


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


# same as Instruments and Drums?
# could be nice to easily access diatonic and chromatic intervals, and filter on interval number
class IntervalsLibrary(object):
    BaseName: str = "IntervalsLibrary"
    Records: List[Record] = None


CHROMATIC_AND_DIATONIC_INTERVALS = [
    IInterval(*spec) for spec in MINOR_MAJOR_PERFECT_INTERVALS
]
PERTURBED_INTERVALS = [
    IInterval(*spec)
    for spec in (AUGMENTED_DIMINISHED_INTERVALS + DOUBLY_AUGMENTED_DIMINISHED_INTERVALS)
]
ALL_INTERVALS = [IInterval(*spec) for spec in ALL_INTERVALS_RAW]
ALL_INTERVALS.sort(key=lambda x: x.TonalDistance)
