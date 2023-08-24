from src.MusiStrata import Note, NoteNames, Chord



def test_major_chord():
    ch = Chord("M")
    ch(Note())


def test_minor_chord():
    ch = Chord("m")
    ch(Note())


def test_maj_seventh_chord():
    ch = Chord("M7")
    ch(Note())

