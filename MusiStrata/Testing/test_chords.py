from MusiStrata import Note, Chord


def test_from_base_extensions():
    n = Note("C", 5)
    maj_triad = Chord.FromBaseExtensions("Major")
    notes, err = n + maj_triad
    assert notes == [Note("C", 5), Note("E", 5), Note("G", 5)]

