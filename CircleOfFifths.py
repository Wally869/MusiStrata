"""
Handling Scale switching:
Switch to close scales
dependent on refNote and Mode obviously
"""
from Components import Scale

from typing import List

# not using flats coz of implementation restrictions
MAJOR_NEIGHBOURS = {
    "C": ["F", "G"],
    "G": ["C", "D"],
    "D": ["G", "A"],
    "A": ["D", "E"],
    "E": ["A", "B"],
    "B": ["E", "F#"],
    "F#": ["B", "C#"],
    "C#": ["F#", "G#"],
    "G#": ["C#", "D#"],
    "D#": ["G#", "A#"],
    "A#": ["D#", "F"],
    "F": ["A#", "C"]
}

# Minors have same neighbours as majors
MINOR_NEIGHBOURS = MAJOR_NEIGHBOURS

MINOR_FROM_MAJOR = {
    "C": "A",
    "G": "E",
    "D": "B",
    "A": "F#",
    "E": "C#",
    "B": "G#",
    "F#": "D#",
    "C#": "A#",
    "G#": "F",
    "D#": "C",
    "A#": "G",
    "F": "D"
}

def FindMajorNeighbours(noteRef: str) -> List[Scale]:
    outNoteRefs = MAJOR_NEIGHBOURS[noteRef]
    return [Scale(n, "Major") for n in outNoteRefs]

def FindMinorNeighbours(noteRef: str) -> List[Scale]:
    outNoteRefs = MINOR_NEIGHBOURS[noteRef]
    return [Scale(n, "Minor") for n in outNoteRefs]

def FindMinorFromMajor(noteRef: str) -> Scale:
    outNoteRef = MINOR_FROM_MAJOR[noteRef]
    return Scale(outNoteRef, "Minor")

def FindMajorFromMinor(noteRef: str) -> Scale:
    keys = list(MINOR_FROM_MAJOR.keys())
    for k in keys:
        if (MINOR_FROM_MAJOR[k] == noteRef):
            return Scale(k, "Major")

def GetAllowedScales(mainScale: Scale) -> List[Scale]:
    outScales = [mainScale]
    if mainScale.Mode == "Major":
        outScales += FindMajorNeighbours(mainScale.RefNote)
        outScales += [FindMinorFromMajor(mainScale.RefNote)]
    else:
        outScales += FindMinorNeighbours(mainScale.RefNote)
        outScales += [FindMajorFromMinor(mainScale.RefNote)]

    return outScales
