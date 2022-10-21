from MusiStrata.Components import *
from MusiStrata.Rendering import Render, RenderFormats
from MusiStrata.Enums import ChordExtension as CE

from random import seed, choice
from copy import deepcopy
from os import path, mkdir

from random import choice

from Utils import invert

CHORD_PROGRESSION = [0, 4, 5, 3]

from MusiStrata import ScaleChordExtension as SCE

def GenerateExample1():
    sc = Scale("C", "Major")
    extensions = [[CE.m7], [CE.m7], [CE.m9], [CE.m7], [CE.P11], [CE.m7], [CE.m7]]
    extensions = [choice([SCE.Seventh, SCE.Ninth]) for i in range(7)]
    #extensions = ["Seventh" for _ in range(7)]
    sc_chords = sc.GetChords(extensions=extensions)

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


def GenerateExample2():
    sc = Scale("C", "Major")
    progression = [0, 2, 4, 0]
    bars = []
    for currID in progression:
        notes = Chord.FromScaleTones([currID, currID + 2, currID + 4], 5, sc)
        if currID == 4:
            notes = invert(notes, 2)
            notes = [note - 12 for note in notes]        
        barNotes = [SoundEvent(0.0, 4.0, n) for n in notes]
        bars.append(Bar(barNotes))
    track = Track(Bars=bars, Instrument="Acoustic Grand Piano")
    song = Song(Tempo=120, Tracks=[track])
    Render(song, "Examples/example2-v2.mid", RenderFormats.MIDI)

#GenerateExample1()
GenerateExample2()
