from typing import List, Tuple, Dict, Union
from dataclasses import dataclass, field

from enum import Enum


class Errors(Enum):
    InvalidHeight = (0,)
    IntervalError = (1,)
