from .MidiInstruments import (
    InstrumentsLibrary as MidiInstrumentsLibrary,
)

GetSignalFromInstrument = MidiInstrumentsLibrary.GetSignalFromInstrumentName

from .MidiDrums import (
    DrumsLibrary as MidiDrumsLibrary,
    GetHeightFromDrumsInstrumentName,
)



class Instrument:
    """
        Base class for instruments
    """
    pass


from dataclasses import dataclass
from typing import Optional


@dataclass
class MidiInstrument(Instrument): 
    """
        Define Midi instrument.
        Soundfont parameter is optional and overrides the soundfont defined in song
    """
    name: str
    id: int
    is_drums: bool
    soundfont: Optional[str] = None


@dataclass
class VstInstrument(Instrument):
    """
        Define VST instrument
    """
    name: str
    vst_path: str
    preset_id: int


class RenderSettings:
    """
        Base class, use LmmsRenderSettings or MidiRenderSettings
    """
    pass

@dataclass
class LmmsRenderSettings(RenderSettings):
    pass


@dataclass
class MidiRenderSettings(RenderSettings):
    soundfont: Optional[str] = None


