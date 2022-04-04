
# Structure Creators
def GenerateBarFromRhythmicPreset(rhythmicPreset: List[Dict[str, Union[float, int]]]) -> Bar:
    """
    :param rhythmicPreset: {
        "Beat": float,
        "Duration": float,
        "NoteName": str (facultative),
        "Octave": int (facultative)
    }
    :return: Bar
    """
    outBar = Bar()
    for rp in rhythmicPreset:
        newEvent = SoundEvent(
            Beat=rp["Beat"],
            Duration=rp["Duration"]
        )

        rpKeys = list(rp.keys())
        if "NoteName" in rpKeys and "Octave" in rpKeys:
            newEvent.Note = Note(
                Name=rp["NoteName"],
                Octave=rp["Octave"]
            )
        outBar.SoundEvents.append(newEvent)

    return outBar
