from __future__ import annotations
from typing import List, Tuple, Dict, Union

from random import choice


def ComputeLengthSong(nbBeatsPerBar: int, nbBars: int, tempo: int):
    """
    Outputs song length in seconds
    """
    # tempo is number of beats per minute so easy calculation
    return (nbBeatsPerBar * nbBars) / tempo * 60


# Instead of iterating, could find from closed form equation
# I'll do it later I guess
def FindListNbBarsFromConstraints(nbBeatsPerBar: int, tempo: int, minLenSong: float, maxLenSong: float) -> List[int]:
    """
    minLenSong and maxLenSong in seconds
    """

    possibilities = []
    nbBars = 1
    while True:
        lenSong = ComputeLengthSong(nbBeatsPerBar, nbBars, tempo)
        if lenSong > maxLenSong:
            break
        elif minLenSong <= lenSong <= maxLenSong:
            possibilities.append(nbBars)
        nbBars += 1
    return possibilities


def FindRandomNbBarsFromConstraints(nbBeatsPerBar: int, tempo: int, minLenSong: float, maxLenSong: float):
    return choice(FindListNbBarsFromConstraints(nbBeatsPerBar, tempo, minLenSong, maxLenSong))
