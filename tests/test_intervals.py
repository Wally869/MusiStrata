#from MusiStrata import Interval, Note

from src.MusiStrata import Note, NoteNames
from src.MusiStrata.Components.Intervals import Interval


def test_base_interval():
    temp = Interval("P1")
    rslt = Note() + temp
    assert rslt == Note()


def test_known_intervals_minor_major_perfect():
    known_intervals = [
        "P1", "m2", "M2", "m3", "M3", "P4", "P5", "m6", "M6", "m7", "M7", "P8"
    ]
    for known_interval in known_intervals:
        temp = Interval(known_interval)

def test_known_intervals_augmented_diminished():
    known_intervals = [
        "d2", "A1", "d3", "A2", "d4", "d5", "A4", "d6", "A5", "d7", "A6", "d8", "A7"
    ]
    for known_interval in known_intervals:
        temp = Interval(known_interval)
        n = Note() + temp


def test_big_intervals_ninths():
    temp = Interval("m9")
    n = Note()
    n2 = n + temp
    assert n2.name == NoteNames.Cs and n2.octave == n.octave + 1
    temp = Interval("M9")
    n = Note()
    n2 = n + temp
    assert n2.name == NoteNames.D and n2.octave == n.octave + 1

