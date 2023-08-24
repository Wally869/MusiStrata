from MusiStrata import Scale
from MusiStrata.Data.Scales import ALL_SCALE_MODES

def test_create_all_scales():
    for sc_name in ALL_SCALE_MODES:
        sc = Scale("C", sc_name)


def test_create_notes():
    for sc_name in ALL_SCALE_MODES:
        sc = Scale("C", sc_name)
        sc.get_notes()
        for i in range(8):
            sc.get_note(i)


def test_get_chord():
    for sc_name in ALL_SCALE_MODES:
        sc = Scale("C", sc_name)
        for i in range(8):
            sc.get_chord("M", i)
            sc.get_chord("m", i)
            sc.get_chord("A", i)
            sc.get_chord("d", i)

