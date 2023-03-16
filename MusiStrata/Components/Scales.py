from typing import List, Union, TYPE_CHECKING
from typing_extensions import Self
from dataclasses import dataclass

from MusiStrata.Components.Notes import Note

from MusiStrata.Data.Scales import SCALE_CHORD_CODES, SCALE_TONES

from MusiStrata.Enums import (
    ScaleModes,
    NoteNames
)


if TYPE_CHECKING: 
    from MusiStrata.Components.Chords import Chord



"""
Major is Ionian, Minor is Aeolian
"""

@dataclass
class Scale:
    ref_note: NoteNames
    mode: ScaleModes

    def __init__(self, ref_note: Union[str, NoteNames], mode: Union[str, ScaleModes]) -> None:
        self.ref_note = NoteNames.SafeFromStr(ref_note)
        self.mode = ScaleModes.SafeFromStr(mode)

    def __str__(self):
        return "Scale({}-{})".format(self.ref_note.name, self.mode.name)

    def __repr__(self):
        return str(self) 

    def __eq__(self, other: Self):
        return self.ref_note == other.ref_note and self.mode == other.mode

    def get_note(self, index: int, octave: int = 5) -> Note:
        tones = SCALE_TONES[self.mode]
        base_note = Note(self.ref_note, octave)
        for id_tone in range(index):
            base_note += tones[id_tone]
        return base_note

    def get_notes(self, octave: int = 5) -> List[Note]:
        tones = SCALE_TONES[self.mode]
        notes = [Note(self.ref_note, octave)]
        for tone in tones:
            notes.append(
                notes[-1] + tone
            )
        return notes

    def get_note_names(self) -> List[NoteNames]:
        return [n.name for n in self.get_notes(5)]
    
    def get_scale_chord_codes(self) -> List[str]:
        return SCALE_CHORD_CODES[self.mode]
    
    def get_scale_chords(self) -> List["Chord"]:
        from MusiStrata.Components.Chords import Chord
        return [Chord(chord_code) for chord_code in self.get_scale_chord_codes()]

    def get_chord(self, chord_code: str, index: int = 0, octave: int = 5) -> List[Note]:
        return Chord(chord_code)(self.get_note(index, octave))
