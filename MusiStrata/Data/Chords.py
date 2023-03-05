from typing import List, Dict
from dataclasses import dataclass


@dataclass
class ChordDescription:
    """
        Raw description of chords.
        Tonal Intervals are the distance in semitones from the root
    """
    Name: str
    Code: str
    Intervals: List[str]


CHORDS_DESCRIPTIONS: Dict[str, ChordDescription] = {
    "m": ChordDescription(
        "Minor",
        "m",
        [
            "P1", "m3", "P5"
        ]
    ),
    "M": ChordDescription(
        "Major",
        "M",
        [
            "P1", "M3", "P5"
        ]
    ),
    "m7": ChordDescription(
        "Minor 7th",
        "m7",
        [
            "P1", "m3", "P5", "m7"
        ]
    ),
    "M7": ChordDescription(
        "Major 7th",
        "M7",
        [
            "P1", "M3", "P5", "M7"
        ]
    ),
    "d": ChordDescription(
        "Diminished",
        "d",
        [
            "P1", "m3", "d5"
        ]
    ),
    "D7": ChordDescription(
        "Diminished 7th",
        "D7",
        [
            "P1", "m3", "d5", "d7"
        ]
    ),
    "A": ChordDescription(
        "Augmented",
        "A",
        [
            "P1", "M3", "A5"
        ]
    )
}
