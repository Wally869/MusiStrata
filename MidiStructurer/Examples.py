from .Components import *
import .ScalesUtils as sc
import .MidoConverter as mc
import .CircleOfFifths as cof

from random import seed, choice
from copy import deepcopy
from os import path, mkdir

"""
Generate a single bar, single track song with predefined note heights and durations
"""
def GenerateExample1():
    note1 = Note(
        Beat=0.0,
        Duration=1.0,
        Octave=5,
        NoteName="A"
    )
    note2 = Note(
        Beat=2.0,
        Duration=1.0,
        Octave=5,
        NoteName="C"
    )
    note3 = Note(
        Beat=3.0,
        Duration=0.5,
        Octave=5,
        NoteName="D"
    )

    bar = Bar(
        Notes=[note1, note2, note3]
    )

    track = Track(
        Name="Main",
        Instrument="Vibraphone",
        Bars=[bar]
    )

    song = Song(
        Tracks=[track]
    )

    return song

"""
Generate a single track, 2 bars song by repeating a pattern bar
Note heights are set by randomly choosing among notes composing a given scale (here C# Major)
"""
def GenerateExample2():
    seed(42)

    note1 = Note(
        Beat=0.0,
        Duration=1.0,
        Octave=5
    )
    note2 = Note(
        Beat=2.0,
        Duration=1.0,
        Octave=5
    )
    note3 = Note(
        Beat=3.0,
        Duration=0.5,
        Octave=5
    )

    bar = Bar(
        [note1, note2, note3]
    )

    mainScale = Scale("C#", "Minor")
    # Get the notes in this scale
    allowedNotes = sc.GeneratePentatonicScaleNotesWithOctaveDelta(mainScale)
    for n in bar.Notes:
        chosenNote = choice(allowedNotes)
        n.NoteName = chosenNote["noteName"]
        n.Octave += chosenNote["octaveDelta"]

    track = Track(
        Bars=[bar, bar],
        Instrument="Acoustic Grand Piano"
    )

    song = Song(
        Tempo=150,
        Tracks=[track]
    )

    return song


"""
Generate a single track, 10 bars song. We use the same rythm for the bars, but 
choose different scales from each bar. 
Possible scales are selected from the Circle of Fifths, which means we select neighbour scales
Note heights are set by randomly choosing among notes composing a given scale
"""
def GenerateExample3():
    seed(42)

    note1 = Note(
        Beat=0.0,
        Duration=1.0,
        Octave=5
    )
    note2 = Note(
        Beat=2.0,
        Duration=1.0,
        Octave=5
    )
    note3 = Note(
        Beat=3.0,
        Duration=0.5,
        Octave=5
    )

    bar = Bar(
        [note1, note2, note3]
    )

    bars = [deepcopy(bar) for i in range(6)]

    mainScale = Scale("C#", "Minor")
    # Get scales neighbouring the mainScale
    allowedScales = cof.GetAllowedScales(mainScale)

    for b in bars:
        currScale = choice(allowedScales)
        # Get the notes in this scale
        allowedNotes = sc.GeneratePentatonicScaleNotesWithOctaveDelta(currScale)
        for n in b.Notes:
            chosenNote = choice(allowedNotes)
            n.NoteName = chosenNote["noteName"]
            n.Octave += chosenNote["octaveDelta"]

    track = Track(
        Bars=bars,
        Instrument="Acoustic Grand Piano"
    )

    song = Song(
        Tempo=60,
        Tracks=[track]
    )

    return song

ALL_EXAMPLES = [
    GenerateExample1,
    GenerateExample2,
    GenerateExample3
]


def RunExamples():
    if path.exists("Examples") == False:
        mkdir("Examples")
    print("Generating Examples in folder Examples")
    for id_example in range(len(ALL_EXAMPLES)):
        currSong = ALL_EXAMPLES[id_example]()
        mc.ConvertSong(currSong, "Examples/example-" + str(id_example + 1) + ".mid")
    print("Done")


if __name__ == "__main__":
    RunExamples()