---
layout: default
title: ScaleSpecs
parent: Components
nav_order: 2
---

# ScaleSpecs 

## Overview  

A ScaleSpecs object allows to generate Scales, aka List of Notes, according to presets.

It also implements methods to find neighbouring Scales [using the Circle of Fifths theory.](https://en.wikipedia.org/wiki/Circle_of_fifths)


## Creating and Using a ScaleSpecs Object

```python
"""
class ScaleSpecs(object):
    def __init__(self, RefNote: str = "A", ScaleType: str = "Major"):
        self.RefNote = RefNote
        self.Type = ScaleType
"""

# Defaults to A-Major
>> ScaleSpecs()
ScaleSpecs(A-Major)

>> sc = ScaleSpecs(RefNote="A", ScaleType="Major")
ScaleSpecs(A-Major)

# Get A-Major Notes using the GetScaleNotes method
# can supply a referenceOctave parameter. Default is 5
>> sc.GetScaleNotes(referenceOctave=5)
[Note(A5), Note(B5), Note(Cs6), Note(D6), Note(E6), Note(Fs6), Note(Gs6), Note(A6)]

# It also possible to generate a scale using modes other than Ionian
>> sc.GetScaleNotes(referenceOctave=4, mode="Phrygian")
[Note(A4), Note(As4), Note(C5), Note(D5), Note(E5), Note(F5), Note(G5), Note(A5)]

# Similarly, can generate pentatonic scales
>> sc.GetPentatonicScaleNotes(referenceOctave=5)
[Note(A5), Note(B5), Note(Cs6), Note(Ds6), Note(F6), Note(G6)]
# and from specific modes
>> sc.GetPentatonicScaleNotes(referenceOctave=4, mode="Mixolydian")
[Note(A4), Note(B4), Note(Cs5), Note(E5), Note(Fs5)]

```

The ScaleSpecs class also implements methods to find neighboring scales according to the Circle of Fifth theory

```python
# Find all neighbouring scales of the same type (Major or Minor)
>> sc.GetSameTypeNeighbours()
[ScaleSpecs(D-Major), ScaleSpecs(E-Major)]

# can also find the neighbouring minor from a major scale, and vice versa
>> sc.GetDifferentTypeNeighbour()
ScaleSpecs(Fs-Minor)

# Get all neighbours
>> sc.GetNeighbouringScales()
[ScaleSpecs(D-Major), ScaleSpecs(E-Major), ScaleSpecs(Fs-Minor)]
```