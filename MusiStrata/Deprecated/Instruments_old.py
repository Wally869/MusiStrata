from __future__ import annotations
from typing import List, Tuple, Dict, Union

from dataclasses import dataclass

from .Utils.PrimitiveClassesUtils import Record, Library


# List taken from: https://github.com/mobyvb/midi-converter/blob/master/lib/instruments.json
RAW_INSTRUMENTS = [
    {"hexcode": "0x00", "family": "Piano", "instrument": "Acoustic Grand Piano"},
    {"hexcode": "0x01", "family": "Piano", "instrument": "Bright Acoustic Piano"},
    {"hexcode": "0x02", "family": "Piano", "instrument": "Electric Grand Piano"},
    {"hexcode": "0x03", "family": "Piano", "instrument": "Honky-tonk Piano"},
    {"hexcode": "0x04", "family": "Piano", "instrument": "Electric Piano 1"},
    {"hexcode": "0x05", "family": "Piano", "instrument": "Electric Piano 2"},
    {"hexcode": "0x06", "family": "Piano", "instrument": "Harpsichord"},
    {"hexcode": "0x07", "family": "Piano", "instrument": "Clavichord"},
    {"hexcode": "0x08", "family": "Chromatic Percussion", "instrument": "Celesta"},
    {"hexcode": "0x09", "family": "Chromatic Percussion", "instrument": "Glockenspiel"},
    {"hexcode": "0x0A", "family": "Chromatic Percussion", "instrument": "Music Box"},
    {"hexcode": "0x0B", "family": "Chromatic Percussion", "instrument": "Vibraphone"},
    {"hexcode": "0x0C", "family": "Chromatic Percussion", "instrument": "Marimba"},
    {"hexcode": "0x0D", "family": "Chromatic Percussion", "instrument": "Xylophone"},
    {"hexcode": "0x0E", "family": "Chromatic Percussion", "instrument": "Tubular bells"},
    {"hexcode": "0x0F", "family": "Chromatic Percussion", "instrument": "Dulcimer"},
    {"hexcode": "0x10", "family": "Organ", "instrument": "Drawbar Organ"},
    {"hexcode": "0x11", "family": "Organ", "instrument": "Percussive Organ"},
    {"hexcode": "0x12", "family": "Organ", "instrument": "Rock Organ"},
    {"hexcode": "0x13", "family": "Organ", "instrument": "Church Organ"},
    {"hexcode": "0x14", "family": "Organ", "instrument": "Reed Organ"},
    {"hexcode": "0x15", "family": "Organ", "instrument": "Accordion"},
    {"hexcode": "0x16", "family": "Organ", "instrument": "Harmonica"},
    {"hexcode": "0x17", "family": "Organ", "instrument": "Tango Accordion"},
    {"hexcode": "0x18", "family": "Guitar", "instrument": "Acoustic Guitar (nylon)"},
    {"hexcode": "0x19", "family": "Guitar", "instrument": "Acoustic Guitar (steel)"},
    {"hexcode": "0x1A", "family": "Guitar", "instrument": "Electric Guitar (jazz)"},
    {"hexcode": "0x1B", "family": "Guitar", "instrument": "Electric Guitar (clean)"},
    {"hexcode": "0x1C", "family": "Guitar", "instrument": "Electric Guitar (muted)"},
    {"hexcode": "0x1D", "family": "Guitar", "instrument": "Overdriven Guitar"},
    {"hexcode": "0x1E", "family": "Guitar", "instrument": "Distortion Guitar"},
    {"hexcode": "0x1F", "family": "Guitar", "instrument": "Guitar harmonics"},
    {"hexcode": "0x20", "family": "Bass", "instrument": "Acoustic Bass"},
    {"hexcode": "0x21", "family": "Bass", "instrument": "Electric Bass (finger)"},
    {"hexcode": "0x22", "family": "Bass", "instrument": "Electric Bass (pick)"},
    {"hexcode": "0x23", "family": "Bass", "instrument": "Fretless Bass"},
    {"hexcode": "0x24", "family": "Bass", "instrument": "Slap Bass 1"},
    {"hexcode": "0x25", "family": "Bass", "instrument": "Slap bass 2"},
    {"hexcode": "0x26", "family": "Bass", "instrument": "Synth Bass 1"},
    {"hexcode": "0x27", "family": "Bass", "instrument": "Synth Bass 2"},
    {"hexcode": "0x28", "family": "Strings", "instrument": "Violin"},
    {"hexcode": "0x29", "family": "Strings", "instrument": "Viola"},
    {"hexcode": "0x2A", "family": "Strings", "instrument": "Cello"},
    {"hexcode": "0x2B", "family": "Strings", "instrument": "Contrabass"},
    {"hexcode": "0x2C", "family": "Strings", "instrument": "Tremolo Strings"},
    {"hexcode": "0x2D", "family": "Strings", "instrument": "Pizzicato Strings"},
    {"hexcode": "0x2E", "family": "Strings", "instrument": "Orchestral Harp"},
    {"hexcode": "0x2F", "family": "Strings", "instrument": "Timpani"},
    {"hexcode": "0x30", "family": "Ensemble", "instrument": "String Ensemble 1"},
    {"hexcode": "0x31", "family": "Ensemble", "instrument": "String Ensemble 2"},
    {"hexcode": "0x32", "family": "Ensemble", "instrument": "SynthStrings 1"},
    {"hexcode": "0x33", "family": "Ensemble", "instrument": "SynthStrings 2"},
    {"hexcode": "0x34", "family": "Ensemble", "instrument": "Choir Aahs"},
    {"hexcode": "0x35", "family": "Ensemble", "instrument": "Voice Oohs"},
    {"hexcode": "0x36", "family": "Ensemble", "instrument": "Synth Voice"},
    {"hexcode": "0x37", "family": "Ensemble", "instrument": "Orchestra Hit"},
    {"hexcode": "0x38", "family": "Brass", "instrument": "Trumpet"},
    {"hexcode": "0x39", "family": "Brass", "instrument": "Trombone"},
    {"hexcode": "0x3A", "family": "Brass", "instrument": "Tuba"},
    {"hexcode": "0x3B", "family": "Brass", "instrument": "Muted Trombone"},
    {"hexcode": "0x3C", "family": "Brass", "instrument": "French Horn"},
    {"hexcode": "0x3D", "family": "Brass", "instrument": "Brass Section"},
    {"hexcode": "0x3E", "family": "Brass", "instrument": "SynthBrass 1"},
    {"hexcode": "0x3F", "family": "Brass", "instrument": "SynthBrass 2"},
    {"hexcode": "0x40", "family": "Reed", "instrument": "Soprano Sax"},
    {"hexcode": "0x41", "family": "Reed", "instrument": "Alto Sax"},
    {"hexcode": "0x42", "family": "Reed", "instrument": "Tenor Sax"},
    {"hexcode": "0x43", "family": "Reed", "instrument": "Baritone Sax"},
    {"hexcode": "0x44", "family": "Reed", "instrument": "Oboe"},
    {"hexcode": "0x45", "family": "Reed", "instrument": "English Horn"},
    {"hexcode": "0x46", "family": "Reed", "instrument": "Bassoon"},
    {"hexcode": "0x47", "family": "Reed", "instrument": "Clarinet"},
    {"hexcode": "0x48", "family": "Pipe", "instrument": "Piccolo"},
    {"hexcode": "0x49", "family": "Pipe", "instrument": "Flute"},
    {"hexcode": "0x4A", "family": "Pipe", "instrument": "Recorder"},
    {"hexcode": "0x4B", "family": "Pipe", "instrument": "Pan Flute"},
    {"hexcode": "0x4C", "family": "Pipe", "instrument": "Blown Bottle"},
    {"hexcode": "0x4D", "family": "Pipe", "instrument": "Shakuhachi"},
    {"hexcode": "0x4E", "family": "Pipe", "instrument": "Whistle"},
    {"hexcode": "0x4F", "family": "Pipe", "instrument": "Ocarina"},
    {"hexcode": "0x50", "family": "Synth Lead", "instrument": "Lead 1 (square)"},
    {"hexcode": "0x51", "family": "Synth Lead", "instrument": "Lead 2 (sawtooth)"},
    {"hexcode": "0x52", "family": "Synth Lead", "instrument": "Lead 3 (calliope)"},
    {"hexcode": "0x53", "family": "Synth Lead", "instrument": "Lead 4 (chiff)"},
    {"hexcode": "0x54", "family": "Synth Lead", "instrument": "Lead 5 (charang)"},
    {"hexcode": "0x55", "family": "Synth Lead", "instrument": "Lead 6 (voice)"},
    {"hexcode": "0x56", "family": "Synth Lead", "instrument": "Lead 7 (fifths)"},
    {"hexcode": "0x57", "family": "Synth Lead", "instrument": "Lead 8 (bass + lead)"},
    {"hexcode": "0x58", "family": "Synth Pad", "instrument": "Pad 1 (new age)"},
    {"hexcode": "0x59", "family": "Synth Pad", "instrument": "Pad 2 (warm)"},
    {"hexcode": "0x5A", "family": "Synth Pad", "instrument": "Pad 3 (polysynth)"},
    {"hexcode": "0x5B", "family": "Synth Pad", "instrument": "Pad 4 (choir)"},
    {"hexcode": "0x5C", "family": "Synth Pad", "instrument": "Pad 5 (bowed)"},
    {"hexcode": "0x5D", "family": "Synth Pad", "instrument": "Pad 6 (metallic)"},
    {"hexcode": "0x5E", "family": "Synth Pad", "instrument": "Pad 7 (halo)"},
    {"hexcode": "0x5F", "family": "Synth Pad", "instrument": "Pad 8 (sweep)"},
    {"hexcode": "0x60", "family": "Synth Effects", "instrument": "FX 1 (rain)"},
    {"hexcode": "0x61", "family": "Synth Effects", "instrument": "FX 2 (soundtrack)"},
    {"hexcode": "0x62", "family": "Synth Effects", "instrument": "FX 3 (crystal)"},
    {"hexcode": "0x63", "family": "Synth Effects", "instrument": "FX 4 (atmosphere)"},
    {"hexcode": "0x64", "family": "Synth Effects", "instrument": "FX 5 (brightness)"},
    {"hexcode": "0x65", "family": "Synth Effects", "instrument": "FX 6 (goblins)"},
    {"hexcode": "0x66", "family": "Synth Effects", "instrument": "FX 7 (echoes)"},
    {"hexcode": "0x67", "family": "Synth Effects", "instrument": "FX 8 (sci-fi)"},
    {"hexcode": "0x68", "family": "Ethnic", "instrument": "Sitar"},
    {"hexcode": "0x69", "family": "Ethnic", "instrument": "Banjo"},
    {"hexcode": "0x6A", "family": "Ethnic", "instrument": "Shamisen"},
    {"hexcode": "0x6B", "family": "Ethnic", "instrument": "Koto"},
    {"hexcode": "0x6C", "family": "Ethnic", "instrument": "Kalimba"},
    {"hexcode": "0x6D", "family": "Ethnic", "instrument": "Bag pipe"},
    {"hexcode": "0x6E", "family": "Ethnic", "instrument": "Fiddle"},
    {"hexcode": "0x6F", "family": "Ethnic", "instrument": "Shanai"},
    {"hexcode": "0x70", "family": "Percussive", "instrument": "Tinkle Bell"},
    {"hexcode": "0x71", "family": "Percussive", "instrument": "Agogo"},
    {"hexcode": "0x72", "family": "Percussive", "instrument": "Steel Drums"},
    {"hexcode": "0x73", "family": "Percussive", "instrument": "Woodblock"},
    {"hexcode": "0x74", "family": "Percussive", "instrument": "Taiko Drum"},
    {"hexcode": "0x75", "family": "Percussive", "instrument": "Melodic Tom"},
    {"hexcode": "0x76", "family": "Percussive", "instrument": "Synth Drum"},
    {"hexcode": "0x77", "family": "Percussive", "instrument": "Reverse Cymbal"},
    {"hexcode": "0x78", "family": "Sound Effects", "instrument": "Guitar Fret Noise"},
    {"hexcode": "0x79", "family": "Sound Effects", "instrument": "Breath Noise"},
    {"hexcode": "0x7A", "family": "Sound Effects", "instrument": "Seashore"},
    {"hexcode": "0x7B", "family": "Sound Effects", "instrument": "Bird Tweet"},
    {"hexcode": "0x7C", "family": "Sound Effects", "instrument": "Telephone Ring"},
    {"hexcode": "0x7D", "family": "Sound Effects", "instrument": "Helicopter"},
    {"hexcode": "0x7E", "family": "Sound Effects", "instrument": "Applause"},
    {"hexcode": "0x7F", "family": "Sound Effects", "instrument": "Gunshot"}
]

# Create direct mapping from instrument names to signal (int)
INSTRUMENT_NAME_TO_SIGNAL = {inst["instrument"]: int(inst["hexcode"], 16) for inst in RAW_INSTRUMENTS}

INSTRUMENT_NAMES = list(INSTRUMENT_NAME_TO_SIGNAL.keys())

# modifying a supposed const but I guess it's ok
for elemid in range(len(RAW_INSTRUMENTS)):
    for pairKeys in [["hexcode", "Signal"], ["family", "Family"], ["instrument", "Name"]]:
        RAW_INSTRUMENTS[elemid][pairKeys[1]] = RAW_INSTRUMENTS[elemid][pairKeys[0]]
        del RAW_INSTRUMENTS[elemid][pairKeys[0]]

    RAW_INSTRUMENTS[elemid]["Signal"] = int(RAW_INSTRUMENTS[elemid]["Signal"], 16)


class InstrumentsLibraryClass(Library):
    BaseName: str = "InstrumentsLibrary"
    Records: List[Record] = None

    def GetSignalFromInstrumentName(self, instrument: str) -> int:
        return self.GetFromValueInField("Name", instrument)[0].Signal

    def GetInstrumentNameFromSignal(self, signal: int) -> str:
        return self.GetFromValueInField("Signal", signal)[0].Name

    def GetFamilyFromSignal(self, signal: int) -> str:
        return self.GetFromValueInField("Signal", signal)[0].Family

    def GetFamilyFromInstrumentName(self, instrument: str) -> str:
        return self.GetFromValueInField("Name", instrument)[0].Family


InstrumentsLibrary = InstrumentsLibraryClass(RAW_INSTRUMENTS)


# unnecessary, but keeping a function for current backward compatibility
def GetSignalFromInstrument(instrument: str) -> int:
    print("DEPRECATION WARNING: GetSignalFromInstrument has been deprecated.")
    print("Use Instruments.GetSignalFromInstrumentName directly instead")
    return InstrumentsLibrary.GetSignalFromInstrumentName(instrument)

