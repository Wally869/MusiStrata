

from .Components import Scale, Note

from typing import Dict, List


"""
Data & Globals
"""


NB_NOTES_IN_SCALE = 7

ALL_NOTES = [
    "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"
]

SCALE_MODES = [
    "Major",
    "Minor",
    "MinorMelodic"
    #"MinorHarmonic"
]

TONES = {
    "Major": [
        1, 1, 0.5, 1, 1, 1, 0.5
    ],
    "Minor": [
        1, 0.5, 1, 1, 0.5, 1, 1
    ],
    "MinorMelodic": [
        1, 0.5, 1, 1, 0.5, 1.5, 0.5
    ]
}


"""
Methods & Functions
"""
def GenerateScaleNotes(scale: Scale) -> List[str]:
    scaleNotes = [scale.RefNote]
    currIdNote = FindNoteIdInAllNotes(scale.RefNote)

    for toneDelta in TONES[scale.Mode]:
        currIdNote += int(toneDelta * 2)
        while currIdNote > len(ALL_NOTES) - 1:
            # loop back on all notes
            currIdNote -= len(ALL_NOTES)
        scaleNotes.append(ALL_NOTES[currIdNote])

    # We are looping on scale, so first and last notes are identical so return list set
    return list(set(scaleNotes))

# Minor Melodic pentatonic only gives 4 notes
# Using toneDelta >= 1 to fix this?
def GeneratePentatonicScale(scale: Scale) -> List[str]:
    outScale = [scale.RefNote]
    currIdNote = FindNoteIdInAllNotes(scale.RefNote)

    for toneDelta in TONES[scale.Mode]:
        currIdNote += int(toneDelta * 2)
        while currIdNote > len(ALL_NOTES) - 1:
            # loop back on all notes
            currIdNote -= len(ALL_NOTES)
        if (toneDelta >= 1):
            outScale.append(ALL_NOTES[currIdNote])
        if len(outScale) == 5:
            break

    return outScale


def GenerateScaleNotesWithOctaveDelta(scale: Scale) -> List[Dict]:
    octaveDelta = 0
    outScale = [
        {
            "noteName": scale.RefNote,
            "octaveDelta": octaveDelta
        }
    ]
    currIdNote = FindNoteIdInAllNotes(scale.RefNote)

    for toneDelta in TONES[scale.Mode]:
        currIdNote += int(toneDelta * 2)
        while currIdNote > len(ALL_NOTES) - 1:
            # loop back on all notes
            # maybe here extract the fact that I am one octave higher?
            currIdNote -= len(ALL_NOTES)
            octaveDelta += 1

        newNote = {
            "noteName": ALL_NOTES[currIdNote],
            "octaveDelta": octaveDelta
        }
        outScale.append(newNote)

    return outScale


def GeneratePentatonicScaleNotesWithOctaveDelta(scale: Scale) -> List[Dict]:
    octaveDelta = 0
    outScale = [
        {
            "noteName": scale.RefNote,
            "octaveDelta": octaveDelta
        }
    ]
    currIdNote = FindNoteIdInAllNotes(scale.RefNote)

    for toneDelta in TONES[scale.Mode]:
        currIdNote += int(toneDelta * 2)
        while currIdNote > len(ALL_NOTES) - 1:
            # loop back on all notes
            currIdNote -= len(ALL_NOTES)
            octaveDelta += 1
        if (toneDelta >= 1):
            newNote = {
                "noteName": ALL_NOTES[currIdNote],
                "octaveDelta": octaveDelta
            }
            outScale.append(newNote)
        if len(outScale) == 5:
            break

    return outScale



"""
Utils
"""
def FindNoteIdInAllNotes(startingNote : str) -> int:
    for i in range(len(ALL_NOTES)):
        if ALL_NOTES[i] == startingNote:
            return i

def FindNoteIdInScale(note, scale):
    for i in range(len(scale)):
        if scale[i] == note:
            return i

def FindNoteIdInScaleWithOctaveNotation(note: str, scale: List[str]):
    for i in range(len(scale)):
        if scale[i]["noteName"] == note:
            return i


def GetHeightNote(note : Note) -> int:
    return note.Octave * 12 + FindNoteIdInAllNotes(note.NoteName)

def GetNoteNameAndOctaveFromHeight(height: int) -> Dict:
    octave = height // 12
    noteName = ALL_NOTES[height - (height // 12)]
    return {
        "NoteName": noteName,
        "Octave" : octave
    }


def GetNoteFromHeight(height: int) -> Note:
    octave = height // 12
    noteName = ALL_NOTES[height - (height // 12) * 12]
    
    return Note(
        Octave=octave,
        NoteName=noteName
    )

def TranslateNote(note: Note, delta: int) -> Note:
    height = GetHeightNote(note)
    outNote = GetNoteFromHeight(height + delta)
    
    # Set previous beat and duration
    outNote.Beat = note.Beat
    outNote.Duration = note.Duration

    return outNote


