---
layout: default
title: MidoConverter
nav_order: 6
---

# MidoConverter  

## Overview  

MidoConverter is a wrapper around the [Mido Package](https://github.com/mido/mido) to create and output a Midi file from a Song object.  

The ConvertSong function handles several things:  
- Create Meta Messages to change instruments used and tempo  
- Set appropriate channel for the drums track  
- Set SoundBank parameter  
- Convert Bar and Beats position to appropriate tick values  

## Usage  

The file revolves around the ConvertSong function, which is the only function you should use.

```python
def ConvertSong(song: Song, outfile: str) -> midoMidiFile
```

Simply call ConvertSong and pass your song and the name of the output file as parameters. Don't forget to add the .mid extension for the output name.  


