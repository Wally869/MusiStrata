from typing import List, Dict

from MusiStrata.Enums import (
    ScaleModes,
)
from enum import Enum



SCALE_TONES: Dict[ScaleModes, List[int]] = {
    ScaleModes.Major: [2, 2, 1, 2, 2, 2, 1],
    ScaleModes.Ionian: [2, 2, 1, 2, 2, 2, 1],
    ScaleModes.Dorian: [2, 1, 2, 2, 2, 1, 2],
    ScaleModes.Phrygian: [1, 2, 2, 2, 1, 2, 2],
    ScaleModes.Lydian: [2, 2, 2, 1, 2, 2, 1],
    ScaleModes.Mixolydian: [2, 2, 1, 2, 2, 1, 2],
    ScaleModes.Minor: [2, 1, 2, 2, 1, 2, 2],
    ScaleModes.MinorHarmonic: [2, 1, 2, 2, 1, 3, 1],
    ScaleModes.Aeolian: [2, 1, 2, 2, 1, 2, 2],
    ScaleModes.Locrian: [1, 2, 2, 1, 2, 2, 2]
}

SCALE_CHORD_CODES: Dict[ScaleModes, List[str]] = {
    ScaleModes.Major: ["M", "m", "m", "M", "M", "m","d"],
    ScaleModes.Ionian: ["M", "m", "m", "M", "M", "m","d"],
    ScaleModes.Dorian: ["m", "m", "M", "M", "m", "d", "M"],
    ScaleModes.Phrygian: ["m", "M", "M", "m", "d", "M", "m"],
    ScaleModes.Lydian: ["M", "M", "m", "d", "M", "m", "m"],
    ScaleModes.Mixolydian: ["M", "m", "d", "M", "m", "m", "M"],
    ScaleModes.Minor: ["m", "d", "M", "m", "m", "M", "M"],
    ScaleModes.Aeolian: ["m", "d", "M", "m", "m", "M", "M"],
    ScaleModes.Locrian: ["d", "M", "m", "m", "M", "M", "m"],

    ScaleModes.MinorHarmonic: ["m", "d", "A", "m", "M", "M", "d"]

}