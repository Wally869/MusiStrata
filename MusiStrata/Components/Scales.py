from __future__ import annotations
from typing import List, Tuple, Dict, Union

from MusiStrata.Components.Notes import NoteNames, Note

from MusiStrata.Utils import FilterRepeated as FilterOutRepeatedNotes
from MusiStrata.Enums import ScaleModes, Mode

from MusiStrata.Enums import (
    ChordBase,
    ChordExtension,
    Mode,
    ScaleChordExtension,
    ScaleModes,
)


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
    "F": ["As", "C"],
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
    "F": "D",
}



class Scale(object):
    def __init__(self, ref_note: Union[str, NoteNames] = "A", scale_type: Union[str, Mode] = "Major"):
        self.RefNote = NoteNames.SafeFromStr(ref_note)
        self.Type = Mode.SafeFromStr(scale_type)

    def __str__(self):
        return "Scale({})".format(self.RefNote.name + "-" + self.Type.name)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        else:
            return self.RefNote == other.RefNote and self.Type == other.Type

    def GetScaleNotes(
        self, octave: int = 5, mode: str = "Ionian"
    ) -> List[Note]:
        mode = ScaleModes.SafeFromStr(mode)
        # Get tone succession for the scale type
        tonesSuccession = self.Type.value

        refNote = Note(name=self.RefNote, octave=octave)

        # Reorganize tones_succession according to ScaleModess value (in different mode, tones_succession changes)
        tonesSuccession = (
            tonesSuccession[mode.value:]
            + tonesSuccession[:mode.value]
        )

        # Create the reference note for the scale wanted and get notes
        scaleNotes = [refNote]
        for toneDelta in tonesSuccession:
            scaleNotes.append(scaleNotes[-1] + int(toneDelta * 2))

        return scaleNotes

    def GetNotesNames(self, mode: str = "Ionian") -> List[str]:
        return [n.Name for n in self.GetScaleNotes(mode=mode)]

    # Implementing circle of fifths here
    def GetNeighbourScales(self) -> List[Scale]:
        return self.GetSameTypeNeighbours() + [self.GetDifferentTypeNeighbour()]

    def GetNeighbourScale(self, direction: int, scale_type: Union[str, Mode] = "Major") -> Scale:
        pass

    def GetSameTypeNeighbours(self) -> List[Scale]:
        # Minors and Majors have the same neighbours, but differentiating anyway
        if self.Type == Mode.Major:
            neighboursRefNotes = MAJOR_NEIGHBOURS[self.RefNote.name]
        else:
            neighboursRefNotes = MINOR_NEIGHBOURS[self.RefNote.name]
        return [
            Scale(ref_note=refNote, scale_type=self.Type)
            for refNote in neighboursRefNotes
        ]

    def GetDifferentTypeNeighbour(self) -> Scale:
        if self.Type == Mode.Major:
            return self.GetMinorFromMajorByRefNote(self.RefNote)
        else:
            return self.GetMajorFromMinorByRefNote(self.RefNote)

    @staticmethod
    def GetMinorFromMajorByRefNote(ref_note: str) -> Scale:
        return Scale(ref_note=MINOR_FROM_MAJOR[ref_note], scale_type="Minor")

    @staticmethod
    def GetMajorFromMinorByRefNote(ref_note: Union[str, NoteNames]) -> Scale:
        ref_note = NoteNames.SafeFromStr(ref_note)
        keys = list(MINOR_FROM_MAJOR.keys())
        for k in keys:
            if MINOR_FROM_MAJOR[k] == ref_note.name:
                return Scale(ref_note=k, scale_type="Major")
        raise KeyError("Scale - GetMajorFromMinorByRefNote - " + str(ref_note))

    def GetPentatonicNotes(
        self, octave: int = 5, mode: Union[str, ScaleModes] = "Ionian"
    ) -> List[Note]:
        mode = ScaleModes.SafeFromStr(mode)
        # Make use of GetScaleNotes method
        allScaleNotes = self.GetScaleNotes(octave=octave, mode=mode)

        # only keep notes where there is a difference of a whole tone
        # compared to previous in scale
        pentatonicScaleNotes = [allScaleNotes[0]]
        for idn in range(1, len(allScaleNotes)):
            if (allScaleNotes[idn] - allScaleNotes[idn - 1]) == 2:
                pentatonicScaleNotes.append(allScaleNotes[idn])

        # only 5 notes in pentatonic scale
        return pentatonicScaleNotes[:5]

    def GetNote(self, tone: int, octave: int, mode: str = "Ionian") -> Note:
        scale_notes = self.GetScaleNotes(octave, mode)
        note = scale_notes[tone % (len(scale_notes) - 1)]
        while tone >= len(scale_notes):
            note += 12
            tone -= len(scale_notes)
        return note


def ExtendScaleNotes(
    scale_notes: List[Note],
    extension_factor: Union[int, float],
    single_direction: bool = False,
    direction: str = "+",
) -> List[Note]:
    """
    Extend a list of note by a given factor by transposing them by N octaves.
    2 methods depending on type of extension factor:
        - if int, extension factor is the number of elements to be added
        - if float, extension factor is a percentage of length of scaleNotes to be added
    when passing a float, compute an int and recursively call ExtendScaleNotes
    """

    if type(extension_factor) == float:
        intExtensionFactor = int(extension_factor * len(scale_notes))
        return ExtendScaleNotes(
            scale_notes, intExtensionFactor, single_direction, direction
        )

    # ensure scaleNotes are sorted in ascending order
    scale_notes = sorted(scale_notes, key=lambda x: x.Height)

    directions = ["+", "-"]
    # Get number of elements
    if single_direction:
        directions = [direction]

    outScaleNotes = [n for n in scale_notes]
    for currDirection in directions:
        addedElements = 0
        refNotes = scale_notes
        nbOctaves = 1
        tonalDelta = 12
        if currDirection == "-":
            tonalDelta = -12
            # need to take order into account
            # if going down, pool note must be reversed
            refNotes = refNotes[::-1]

        while addedElements < extension_factor:
            for note in refNotes:
                if addedElements > extension_factor:
                    break
                outScaleNotes.append(note + nbOctaves * tonalDelta)
                addedElements += 1
            nbOctaves += 1

    # sort again and get rid of repeated notes
    outScaleNotes = sorted(outScaleNotes, key=lambda x: x.Height)
    return FilterOutRepeatedNotes(outScaleNotes)
