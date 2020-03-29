"""
Handling Scale switching:
Switch to close scales
dependent on refNote and Mode obviously
"""
from .Components.Scales import ScaleSpecs

from typing import List

# not using flats coz of implementation restrictions
MAJOR_NEIGHBOURS = {
    "C": ["F", "G"],
    "G": ["C", "D"],
    "D": ["G", "A"],
    "A": ["D", "E"],
    "E": ["A", "B"],
    "B": ["E", "Fs"],
    "Fs": ["B", "Cs"],
    "Cs": ["Fs", "Gs"],
    "Gs": ["Cs", "Ds"],
    "Ds": ["Gs", "As"],
    "As": ["Ds", "F"],
    "F": ["As", "C"]
}

# Minors have same neighbours as majors
MINOR_NEIGHBOURS = MAJOR_NEIGHBOURS

MINOR_FROM_MAJOR = {
    "C": "A",
    "G": "E",
    "D": "B",
    "A": "Fs",
    "E": "Cs",
    "B": "Gs",
    "Fs": "Ds",
    "Cs": "As",
    "Gs": "F",
    "Ds": "C",
    "As": "G",
    "F": "D"
}


def FindMajorNeighbours(noteRef: str) -> List[ScaleSpecs]:
    outNoteRefs = MAJOR_NEIGHBOURS[noteRef]
    return [ScaleSpecs(refNote=n, type="Major") for n in outNoteRefs]


def FindMinorNeighbours(noteRef: str) -> List[ScaleSpecs]:
    outNoteRefs = MINOR_NEIGHBOURS[noteRef]
    return [ScaleSpecs(refNote=n, type="Minor") for n in outNoteRefs]


def FindMinorFromMajor(noteRef: str) -> ScaleSpecs:
    outNoteRef = MINOR_FROM_MAJOR[noteRef]
    return ScaleSpecs(refNote=outNoteRef, type="Minor")


def FindMajorFromMinor(noteRef: str) -> ScaleSpecs:
    keys = list(MINOR_FROM_MAJOR.keys())
    for k in keys:
        if (MINOR_FROM_MAJOR[k] == noteRef):
            return ScaleSpecs(refNote=k, type="Major")


def GetAllowedScales(mainScale: ScaleSpecs) -> List[ScaleSpecs]:
    outScales = [mainScale]
    if mainScale.Type == "Major":
        outScales += FindMajorNeighbours(mainScale.RefNote)
        outScales += [FindMinorFromMajor(mainScale.RefNote)]
    else:
        outScales += FindMinorNeighbours(mainScale.RefNote)
        outScales += [FindMajorFromMinor(mainScale.RefNote)]

    return outScales
