from MusiStrata.Components import *
from MusiStrata.Rendering import Render, RenderFormats
from MusiStrata.Enums import ChordExtension as CE

from random import seed, choice
from copy import deepcopy
from os import path, mkdir


CHORD_PROGRESSION = [0, 4, 5, 3]


def GenerateExample1():
    sc = Scale("C", "Major")
    extensions = [None, CE.m7, CE.m9, CE.m7, [CE.P11], None, None]
    sc_chords = sc.GetChordsProgression(extensions=extensions)
    sc_notes = sc.GetScaleNotes(4)

    bars = []
    for currID in CHORD_PROGRESSION:
        indices = [(0, 0), (1, -1), (0, 2)]
        if len(sc_chords[currID]) == 4:
            indices = [(0, 0), (1, -1), (2, 0), (3, -1)]
        notes = sc.GetSingleChordNotes(currID, 5, extensions, indices)
        barNotes = [SoundEvent(0.0, 4.0, n) for n in notes]
        bars.append(Bar(barNotes))

    track = Track(Bars=bars, Instrument="Acoustic Grand Piano")

    song = Song(Tempo=120, Tracks=[track])

    Render(song, "Examples/example-v2.mid", RenderFormats.MIDI)
