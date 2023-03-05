from typing import List, Union, cast
from typing_extensions import Self
from enum import Enum

from MusiStrata.Utils import EnumExtensions

from dataclasses import dataclass

class TrackType(Enum):
    Instrument = 0,
    Drums = 1,
    Sample = 2


class InstrumentType(Enum):
    Instrument = 0,
    Drums = 1

@dataclass
class Instrument:
    type: InstrumentType
    name: str



