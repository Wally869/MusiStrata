from __future__ import annotations

from .Components import *
import soundcard as sc
import numpy as np
from scipy import signal

from typing import List, Union

DEFAULT_SPEAKER = sc.default_speaker()

def PlayNotes(notes: Union[List[Note], Note], sampleRate: int = 10000):
    if type(notes) == Note:
        return PlayNotes([notes])
    deltaTimes = np.arange(sampleRate) / sampleRate
    output = np.zeros(len(deltaTimes))
    for n in notes:
        # use triangle waves
        #output += 0.5 * (2/np.pi) * np.arcsin(np.sin(deltaTimes * 2 * np.pi * n.Frequency))
        output += 0.25 * np.sin(deltaTimes * 2 * np.pi * n.Frequency)
    DEFAULT_SPEAKER.play(output, sampleRate)


def PlayBar(bar: Bar, nbBeatsInBar: int = 4, sampleRate: int = 10000):
    deltaTimes = np.arange(sampleRate * nbBeatsInBar) / sampleRate
    output = np.zeros(len(deltaTimes))
    for se in bar.SoundEvents:
        idStartSound = int(se.Beat * sampleRate)
        idEndSound = idStartSound + (se.Duration * sampleRate)
        output[idStartSound:idEndSound] += 0.25 * np.sin(deltaTimes[idStartSound:idEndSound] * 2 * np.pi * se.Note.Frequency)
    DEFAULT_SPEAKER.play(output, sampleRate)
