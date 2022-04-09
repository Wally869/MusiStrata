
from MusiStrata import Note

def test_note_init():
    n = Note("A", 5)
    assert n.Name == "A"
    assert n.Octave == 5
    n2 = Note("C", 3)
    assert n2.Name == "C"
    assert n2.Octave == 3

def test_set_octave():
    n = Note("A", 5)
    assert n.Octave == 5
    n.Octave = 3
    assert n.Octave == 3

def test_equal():
    n = Note("B", 4)
    n2 = Note("B", 4)
    assert n == n2

def test_math():
    n = Note("B", 4)
    assert n + 12 - 12 == n
    n2 = Note("E", 5)
    assert n + 5 == n2

def test_comparisons():
    n = Note("A", 5)
    n2 = n + 5
    assert n < n2
    assert n2 > n
    assert n <= n2
    assert n2 >= n    
    n3 = Note("A", 5)
    assert not n > n3
    assert not n < n3
    assert n == n3
    assert n >= n3
    assert n <= n3

def test_tonal_distance():
    n = Note("A", 5)
    n2 = n + 5
    assert n.GetTonalDistance(n2) == -5
    assert n.GetRootedTonalDistance(n2) == 5

def test_interval_number():
    n = Note("B", 4)
    n2 = Note("E", 5)
    assert n.GetIntervalNumber(n2)

def test_from_value():
    n = Note("A", 4)
    height_note = n.Height
    n2 = Note.FromHeight(height_note)
    assert n == n2

