from __future__ import annotations
from typing import List, Tuple, Dict, Union

from MusiStrata.Components import Note, Bar
import soundcard as sc
import numpy as np
from scipy import signal


# Alias for typeStripper
npNdarray = np.ndarray


DEFAULT_SPEAKER = sc.default_speaker()


def PlayNotes(notes: Union[List[Note], Note], sampleRate: int = 10000) -> None:
    if type(notes) == Note:
        return PlayNotes([notes])
    deltaTimes = np.arange(sampleRate) / sampleRate
    output = np.zeros(len(deltaTimes))
    for n in notes:
        # use triangle waves
        # output += 0.5 * (2/np.pi) * np.arcsin(np.sin(deltaTimes * 2 * np.pi * n.Frequency))
        output += 0.25 * np.sin(deltaTimes * 2 * np.pi * n.Frequency)
    DEFAULT_SPEAKER.play(output, sampleRate)


def PlayBar(
    bar: Bar, nbBeatsInBar: int = 4, sampleRate: int = 10000, tempo: int = 60
) -> None:
    deltaTimes = np.arange(int(sampleRate * nbBeatsInBar * 60 / tempo)) / sampleRate
    output = np.zeros(len(deltaTimes))
    for se in bar.SoundEvents:
        idStartSound = int(se.Beat * sampleRate * 60 / tempo)
        idEndSound = int(idStartSound + (se.Duration * sampleRate) * 60 / tempo) - 1
        output[idStartSound:idEndSound] += 0.25 * np.sin(
            deltaTimes[idStartSound:idEndSound] * 2 * np.pi * se.Note.Frequency
        )
    DEFAULT_SPEAKER.play(output, sampleRate)


def SaveBarsToSineArray(
    bars: List[Bar], nbBeatsInBar: float = 4.0, sampleRate: int = 10000, tempo: int = 60
) -> List[npNdarray, int]:
    deltaTimes = (
        np.arange(int(sampleRate * nbBeatsInBar * len(bars) * 60 / tempo)) / sampleRate
    )
    output = np.zeros(len(deltaTimes))
    for idB, b in enumerate(bars):
        for se in b.SoundEvents:
            idStartSound = int(
                idB * nbBeatsInBar * sampleRate * 60 / tempo
                + se.Beat * sampleRate * 60 / tempo
            )
            idEndSound = int(idStartSound + (se.Duration * sampleRate) * 60 / tempo) - 1
            output[idStartSound:idEndSound] += 0.25 * np.sin(
                deltaTimes[idStartSound:idEndSound] * 2 * np.pi * se.Note.Frequency
            )
    return output, sampleRate


def PlayBars(
    bars: List[Bar], nbBeatsInBar: float = 4.0, tempo: int = 60, sampleRate: int = 10000
) -> None:
    arr, _ = SaveBarsToSineArray(bars, nbBeatsInBar, sampleRate, tempo)
    DEFAULT_SPEAKER.play(arr, sampleRate)
