


# A note with a sharp is considered to belong to higher staff
NOTE_NAME_TO_STAFF = {
    "A": "A",
    "As": "B",
    "B": "B",
    "C": "C",
    "Cs": "D",
    "D": "D",
    "Ds": "E",
    "E": "E",
    "F": "F",
    "Fs": "G",
    "G": "G",
    "Gs": "A",
}

ALL_NOTES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]

ALL_STAFF_POSITIONS = ["C", "D", "E", "F", "G", "A", "B"]



class NoteNames(EnumManager_Ordered_Looping):
    KeyValuesMap = {ALL_NOTES[i]: i for i in range(len(ALL_NOTES))}
    KeyList = ALL_NOTES
    ValuesList = [i for i in range(len(ALL_NOTES))]


class StaffPositions(EnumManager_Ordered_Looping):
    KeyValuesMap = {ALL_STAFF_POSITIONS[i]: i for i in range(len(ALL_STAFF_POSITIONS))}
    KeyList = ALL_STAFF_POSITIONS
    ValuesList = [i for i in range(len(ALL_STAFF_POSITIONS))]