from typing import List, Tuple, Dict, Union

from MusiStrata.Components import Chord, Interval
from MusiStrata.Utils import Record, Library

from MusiStrata.Enums import IntervalQuality
     
# Using good old wikipedia as starting point
# https://en.wikipedia.org/wiki/Chord_(music)

# using this, and a different approach I guess
# actually this nice: https://en.wikibooks.org/wiki/Music_Theory/Complete_List_of_Chord_Patterns
CHORD_TYPES = [
    "Major", "Minor", "Diminished", "MajorSeventh", "MinorSeventh", "DominantSeventh",
    "Suspended", "Augmented", "Extended"
]

RAW_CHORDS = []

MAJOR_CHORDS = [
    {
        "Name": "Major Triad",
        "Type": "Major",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Perfect")]
    },
    {
        "Name": "Major Seventh",
        "Type": "Major",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Perfect"), Interval(7, "Major")]
    }
]

DOMINANT_CHORDS = [
    {
        "Name": "Dominant Seventh",
        "Type": "Dominant",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Perfect"), Interval(7, "Minor")]
    }
]

MINOR_CHORDS = [
    {
        "Name": "Minor Triad",
        "Type": "Minor",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Perfect")]
    },
    {
        "Name": "Minor Seventh",
        "Type": "Minor",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Perfect"), Interval(7, "Major")]
    }
]

DIMINISHED_CHORDS = [
    {
        "Name": "Diminished Triad",
        "Type": "Diminished",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Diminished")]
    },
    {
        "Name": "Diminished Seventh",
        "Type": "Diminished",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Minor"), Interval(5, "Diminished"),
                      Interval(7, "Diminished")]
    }
]

AUGMENTED_CHORDS = [
    {
        "Name": "Augmented Triad",
        "Type": "Augmented",
        "Attribute": "Triad",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Augmented")]
    },
    {
        "Name": "Augmented Seventh",
        "Type": "Augmented",
        "Attribute": "Seventh",
        "Intervals": [Interval(1, "Perfect"), Interval(3, "Major"), Interval(5, "Augmented"), Interval(7, "Augmented")]
    }
]

RAW_CHORDS = MAJOR_CHORDS + MINOR_CHORDS + DOMINANT_CHORDS + DIMINISHED_CHORDS + AUGMENTED_CHORDS

for c in RAW_CHORDS:
    c["Chord"] = Chord(c["Intervals"])
    del c["Intervals"]


class ChordsLibraryClass(Library):
    BaseName: str = "ChordsLibrary"
    Records: List[Record] = None

    def GetChordsFromType(self, typeValue: str):
        records = self.GetFromValueInField("Type", typeValue)
        return [r.Chord for r in records]

    def GetChordsFromAttribute(self, attributeValue: str):
        records = self.GetFromValueInField("Attribute", attributeValue)
        return [r.Chord for r in records]

    def GetChordFromName(self, nameChord: str):
        record = self.GetFromValueInField("Name", nameChord)
        return record[0].Chord



ChordsLibrary = ChordsLibraryClass(RAW_CHORDS)

# common chords
MINOR_TRIAD = ChordsLibrary.GetChordFromName("Minor Triad")
MAJOR_TRIAD = ChordsLibrary.GetChordFromName("Major Triad")
DIMINISHED_TRIAD = ChordsLibrary.GetChordFromName("Diminished Triad")

# seventh
MINOR_SEVENTH = ChordsLibrary.GetChordFromName("Minor Seventh")
MAJOR_SEVENTH = ChordsLibrary.GetChordFromName("Major Seventh")
DIMINISHED_SEVENTH = ChordsLibrary.GetChordFromName("Diminished Seventh")