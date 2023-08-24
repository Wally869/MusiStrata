from typing import List, Tuple, Dict, Union, Optional

from dataclasses import dataclass

from MusiStrata.Enums import IntervalQuality

from rustshed import Null, Option, Some


INTERVALS_MAP: Dict[str, Tuple[int, IntervalQuality, int]] = {
    # Minor, major, perfect
    "P1": (1, IntervalQuality.Perfect, 0),
    "m2": (2, IntervalQuality.Minor, 1),
    "M2": (2, IntervalQuality.Major, 2),
    "m3": (3, IntervalQuality.Minor, 3),
    "M3": (3, IntervalQuality.Major, 4),
    "P4": (4, IntervalQuality.Perfect, 5),
    "P5": (5, IntervalQuality.Perfect, 7),
    "m6": (6, IntervalQuality.Minor, 8),
    "M6": (6, IntervalQuality.Major, 9),
    "m7": (7, IntervalQuality.Minor, 10),
    "M7": (7, IntervalQuality.Major, 11),
    "P8": (8, IntervalQuality.Perfect, 12),

    # Augmented, diminished
    "d2": (2, IntervalQuality.Diminished, 0),  # Diminished Second
    "A1": (1, IntervalQuality.Augmented, 1),  # Augmented Unison
    "d3": (3, IntervalQuality.Diminished, 2),  # Diminished Third
    "A2": (2, IntervalQuality.Augmented, 3),  # Augmented Second
    "d4": (4, IntervalQuality.Diminished, 4),  # Diminished Fourth
    "d5": (5, IntervalQuality.Diminished, 6),  # Diminished Fifth, aka Tritone
    "A4": (4, IntervalQuality.Augmented, 6),  # Augmented Fourth, aka Tritone
    "d6": (6, IntervalQuality.Diminished, 7),  # Diminished Sixth
    "A5": (5, IntervalQuality.Augmented, 8),  # Augmented Fifth
    "d7": (7, IntervalQuality.Diminished, 9),  # Diminished Seventh
    "A6": (6, IntervalQuality.Augmented, 10),  # Augmented Sixth
    "d8": (8, IntervalQuality.Diminished, 11),  # Diminished Octave
    "A7": (7, IntervalQuality.Augmented, 12),   # Augmented Seventh
}

REVERSE_INTERVALS_MAP: Dict[Tuple[int, IntervalQuality, int], str] = {
    INTERVALS_MAP[key]: key for key in INTERVALS_MAP.keys()
}


def find_interval(interval_number: Optional[int] = None, quality: Optional[IntervalQuality] = None, tonal_distance: Optional[int] = None) -> Option[Tuple[int, IntervalQuality, int]]:
    """
        Greedy search to find a matching interval. Returns the first match
    """
    data = list(INTERVALS_MAP.values())
    for interval in data:
        is_match = True
        if interval_number and interval[0] != interval_number:
            is_match = False
        if quality and interval[1] != quality:
            is_match = False
        if tonal_distance and interval[2] != tonal_distance:
            is_match = False
        if is_match:
            return Some(interval)
    return Null