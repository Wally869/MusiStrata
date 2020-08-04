# MusiStrata

## Overview

MusiStrata is a pure Python library to represent and manipulate Musical Components.  

The idea is to be able to create Notes, translate them using Tonal Distance and Intervals, generate Chords... 
  
[The Documentation is available on github pages.](https://wally869.github.io/MusiStrata/)


Some of my projects using this library:
- [MidiSplitter](https://github.com/Wally869/MidiSplitter), an algorithm that splits Midi Files per Channel into subsections which are then saved as standalone Midi Files.
- [VisualMidi](https://github.com/Wally869/VisualMidi), a webapp to visualize and analyze Midi Files.


## Installing

```shell script
git clone https://github.com/Wally869/MusiStrata.git
cd MusiStrata
pip install -e .
```

## Examples

See Examples.py for some quick implementation examples.
You can also run Examples.py, and listen to the generated samples in the Examples folder.

## Dependencies

- [Mido](https://github.com/mido/mido), to generate Midi Files
- [Soundcard](https://github.com/bastibe/SoundCard), a cross-platform library for playing and recording sound in Python

