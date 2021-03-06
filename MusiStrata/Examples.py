from MusiStrata.Components import *
import MusiStrata.MidoConverter as mc

from random import seed, choice
from copy import deepcopy
from os import path, mkdir

"""
Generate a single bar, single track song with predefined note heights and durations
"""


def GenerateExample1():
    note1 = SoundEvent(
        Beat=0.0,
        Duration=1.0,
        Note=Note(
            Name="A",
            Octave=5,
        )
    )
    note2 = SoundEvent(
        Beat=2.0,
        Duration=1.0,
        Note=Note(
            Name="C",
            Octave=5,
        )
    )
    note3 = SoundEvent(
        Beat=3.0,
        Duration=0.5,
        Note=Note(
            Name="D",
            Octave=5,
        )
    )

    bar = Bar(
        SoundEvents=[note1, note2, note3]
    )

    track = Track(
        Name="Main",
        Instrument="Vibraphone",
        Bars=[bar],
        BankUsed=1
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

    note1 = SoundEvent(
        Beat=0.0,
        Duration=1.0,
        Note=Note(
            Name="A",
            Octave=5,
        )
    )
    note2 = SoundEvent(
        Beat=2.0,
        Duration=1.0,
        Note=Note(
            Name="C",
            Octave=5,
        )
    )
    note3 = SoundEvent(
        Beat=3.0,
        Duration=0.5,
        Note=Note(
            Name="D",
            Octave=5,
        )
    )

    bar = Bar(
        [note1, note2, note3]
    )

    mainScale = ScaleSpecs("Cs", "Minor")
    # Get the notes in this scale
    allowedNotes = mainScale.GetScaleNotes()
    for e in bar.SoundEvents:
        e.Note = choice(allowedNotes)

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

    note1 = SoundEvent(
        Beat=0.0,
        Duration=1.0,
        Note=Note(Octave=5)
    )
    note2 = SoundEvent(
        Beat=2.0,
        Duration=1.0,
        Note=Note(Octave=5)
    )
    note3 = SoundEvent(
        Beat=3.0,
        Duration=0.5,
        Note=Note(Octave=5)
    )

    bar = Bar(
        [note1, note2, note3]
    )

    bars = [deepcopy(bar) for i in range(6)]

    mainScale = ScaleSpecs("Cs", "Minor")
    # Get scales neighbouring the mainScale
    allowedScales = mainScale.GetNeighbouringScales()

    for b in bars:
        currScale = choice(allowedScales)
        # Get the notes in this scale
        allowedNotes = currScale.GetScaleNotes()
        for e in b.SoundEvents:
            e.Note = choice(allowedNotes)

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
    if not path.exists("Examples"):
        mkdir("Examples")
    print("Generating Examples in folder Examples")
    for id_example in range(len(ALL_EXAMPLES)):
        currSong = ALL_EXAMPLES[id_example]()
        mc.ConvertSong(currSong, "Examples/example-" + str(id_example + 1) + ".mid")
    print("Done")


if __name__ == "__main__":
    RunExamples()
