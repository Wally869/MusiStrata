

from random import choice


def ComputeLengthSong(nbBeatsPerBar, nbBars, tempo):
    """
    Outputs song length in seconds
    """
    # tempo is number of beats per minute so easy calculation
    return (nbBeatsPerBar * nbBars) / tempo * 60


# Instead of iterating, could find from closed form equation
# I'll do it later I guess
def FindListNbBarsFromConstraints(nbBeatsPerBar, tempo, minLenSong, maxLenSong):
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


def FindRandomNbBarsFromConstraints(nbBeatsPerBar, tempo, minLenSong, maxLenSong):
    return choice(FindListNbBarsFromConstraints(nbBeatsPerBar, tempo, minLenSong, maxLenSong))
