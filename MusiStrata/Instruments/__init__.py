from .MidiInstruments import (
    InstrumentsLibrary as MidiInstrumentsLibrary,
)

GetSignalFromInstrument = MidiInstrumentsLibrary.GetSignalFromInstrumentName

from .MidiDrums import (
    DrumsLibrary as MidiDrumsLibrary,
    GetHeightFromDrumsInstrumentName,
)
