---
layout: default
title: VelocityColorer
nav_order: 5
---

# VelocityColorer

## Overview

The VelocityColorer file implements the VelocityColorer Class, which enables control over the velocity of notes/sound events (aka the strength with which the note is played) depending which beats the sound event occurs.

This is a common feature of Music Performances: some Beats are accentuated. For example, a 4/4 piano piece would usually have emphasize the first beat and do another, smaller, emphasis on the 3rd beat. The Velocity Colorer enables us to set this kind of behaviour for a full track and or a bar.

## Usage

The Velocity Colorer class takes as input a dict of the following format:

```json
standardBeatColorer = {
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
```

Beats are classified as belonging to a certain tag, and each tag has a specified multiplier which will be applied to the velocity of a sound event.  

The VelocityColorer object can then be applied to a Track, or a Bar, and will adjust the velocity according to a reference velocity.

```python
def PrepareTrack(self, track: Track, refVelocity: int = 60) -> None
def PrepareBar(self, inputBar: Bar, refVelocity: int = 60) -> Bar
```

Considering the StandardBeatColorer we defined above and a reference Velocity of 60, this means a SoundEvent on beat 0.0 would end up with a Velocity of 72, a SoundEvent on beat 2.0 with a Velocity of 66 while all others would get a 60.  

## ColorerLibrary  

Some preset colorers will be available from the ColorerLibrary, and can access by name. Most notably the Standard Colorer is accessible through the Standard property.  

```python
# See Internals/PrimitiveClassesUtils for details on the Library Class

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
```

Other colorers will be added and we'll make it more convenient to implement custom VelocityCOlorers.