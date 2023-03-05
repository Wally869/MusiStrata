from MusiStrata.Components import *
from MusiStrata.Rendering import Render, RenderFormats

from random import seed, choice

from Utils import invert

CHORD_PROGRESSION = [0, 4, 5, 3]



def GenerateExample2():
    sc = Scale("C", "Major")
    progression = [0, 2, 4, 0]
    bars = []
    for currID in progression:
        chord = Chord("m7")
        notes = chord(sc.get_note(currID, 5))
        if currID == 4:
            notes = invert(notes, 2)
            notes = [note - 12 for note in notes]        
        barNotes = [SoundEvent(0.0, 4.0, n) for n in notes]
        bars.append(Bar(barNotes))
    track = Track(Bars=bars, Instrument="Acoustic Grand Piano")
    song = Song(Tempo=120, Tracks=[track])
    Render(song, "Examples/example2-v2.mid", RenderFormats.MIDI)


def GenerateExample3():
    sc = Scale("C", "Major")
    progression = [0, 2, 4, 0]
    bars = []
    for currID in progression:
        root_note = sc.get_note(currID, 5)
        notes = Chord("m7" if currID != 2 else "M7")(root_note - 12, 2)
        barNotes = [SoundEvent(0.0, 4.0, n) for n in notes]
        bars.append(Bar(barNotes))
    track = Track(Bars=bars, Instrument="Acoustic Grand Piano")
    song = Song(Tempo=120, Tracks=[track])
    Render(song, "Examples/example3-v2.mid", RenderFormats.MIDI)
    Render(song, "Examples/example3-v2.wav", RenderFormats.WAV)
    #PlayBars(track.Bars)

def GenerateExample4():
    sc = Scale("C", "Major")
    progression = [0, 2, 4, 0]
    chords = Scale.get_scale_chords(sc)
    bars = []
    for currID in progression:
        root_note = sc.get_note(currID, 5)
        notes = chords[currID](root_note)
        if currID == 4:
            notes = invert(notes, 2)
            notes = [note - 12 for note in notes]    
        elif currID == 2:
            notes = invert(notes, 2)
            notes = [note - 12 for note in notes]   
        barNotes = [SoundEvent(0.0, 4.0, n) for n in notes]
        bars.append(Bar(barNotes))
    bass_track = Track(Bars=bars, Instrument="Acoustic Grand Piano")

    bars = []
    for currID in progression:
        root_note = sc.get_note(currID, 6)
        notes = chords[currID](root_note)
        barNotes = [SoundEvent(i, 1.0, choice(notes)) for i in range(4)]
        bars.append(Bar(barNotes))
    melody_track = Track(Bars=bars, Instrument="Acoustic Grand Piano")
    song = Song(Tempo=120, Tracks=[melody_track, bass_track])
    Render(song, "Examples/example4-v2.mid", RenderFormats.MIDI)

#GenerateExample1()
GenerateExample2()
GenerateExample3()
GenerateExample4()