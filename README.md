# MidiStructurer

## Overview

Classes and Utilities for representing Notes and performing transformations on them with the intent of creating midi files.

In this library I strive to implement some basic concepts of Music Theory, to serve as base for a music generation package.
This is still a WIP, but the main operations are well defined and future work will likely only be extensions.

See the following sections for usage documentation (WIP). 
This library serves as base for my music generation project: https://github.com/Wally869/MidiGenerator

## Installing

```
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

### The Note Object

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

To note: the input value for Name when creating a Note is a string, but it is converted to an enum value inside the Note class.

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

### Operations on Notes

The __add__ and __sub__ operators have been overloaded to allow special operations.
  

##### Notes and integers
```python
# base note for all our examples
>> n = Note("C", 5)
Note(C5)

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