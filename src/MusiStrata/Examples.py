from MusiStrata.Structure import *
from MusiStrata.Components import *
from MusiStrata.Rendering import Render, RenderFormats

from random import seed, choice
from copy import deepcopy
from os import path, mkdir


def GenerateExample1():
    """
    Generate a single bar, single track song with predefined note heights and durations
    """
    note1 = SoundEvent(
        Beat=0.0,
        Duration=1.0,
        Note=Note(
            name="A",
            octave=5,
        ),
    )
    note2 = SoundEvent(
        Beat=2.0,
        Duration=1.0,
        Note=Note(
            name="C",
            octave=5,
        ),
    )
    note3 = SoundEvent(
        Beat=3.0,
        Duration=0.5,
        Note=Note(
            name="D",
            octave=5,
        ),
    )

    bar = Bar(SoundEvents=[note1, note2, note3])

    track = Track(Name="Main", Instrument="Vibraphone", Bars=[bar], BankUsed=1)

    song = Song(Tracks=[track])

    return song


def GenerateExample2():
    """
    Generate a single track, 2 bars song by repeating a pattern bar
    Note heights are set by randomly choosing among notes composing a given scale (here C# Major)
    """
    seed(42)

    note1 = SoundEvent(
        Beat=0.0,
        Duration=1.0,
        Note=Note(
            name="A",
            octave=5,
        ),
    )
    note2 = SoundEvent(
        Beat=2.0,
        Duration=1.0,
        Note=Note(
            name="C",
            octave=5,
        ),
    )
    note3 = SoundEvent(
        Beat=3.0,
        Duration=0.5,
        Note=Note(
            name="D",
            octave=5,
        ),
    )

    bar = Bar([note1, note2, note3])

    mainScale = Scale("Cs", "Minor")
    # Get the notes in this scale
    allowedNotes = mainScale.GetScaleNotes()
    for e in bar.SoundEvents:
        e.Note = choice(allowedNotes)

    track = Track(Bars=[bar, bar], Instrument="Acoustic Grand Piano")

    song = Song(Tempo=150, Tracks=[track])

    return song


def GenerateExample3():
    """
    Generate a single track, 10 bars song. We use the same rythm for the bars, but
    choose different scales from each bar.
    Possible scales are selected from the Circle of Fifths, which means we select neighbour scales
    Note heights are set by randomly choosing among notes composing a given scale
    """
    seed(42)

    note1 = SoundEvent(Beat=0.0, Duration=1.0, Note=Note(octave=5))
    note2 = SoundEvent(Beat=2.0, Duration=1.0, Note=Note(octave=5))
    note3 = SoundEvent(Beat=3.0, Duration=0.5, Note=Note(octave=5))

    bar = Bar([note1, note2, note3])

    bars = [deepcopy(bar) for i in range(6)]

    mainScale = Scale("Cs", "Minor")
    # Get scales neighbouring the mainScale
    allowedScales = mainScale.GetNeighbourScales()

    for b in bars:
        currScale = choice(allowedScales)
        # Get the notes in this scale
        allowedNotes = currScale.GetScaleNotes()
        for e in b.SoundEvents:
            e.Note = choice(allowedNotes)

    track = Track(Bars=bars, Instrument="Acoustic Grand Piano")

    song = Song(Tempo=60, Tracks=[track])

    return song


ALL_EXAMPLES = [GenerateExample1, GenerateExample2, GenerateExample3]


def RunExamples():
    if not path.exists("Examples"):
        mkdir("Examples")
    print("Generating Examples in folder Examples")
    for id_example in range(len(ALL_EXAMPLES)):
        currSong = ALL_EXAMPLES[id_example]()
        Render(
            currSong,
            "Examples/example-" + str(id_example + 1) + ".mid",
            RenderFormats.MIDI,
        )
    print("Done")


if __name__ == "__main__":
    RunExamples()
