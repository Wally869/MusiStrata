from __future__ import annotations
from typing import List, Tuple, Dict, Union

from .Components import *
from .PrimitiveClassesUtils import Record, Library


class VelocityColorer(object):
    """
    This is based on the DrumsBeatColorer class in MidiGenerator

    Example Input
    {
        "Name": "Standard",
        "BeatsDecomposition": {
            "Primary": 0.0,
            "Secondary": 2.0
        },
        "BeatMultipliers": {
            "Primary": 1.1
            "Secondary": 1.0
            "Default": 0.9
        }
    }
    """

    def __init__(self, specs: Dict):
        # Dicts are mutable so DO NOT SET THEM as cls property
        self.BeatsValueToBeatsClassified = {}
        self.DrumsInstruments = {}

        self.BeatMultipliers = specs["BeatMultipliers"]
        self.SetBeatsDecomposition(specs["BeatsDecomposition"])

    def SetBeatsDecomposition(self, beatsDecomposition: Dict) -> None:
        """
            beatsDecomposition in the specs json to be input maps keys to arrays of beats, to make it easy
            to specify new presets for the user.
            Here we reverse this: a beat can be both primary and secondary, and more depending on the specs
            So we create a new dict using the beat as key, and its classifications in an array
            Example:
            {
            "Primary": [0.0],
            "Secondary": [0.0, 2.0]
            }
            will become:
            {
            0.0: ["Primary", "Secondary"],
            2.0: ["Secondary"]
            }
            NOTE: 0.0 and 0 are considered the same thing when used as key in a dict
        """
        self.BeatsValueToBeatsClassified = {}
        for key in list(beatsDecomposition.keys()):
            val = beatsDecomposition[key]
            self.BeatsValueToBeatsClassified[val] = key

    def CheckMultiplierForBeat(self, beat: float) -> int:
        """
        get the multiplier to be associated with a given beat
        """
        if beat in list(self.BeatsValueToBeatsClassified.keys()):
            outMultiplier = self.BeatsValueToBeatsClassified[beat]
        else:
            outMultiplier = "Default"

        return outMultiplier

    def PrepareBar(self, inputBar: Bar, refVelocity: int = 60) -> Bar:
        newBar = Bar()
        for se in inputBar.SoundEvents:
            newSoundEvent = se
            newSoundEvent.Velocity = int(refVelocity * self.BeatMultipliers[self.CheckMultiplierForBeat(se.Beat)])
            newBar.SoundEvents.append(newSoundEvent)

        return newBar

    def PrepareTrack(self, track: Track, refVelocity: int = 60) -> None:
        """
        Set drums instruments to notes, depending on beat
        """
        newBars = []
        for bar in track.Bars:
            newBars.append(
                self.PrepareBar(
                    bar, refVelocity=refVelocity
                )
            )

        track.Bars = newBars


specsStandard = {
    "Name": "Standard",
    "BeatsDecomposition": {
        "Primary": 0.0,
        "Secondary": 2.0
    },
    "BeatMultipliers": {
        "Primary": 1.2,
        "Secondary": 1.1,
        "Default": 1.0,
    }
}

StandardColorer = VelocityColorer(specsStandard)

class ColorerLibraryClass(Library):
    BaseName: str = "ColorerLibrary"
    Records: List[Record] = None

    def GetColorerFromName(self, nameColorer: str = "Standard") -> str:
        return self.GetFromValueInField("Name", nameColorer)[0].Colorer

    def Get(self, nameColorer: str = "Standard") -> str:
        return self.GetFromValueInField("Name", nameColorer)[0].Colorer

    @property
    def Standard(self):
        return self.Get("Standard")


ColorerLibrary = ColorerLibraryClass([{
    "Name": "Standard",
    "Colorer": StandardColorer
}])
