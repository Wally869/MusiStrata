from MusiStrata import Interval, Note


def test_interval_from_interval_number_and_quality():
    i = Interval(4, "Perfect")
    assert True

def test_interval_from_intervals():
    i = Interval(4, "Perfect")
    i2 = Interval(Intervals=[i])
    assert True

def test_interval_equality():
    i = Interval(4, "Perfect")
    i2 = Interval(4, "Perfect")
    i3 = Interval(Intervals=[i])
    assert i == i2
    assert i == i3

def test_interval_addition():
    n = Note("A", 5)
    n2, err = n + Interval(8, "Perfect")
    assert n2 == Note("A", 6)
    assert err is None

def test_interval_from_notes():
    n = Note("A", 5)
    n2 = Note("A", 6)
    i = Interval.FromNotes(n, n2)
    assert i == Interval(8, "Perfect")

