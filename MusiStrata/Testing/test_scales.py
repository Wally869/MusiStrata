from MusiStrata import Scale
from MusiStrata.Enums import ChordExtension, NoteNames, ScaleModes

def test_create_scale():
    sc = Scale("A", "Major")
    sc2 = Scale("A", "Minor")


def test_get_pentatonic_notes():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                sc = Scale(note_name, scale_type)
                notes = sc.GetPentatonicNotes(5, scale_mode)    


def test_get_scale_notes():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                sc = Scale(note_name, scale_type)
                notes = sc.GetScaleNotes(5, scale_mode)


def test_get_single_chord_no_extensions():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                for i in range(7):
                    sc = Scale(note_name, scale_type)
                    chords = sc.GetSingleChord(tone=i, mode=scale_mode)


def test_get_chords_no_extensions():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                sc = Scale(note_name, scale_type)
                chords = sc.GetChords(mode=scale_mode)


def test_get_chords_notes_no_extensions():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                sc = Scale(note_name, scale_type)
                chords = sc.GetChordsNotes(mode=scale_mode)


def test_get_chords_with_single_extension():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                for extension in ChordExtension:
                    sc = Scale(note_name, scale_type)
                    chords = sc.GetChords(mode=scale_mode, extensions=[[extension] for i in range(7)])


def test_get_chords_with_multiple_extensions():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            for scale_mode in ScaleModes:
                sc = Scale(note_name, scale_type)
                chords = sc.GetChords(mode=scale_mode, extensions=[list(ChordExtension) for i in range(7)]) 


def test_get_single_chord_notes():
    for scale_type in ["Minor", "Major"]:
        for note_name in NoteNames:
            sc = Scale(note_name, scale_type)
            for i in range(7):
                for sc_mode in ScaleModes:
                    for extension in ["Seventh", "Ninth", "Eleventh", "Thirteenth"]:
                        chord = sc.GetSingleChord(tone=i, extensions=[extension], mode=sc_mode)
                        notes = sc.GetSingleChordNotes(tone=i, octave=5, extensions=[extension], mode=sc_mode)

