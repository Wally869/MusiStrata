from Interfaces.Components import INote
from .PrimitiveClassesUtils import Record, Library
from .utils import *


def invert(notes: List[INote], inversions: int) -> List[INote]:
    """
        From a list of notes, while inversions > 0 pop the first note, add an octave and put it at the end of the stack
    """
    notes = notes[:]
    while inversions > 0:
        notes.append(notes.pop(0) + 12)
        inversions = inversions - 1
    return notes

