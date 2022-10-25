from typing import List, Tuple
import numpy as np

from MusiStrata.Components import Bar

def SaveBarsToSineArray(
    bars: List[Bar], nbBeatsInBar: float = 4.0, tempo: int = 60, sampleRate: int = 10000
) -> np.ndarray:
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
    return output
