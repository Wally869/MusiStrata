# List taken from https://github.com/ianjennings/midi-wtf/blob/master/index.js
RAW_DRUMS = {
  27: "High Q",
  28: "Slap",
  29: "Scratch Push",
  30: "Scratch Pull",
  31: "Sticks",
  32: "Square Click",
  33: "Metronome Click",
  34: "Metronome Bell",
  35: "Bass Drum 2",
  36: "Bass Drum 1",
  37: "Side Stick",
  38: "Snare Drum 1",
  39: "Hand Clap",
  40: "Snare Drum 2",
  41: "Low Tom 2",
  42: "Closed Hi-hat",
  43: "Low Tom 1",
  44: "Pedal Hi-hat",
  45: "Mid Tom 2",
  46: "Open Hi-hat",
  47: "Mid Tom 1",
  48: "High Tom 2",
  49: "Crash Cymbal 1",
  50: "High Tom 1",
  51: "Ride Cymbal 1",
  52: "Chinese Cymbal",
  53: "Ride Bell",
  54: "Tambourine",
  55: "Splash Cymbal",
  56: "Cowbell",
  57: "Crash Cymbal 2",
  58: "Vibra Slap",
  59: "Ride Cymbal 2",
  60: "High Bongo",
  61: "Low Bongo",
  62: "Mute High Conga",
  63: "Open High Conga",
  64: "Low Conga",
  65: "High Timbale",
  66: "Low Timbale",
  67: "High Agogo",
  68: "Low Agogo",
  69: "Cabasa",
  70: "Maracas",
  71: "Short Whistle",
  72: "Long Whistle",
  73: "Short Guiro",
  74: "Long Guiro",
  75: "Claves",
  76: "High Wood Block",
  77: "Low Wood Block",
  78: "Mute Cuica",
  79: "Open Cuica",
  80: "Mute Triangle",
  81: "Open Triangle",
  82: "Shaker",
  83: "Jingle Bell",
  84: "Belltree",
  85: "Castanets",
  86: "Mute Surdo",
  87: "Open Surdo",
}

DRUMS_NAME_TO_HEIGHT = {
    v: k for k, v in RAW_DRUMS.items() 
}

DRUMS_NAMES = list(
    DRUMS_NAME_TO_HEIGHT.keys()
)


def GetHeightFromDrums(drums: str) -> int:
    outHeight = 46
    try:
        outHeight = DRUMS_NAME_TO_HEIGHT[drums]
    except:
        print("Invalid instrument provided. " + drums + " is not in the list of allowed drums instruments")
        print("Please Check Drums.DRUMS_NAMES for allowed drums instruments")
        print("Defaulting to Open Hi-Hat (height 46)")
        print()
    return outHeight