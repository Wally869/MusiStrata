from MusiStrata import Note, Chord


def test_from_base_extensions():
    n = Note("C", 5)
    maj_triad = Chord.FromBaseExtensions("Major")
    notes, err = n + maj_triad
    assert notes == [Note("C", 5), Note("E", 5), Note("G", 5)]



from MusiStrata.Enums import NoteNames
from MusiStrata import Note, Chord, Scale
from MusiStrata.Components import *

from MusiStrata.Utils.Functions import MinimizeDistance

def test_minimize_distance():
    sc = Scale("A", "Major")
    tones = [0, 4, 5, 3]

    chords = [sc.GetSingleChord(t) for t in tones]
    sc_notes = [sc.GetScaleNotes(4)[t] for t in tones]

    notes_1, err1 = chords[0](sc_notes[0], [(0, 0), (1, 0), (2, 0)])
    notes_2, err2 = chords[1](sc_notes[1], [(0, 0), (1, 0), (2, 0)])

    notes_1 += [Note("B", 5)]

    out_notes = MinimizeDistance(notes_1, notes_2, False)

