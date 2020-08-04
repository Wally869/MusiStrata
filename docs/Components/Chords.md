---
layout: default
title: Chords
parent: Components
nav_order: 4
---

# Chords

## Overview  

MusiStrata allows you to define Chords from Intervals, and apply them to a Note.

Multiple Features are supported:  
- No limit on Chord size  
- Silence Errors (by default, returns errors from Intervals)  
- Apply Chord intervals to root Note, or to intermediary Notes  
- Chord Inversion  

## Usage

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

# By default, chords apply all intervals to the provided root note
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

