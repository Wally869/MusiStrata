from __future__ import annotations
from typing import List, Tuple, Dict, Union

from MusiStrata.Components import Note
from MusiStrata.Structure import Bar, Track, Song
import numpy as np
from scipy import signal
import soundfile

from MusiStrata.Interfaces import IRenderer

from .Utils import SaveBarsToSineArray

class WavRenderer(IRenderer):
    @classmethod
    def Render(cls, song: Song, outfile: str, sample_rate: int):
        ConvertSong(song, outfile, sample_rate)


def ConvertSong(song: Song, outfile: str, sample_rate: int):
    tracks = [
        SaveBarsToSineArray(track.Bars, song.BeatsPerBar, song.Tempo, sample_rate)
        for track in song.Tracks
    ]    
    output = np.zeros_like(tracks[0])
    for track in tracks:
        output += track
    output /= np.max(output)
    output *= 0.5
    soundfile.write(outfile, output, sample_rate, "PCM_24")




