from typing import List

from MusiStrata.Components import Song, Note, Bar

from enum import Enum


class RenderFormats(Enum):
    MIDI = 0
    LMMS = 1
    WAV = 2
    LILYPOND = 3
    ABC = 4


def Render(song: Song, outfile: str, format: RenderFormats, **kwargs):
    match format:
        case RenderFormats.MIDI:
            from .MidiRenderer import MidiRenderer
            MidiRenderer.Render(song, outfile)
        case RenderFormats.LMMS:
            raise NotImplementedError("Rendering - Format Not Implemented: LMMS")
        case RenderFormats.WAV:
            from .WavRenderer import WavRenderer
            WavRenderer.Render(song, outfile, kwargs.get("sample_rate", 20000))
        case RenderFormats.LILYPOND:
            raise NotImplementedError("Rendering - Format Not Implemented: LILYPOND")
        case RenderFormats.ABC:
            raise NotImplementedError("Rendering - Format Not Implemented: ABC")
        case _:
            raise ValueError("Render - Invalid Format")


def Play(element, nbBeatsInBar: int = 4, sampleRate: int = 16000, tempo: int = 60):
    played = False
    if type(element) is Note or (type(element) is list and type(element[0]) is Note):
        from .NotePlayer import PlayNotes

        PlayNotes(element, sampleRate)
        played = True
    elif type(element) is Bar:
        element = [element]
    if type(element) is list and type(element[0]) is Bar:
        from .NotePlayer import PlayBars

        PlayBars(element, nbBeatsInBar, sampleRate, tempo)
        played = True
    if not played:
        raise NotImplementedError("Play - Type Not Supporter: {}".format(type(element)))
