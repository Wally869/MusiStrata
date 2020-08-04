---
layout: default
title: Notes
parent: Components
nav_order: 1
---


# Notes

## Overview  

The Note Object is the most basic element of MusiStrata. It is created to represent Notes as they are defined in Western Music Theory, with a name and an octave value.
Operator overloads have been defined between Notes and most other components to create new Notes.


## Creating and Using a Note object  

Valid Note Names are letters A to G.  
The only allowed alterations are Sharps. An altered note can be specified by appending  's' to the note name.

```python
"""
class Note(object):
    def __init__(self,  Name: str = "A", Octave: int = 5):
        self._Name = NoteNames(Name)   # NoteNames is a class more or less the same functions as an enum
        self._Octave = Octave
"""

# Allowed note names when creating a note object
>>> MusiStrata.Components.Notes.ALL_NOTES
ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]

# Creating a Note. Default values are Name="A" and Octave=5
>> Note()
Note(A5)

# Can specify values
>> Note("B", 6)
Note(B6)

# Append s to Name to create a Note with a sharp
>> Note("Cs", 5)
Note(Cs5)

# The note name can be access by the .Name property.
>> Note("C", 5).Name
"C"
# Name is actually a public property returning _Name.name. 
# The _Name property is a pseudo enum and works similarly.
>> Note("C", 5).Name.name
"C"
>> Note("C", 5).Name.value
0

# Octave can be accessed through the Octave property. A setter ensures it cannot be negative
>> Note("C", 5).Octave
5

```

The intent of this library is to represent a song as a succession of Notes, ordered into Structural classes, to then generate a midi file, or interface with other libraries.    
As such a Note object has methods to return its height, aka its "note" property for a midi note_on/note_off message, as well as its frequency.  
Remark: the height computation is what allows all comparisons, and tonal distance computations. 

```python
>> Note("C", 5).Height
72

>> Note("C", 5).Frequency
523.2

# This means it is also possible to create a note from its height
>> Note.FromHeight(72)
Note(C5)

```