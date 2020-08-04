---
layout: default
title: Index
nav_order: 1
---

# MusiStrata

MusiStrata is a pure Python library to represent and manipulate Musical Components.

The idea is to be able to create Notes, translate them using Tonal Distance and Intervals, generate Chords... Support all operations useful in creating music algorithmically, through the use of Western Music Theory 

## Implementation  

MusiStrata defines Components to represent Musical Elements. There are 2 types:
- Basic Components (Notes, Scales, Intervals and Chords) which represent Notes and potential operations that can be applied to it to generate complex sequences of Notes.
- Structural Components (SoundEvents, Bars, Tracks and Songs) which allow us to structure our Notes into rhythmically defined sequences.



## Components



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
>> sc.GetSameTypeNeighbours()
[ScaleSpecs(D-Major), ScaleSpecs(E-Major)]

# can also find the neighbouring minor from a major scale, and vice versa
>> sc.GetDifferentTypeNeighbour()
ScaleSpecs(Fs-Minor)

# Get all neighbours
>> sc.GetNeighbouringScales()
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
>> Interval.FindQualityFromNumberAndDistance(intervalNumber=4, tonalDistance=4)
'Diminished'
# If there is no relevant interval, this returns None
```

### Chords

Still a WIP. Can create a Chord Object by passing a list of Intervals to it.

```python
# Create a chord from a major third and a perfect 5th. 
>> chord = Chord([Interval(3, "Major"), Interval(5, "Perfect")])
Chord(M3-P5)

# this works as a callable class. Outputs (List[Note], List[errors]).
# errors in output are the interval errors seen below in section "Notes and Intervals"
>> chord(Note())
([Note(A5), Note(Cs6), Note(E6)], [ValueError('Invalid from given starting note. Target: Interval(3-Major--4 semitones), Generated: Interval(4-Diminished--4 semitones)'), None])

# chord can return with silenced errors
>> chord(Note(), excludeErrors=True)
[Note(A5), Note(Cs6), Note(E6)]

# By default, chords apply all intervals to the provided note
# but it is possible to make the chord apply intervals to the generated notes in succession
>> chord(Note(), fromRoot=False, excludeErrors=True)
[Note(A5), Note(Cs6), Note(Gs6)]
# In this case, what is done is Note(A5) + Interval(M3) = Note(Cs6)
# Then Note(Cs6) + Interval(P5) = Note(Gs6)

# Chords output a List of Notes, which includes the input note
# For convenience, it is possible to exclude the root note from the output
>> chord(Note(), fromRoot=False, rootInOutput=False, excludeErrors=True)
[Note(Cs6), Note(Gs6)]
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
>> n.GetRootedTonalDistance(Note("F", 4))
7
>> Note("F", 4).GetRootedTonalDistance(n)
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
