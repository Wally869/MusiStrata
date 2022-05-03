from typing import List, Tuple


class BaseNote(object):
    NoteName: str
    Octave: int
    Height: int



from typing import List

from MusiStrata import Note, NoteNames

from itertools import permutations, combinations, combinations_with_replacement, product


def distance(n1: NoteNames, n2: NoteNames) -> int:
    return abs(n1._Name.ToStaffPosition().value - n2._Name.ToStaffPosition().value)


def _MinimizeDistance_LessNotesInBase(notes_1: List[Note], notes_2: List[Note]) -> List[Note]:
    """
        Find the subset of notes from notes_2 which minimizes distance from notes_1.
        Remaining notes will be considered as chord extensions, and set above the other notes. 
    """
    perms = [list(elem) for elem in product(notes_2, repeat=len(notes_1))]

    distances = []
    for perm in perms:
        curr = perm  #notes_2[:] + perm
        summed = 0
        for id_elem in range(len(curr)):
            summed += distance(notes_1[id_elem], curr[id_elem])
        distances.append(summed)

    # find lowest  
    min_distance = 999
    chosen_id = 0
    for id_elem in range(len(distances)):
        if distances[id_elem] < min_distance:
            min_distance = distances[id_elem]
            chosen_id = id_elem

    out_notes = perms[chosen_id]
    # gotta find missing from out_notes and save them on the side
    missing: List[Note] = []
    for elem in notes_2:
        if elem not in out_notes:
            missing.append(elem)

    # now minimize tonal pairwise distance 
    out_notes = AdjustOctaves(notes_1, out_notes)
    # now add missing to out_notes, but make sure they are above
    max_height = 0
    for elem in out_notes:
        if elem.Height > max_height:
            max_height = elem.Height

    for id_elem in range(len(missing)):
        while(missing[id_elem].Height < max_height):
            missing[id_elem] = missing[id_elem] + 12

    return out_notes   #+ missing


def _MinimizeDistance_MoreNotesInBase(notes_1: List[Note], notes_2: List[Note], can_pad: bool = False) -> List[Note]:
    if can_pad:
        return _MinimizeDistance_MoreNotesInBase_WithPadding(notes_1, notes_2)
    else:
        return _MinimizeDistance_MoreNotesInBase_NoPadding(notes_1, notes_2)


def _MinimizeDistance_MoreNotesInBase_WithPadding(notes_1: List[Note], notes_2: List[Note]) -> List[Note]:
    """
        Smoothen transition between notes_1 and notes_2 with len(notes_1) > len(notes_2) with padding allowed. 
        Find all combinations of notes with length of notes_2 padded by duplicating notes, then find combination
        that minimizes staff distance, adjust octave height and prune solutions that end up with twice the same note.   
    """
    delta_len = len(notes_1) - len(notes_2)
    #perms = list(product(notes_2, delta_len))
    perms_base = [list(elem) for elem in list(permutations(notes_2))]
    perms = [list(elem) for elem in product(notes_2, repeat=delta_len)]
    combinations = []
    for perm_base in perms_base:
        for perm in perms:
            combinations.append(perm_base + perm)
    
    distances = []
    for id_perm in range(len(combinations)):
        curr = combinations[id_perm]
        summed = 0
        for id_elem in range(len(curr)):
            summed += notes_1[id_elem].StaffDistance(curr[id_elem])  # distance(notes_1[id_elem], curr[id_elem])
        distances.append((id_perm, summed))

    # sort by distance  
    distances = sorted(distances, key=lambda x: x[1])
    # get value min and prune
    min_distance = distances[0][1]
    #distances = list(filter(lambda x: x[1] == min_distance, distances))
    pruned = []
    for elem in distances:
        curr_notes = combinations[elem[0]]
        curr_notes = AdjustOctaves(notes_1, curr_notes)
        if len(set(curr_notes)) == len(curr_notes):
            # compute tonal distance
            summed_tonal_distance = 0
            for id_note in range(len(curr_notes)):
                summed_tonal_distance += abs(curr_notes[id_note] - notes_1[id_note])
            pruned.append((summed_tonal_distance, curr_notes))
    
    pruned = sorted(pruned, key=lambda x: x[0])
    return pruned[0][1]



def _MinimizeDistance_MoreNotesInBase_NoPadding(notes_1: List[Note], notes_2: List[Note]) -> List[Note]:
    """
        Proceed in reverse compared to the others: find the subset of notes from the initial chord that allows for the minimal distance,
        in the second chord, then adjust octave of notes in notes_2. 
    """
    perms = [list(elem) for elem in product(notes_1, repeat=len(notes_2))]

    distances = []
    for perm in perms:
        summed = 0
        for id_elem in range(len(perm)):
            summed += distance(perm[id_elem], notes_2[id_elem])
        distances.append(summed)

    # find lowest  
    min_distance = 999
    chosen_id = 0
    for id_elem in range(len(distances)):
        if distances[id_elem] < min_distance:
            min_distance = distances[id_elem]
            chosen_id = id_elem

    chosen_target = perms[chosen_id]
    # now minimize tonal pairwise distance 
    out_notes = AdjustOctaves(chosen_target, notes_2)
    return out_notes


def AdjustOctaves(notes_1: List[Note], notes_2: List[Note]) -> List[Note]:
    out_notes = []
    for id_note in range(len(notes_2)):
        curr_note = notes_2[id_note]
        while notes_1[id_note] - curr_note > 6:
            curr_note = curr_note + 12
        while notes_1[id_note] - curr_note < -6 :
            curr_note = curr_note - 12
        out_notes.append(curr_note)
    return out_notes    

def _MinimizeDistance_EqualNotes(notes_1: List[Note], notes_2: List[Note]) -> List[Note]:
    # get permutations staff_2
    perms = list(permutations(notes_2))
    distances = []
    for id_perm in range(len(perms)):
        perm = perms[id_perm]
        summed = 0
        for id_elem in range(len(perm)):
            summed += distance(notes_1[id_elem], perm[id_elem])
        distances.append((id_perm, summed))

    # sort by distance  
    distances = sorted(distances, key=lambda x: x[1])
    outputs = []
    for elem in distances:
        curr_notes = perms[elem[0]]
        curr_notes = AdjustOctaves(notes_1, curr_notes)
        if len(set(curr_notes)) == len(curr_notes):
            outputs.append(curr_notes)

    return outputs[0]


def MinimizeDistance(notes_1: List[Note], notes_2: List[Note], can_pad: bool = True) -> List[Note]:
    """
        Minimize distance between notes of 2 chords. Consider first notes first chord as immutable
    """
    smoothed: List[Note]
    if len(notes_1) == len(notes_2):
        smoothed = _MinimizeDistance_EqualNotes(notes_1, notes_2)
    elif len(notes_1) > len(notes_2):
        smoothed = _MinimizeDistance_MoreNotesInBase(notes_1, notes_2, can_pad)
    else:
        smoothed = _MinimizeDistance_LessNotesInBase(notes_1, notes_2)

    return sorted(smoothed, key=lambda x : x.Height)


### DO IT DIFFERENTLY  
# do something like: reference_chord, required_notes, optional_notes ?
# would need to distinguish between can use required_notes for padding or not?  
# also, return more than 1 possibility? might be useful with some analytics features? bit too complex maybe
# maybe pass a maximal tonal distance between the 2 chords?  