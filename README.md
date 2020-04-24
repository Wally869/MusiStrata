# MidiStructurer

## Overview

Classes and Utilities for representing Notes and performing transformations on them with the intent of creating midi files.

In this library I strive to implement some basic concepts of Music Theory, to serve as base for a music generation package.
This is still a WIP, but the main operations are well defined and future work will likely only be extensions.

This readme is a quick overview of the main functions of this library. Extended explanations can be found in the wiki (WIP).

See the following sections for usage documentation (WIP). 
This library serves as base for my music generation project: https://github.com/Wally869/MidiGenerator

## Installing

```shell script
git clone https://github.com/Wally869/MidiStructurer.git
cd MidiStructurer
pip install -e .
```

## Examples

See Examples.py for some quick implementation examples.
You can also run Examples.py, and listen to the generated samples in the Examples folder.

## Dependencies

Written in python, the only dependency is Mido (https://github.com/mido/mido)


## Components

### Note Class

A note can be created easily, with 2 parameters: the note name, and the octave. 
Valid Note Names are letters A to G.  
The only allowed alterations are Sharps. An altered note can be specified by appending  's' to the note name.

```python
# Allowed note names when creating a note object
>>> MidiStructurer.Components.Notes.ALL_NOTES
ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]
```

Remark: the input value for Name when creating a Note is a string, but it is converted to an enum value inside the Note class.

```python
# Creating a Note. Default values are Name="A" and Octave=5
>> Note()
Note(A5)

# Can specify values
>> Note("B", 6)
Note(B6)

# Append s to Name to create a Note with a sharp
>> Note("Cs", 5)
Note(Cs5)

# The note name can be access by the .Name property. Returns NoteName enum
>> Note("C", 5).Name
<NoteName.C: 0>
>> Note("C", 5).Name.name
"C"
>> Note("C", 5).Name.value
0
```

The intent of this library is to represent a song as a succession of Notes, ordered into Structural classes, to then generate a midi file, or interface with other libraries.    
As such a Note object has methods to return its height, aka its note for a midi note_on/note_off message, as well as its frequency.  
Remark: the height computation is what allows all comparisons, and tonal distance computations. 

```python
>> Note("C", 5).ComputeHeight()
72

>> Note("C", 5).ComputeFrequency()
523.2

# This means it is also possible to create a note from its height
>> CreateNoteFromHeight(72)
Note(C5)
```

### ScaleSpecs Class

A ScaleSpecs object allows to generate Scales, aka List of Notes, according to presets.

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
>> sc.FindSameTypeNeighbours()
[ScaleSpecs(D-Major), ScaleSpecs(E-Major)]

# can also find the neighbouring minor from a major scale, and vice versa
>> sc.FindDifferentTypeNeighbour()
ScaleSpecs(Fs-Minor)

# Get all neighbours
>> sc.FindNeighbouringScales()
[ScaleSpecs(D-Major), ScaleSpecs(E-Major), ScaleSpecs(Fs-Minor)]
```

### Interval Class

In Music Theory, the distance between 2 Notes is called an Interval. Intervals are defined by their number, their quality and the distance in terms on semitones.  
Some combinations are considered consonants (i.e. nice sounding) while others are dissonants.  
The use of this class requires some knowledge interval numbers and interval quality, so if you need a refresher [check out Wikipedia](https://en.wikipedia.org/wiki/Interval_(music\))
or the wiki (WIP)

```python
# All Intervals can be found in ALL_INTERVALS, sorted by tonal distance
>> Intervals.ALL_INTERVALS

# Create an Interval object by specifying an Interval Number and a Quality
>> interval = Interval(4, "Perfect")
Interval(4-Augmented--6 semitones)

# An invalid interval definition will throw an error
>> Interval(4, "Major")
KeyError: 'Wrong Inputs: (IntervalNumber: 4, Quality: Major) is not a valid combination for an interval.'

# If needed, there is a class method to find Interval quality from interval number and tonal distance
>> Interval.FindQualityFromOtherSpecs(intervalNumber=4, tonalDistance=4)
'Diminished'
# If there is no relevant interval, this returns None
```

## Operations on Notes

The __add__ and __sub__ operators have been overloaded to allow special operations.
  
##### Notes and Notes
```python
# base note for all our examples
>> n = Note("C", 5)
Note(C5)

# Notes have a Height, defined by its Name and Octave, so comparisons are supported
>> n > n
False
>> n >= n 
True

# Can perform a substraction between two notes. Will return an integer representing tonal distance in semitones
>> n - Note("F", 4)
7
>> Note("F", 4) - n
-7
# Use the method ComputeRootedTonalDistance to ensure positive value is returned
>> n.ComputeRootedTonalDistance(Note("F", 4))
7
>> Note("F", 4).ComputeRootedTonalDistance(n)
7

# It is also possible to get an Interval object describing the distance between 2 notes
# This method requires the lower note to be the one calling the method
>> Note("F", 4).GetIntervalSpecs(n)
Interval(5-Perfect--7 semitones)
```


##### Notes and integers
```python
# Adding a Note and a int returns a new note, translated by a given number of semitones
>> n + 4
Note(E5)

# Substractions are also supported
>> (n + 4) - 4 
Note(C5)

# Changes in Octave are handled automatically
>> n - 1
Note(B4)
```

##### Notes and Intervals
See Intervals section for more details on Interval class

```python
>> i = Interval(IntervalNumber=3, Quality="Major")
# Can add interval to a note, returns a tuple (Note, error)
# error is None, except when unable to compute a note from the given starting note and interval
# Here no error since it is possible to create a Major Third from a C note
>> n + i
(Note(E5), None)

>> i2 = Interval(IntervalNumber=2, Quality="Augmented")
# In this case it is not possible to generate an Augmented Second from a C note
# Intervals are linked to a number of semitones, so it returns Note + number of semitones associated with the interval
# and an error as second element of the return tuple (error is very verbose)
>> n + i2
(Note(Ds5), ValueError('Expected Interval Cannot Be Generated: Invalid Interval from given starting note. Target Interval: Interval(2-Augmented--3 semitones), GeneratedInterval: Interval(3-Minor--3 semitones)'))
# There is no throw in this case so execution is not interrupted
```