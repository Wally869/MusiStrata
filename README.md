# MidiStructurer

### Overview

Classes and Utilities for algorithmic music generation of midi files.

Midi is a great format, but I find it unpractical as is to generate music so I created these classes to serve as an intermediary representation.

Here are some benefits to these classes:
- Sensible representations of data
- Instruments and Notes are encoded in user-friendly format instead of a numeric value
- Scales Generation, and selection of neighbour scales following the Circle of Fifth in music theory
- Timedelta between Midi events is calculated at conversion time, the user only cares about beats and duration of notes

I am also working on helpers to generate music, hoping to share it soon 

### Examples

See Examples.py for some quick implementation examples.
You can also run Examples.py, and listen to the generated samples in the Examples folder.

### Dependencies

Written in python, the only dependency is Mido (https://github.com/mido/mido)

### Components

I tried to create sensible representations for music components

- Note

A simple music note, meant to be in a Bar (see below).

```python
Note(
    Beat=1.0,
    Duration= 1.0,
    Octave=5,
    NoteName="A"
)
```

This Note would be a A5, played on Beat 1 of a given Bar, for a duration of 1 beat (i.e. a quarter note / crotchet)


- Bar

A dataclass containing a list of Notes

```python
@dataclass
class Bar:
    Notes: list = field(default_factory=list)

```

- Track

A track of a Song. Keeps in memory the instrument used in this particular track, as well as the velocity of the track (i.e. how loud the notes should be played)
The Name field is mostly for readability purpose 

```python
@dataclass
class Track:
    Name: str = ""
    Instrument: str = ""
    Bars: list = field(default_factory=list)
    Velocity: int = 80

```

- Song

Records all the tracks, and some song-wide elements: tempo and beats per bar
This object is the one passed to the converter (based on mido) for file generation

```python
@dataclass
class Song:
    Tempo: int = 80
    BeatsPerBar: int = 4
    Tracks: list = field(default_factory=list)

```


### Converter

The function ConvertSong in MidoConverter.py takes as input a Song object and a string specying the name of the output file (for example "test.mid").

```python
import mido

ConvertSong(song: Song, outfile: str) -> mido.MidiFile
```

Time difference between Midi messages is given in ticks so the converter computes a tick time for each notes specified for each track.
Once these occurring times are computed, the converter generates Midi Messages with the proper time differences between them before saving them and other specific information in a midi file.




