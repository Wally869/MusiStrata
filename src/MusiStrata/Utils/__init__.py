from typing import Any
from .utils import *
from .PrimitiveClassesUtils import *

def invert(notes: List[Any], inversions: int) -> List[Any]:
    """
        From a list of notes, while inversions > 0 pop the first note, add an octave and put it at the end of the stack
    """
    notes = notes[:]
    while inversions > 0:
        notes.append(notes.pop(0) + 12)
        inversions = inversions - 1
    return notes

