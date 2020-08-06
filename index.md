---
layout: default
title: Index
nav_order: 1
---

# MusiStrata

MusiStrata is a pure Python library to represent and manipulate Musical Components.

The idea is to be able to create Notes, translate them using Tonal Distance and Intervals, generate Chords...   
Basically, support all operations useful in creating music algorithmically, through the use of Western Music Theory.

## Philosophy  

MusiStrata is meant to reach a wide public by enabling a data-driven approach to algorithmic Music Composition as well as easy integration in a variety of environment.  

Here is what we mean:  
- **Behaviour can be specified by JSON files** and will be an integral part of the generation process. Take a look at the VelocityColorer section as an example of what is intended: Beats Accentuation can be defined in a very straightforward, yet very flexible, manner by setting simple fields.  
- **MusiStrata transpiles to Javascript.** We are still working the kinks out, but this means a large portion of the library can be used with little to no difference in websites, phone applications and even on desktop through Electron or other webview approaches. All of this, without needing to download the huge interpreter files!


## Implementation  

MusiStrata defines Components to represent Musical Elements. There are 2 types:
- Basic Components (Notes, Scales, Intervals and Chords) which represent Notes and potential operations that can be applied to it to generate complex sequences of Notes.
- Structural Components (SoundEvents, Bars, Tracks and Songs) which allow us to structure our Notes into rhythmically defined sequences.



## Projects Using this Library  

- [MidiSplitter](https://github.com/Wally869/MidiSplitter), an algorithm that splits Midi Files per Channel into subsections which are then saved as standalone Midi Files.
- [VisualMidi](https://github.com/Wally869/VisualMidi), a webapp to visualize and analyze Midi Files.