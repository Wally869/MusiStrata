

import mido
from copy import deepcopy

from .Components import *
from .Instruments import GetSignalFromInstrument


# TYPESTRIPPER - TYPE ALIASES
midoMidiFile = mido.MidiFile
midoMessage = mido.Message


# as default, 480 ticks per beat
TICKS_PER_BEAT = 480


def ConvertSong(song, outfile):
    outMidoSong = mido.MidiFile(type=1)

    # create tempo message here. Maybe put this message in specific channel?
    tempoMessage = mido.MetaMessage(
        "set_tempo",
        tempo=int(mido.tempo2bpm(song.Tempo))
    )

    # NEED A FIX: drums on track 10 so needs another solution if there is a drums track
    idChannel = 0
    for trackData in song.Tracks:
        track = mido.MidiTrack()
        track.append(tempoMessage)

        # need to add alternative bank support for drums track. what value needs to be passed?
        if trackData.IsDrumsTrack:
            realIdChannel = 9

        else:
            if type(trackData.Instrument) == str:
                signal = GetSignalFromInstrument(trackData.Instrument)
            elif type(trackData.Instrument) == int:
                signal = trackData.Instrument
            else:
                raise TypeError("In MidoConverter.ConvertSong: Track Instrument can only be a string name of instrument or an int")
            if idChannel == 9:
                idChannel += 1
            realIdChannel = idChannel

            track.append(
                mido.Message(
                    "control_change", control=0, value=trackData.BankUsed, channel=realIdChannel, time=0
                )
            )
            track.append(
                mido.Message(
                    "control_change", control=32, value=trackData.BankUsed, channel=realIdChannel, time=0
                )
            )

            track.append(
                mido.Message(
                    "program_change", program=signal, channel=realIdChannel, time=0
                )
            )

        prepped = PrepTrack(trackData, song.BeatsPerBar)
        messages = EventsToMido(prepped, realIdChannel)
        for m in messages:
            track.append(m)

        track.append(
            mido.MetaMessage(
                type="end_of_track",
                time=50
            )
        )

        idChannel += 1
        outMidoSong.tracks.append(track)

    outMidoSong.save(outfile)
    return outMidoSong


# first, create all NoteOn and NoteOff structs
# Use NoteOn and NoteOff structs to get time of message
# and compute deltaTime between messages
class NoteOn:
    def __init__(self, time, height, velocity):
        self.Time = time
        self.Height = height
        self.Velocity = velocity

    def GetMessage(self):
        return "note_on"


class NoteOff:
    def __init__(self, time, height):
        self.Time = time
        self.Height = height
        self.Velocity = 0

    def GetMessage(self):
        return "note_off"


def CreateEventsStructs(soundEvent, baseTime, velocity):
    # here using the Note struct defined in Structs.py
    # will have to rewrite all this BS btw, this is getting fucked up
    noteHeight = soundEvent.Note.Height
    noteOnObject = NoteOn(baseTime, noteHeight, velocity)
    deltaTime = soundEvent.Duration * TICKS_PER_BEAT
    noteOffObject = NoteOff(baseTime + deltaTime, noteHeight)
    return noteOnObject, noteOffObject


def ConvertNoteStructToMidoMessage(noteStruct, deltaTime, channelId):
    # Note Off is a special case of Note On, with 0 velocity
    # So don't even need to make a difference?
    outMessage = mido.Message(
        noteStruct.GetMessage(),
        note=noteStruct.Height,
        velocity=noteStruct.Velocity,
        time=int(deltaTime),
        channel=channelId
    )
    return outMessage


def PrepTrack(track, nbBeatsPerBar):
    events = []
    startTick = 50

    for id_bar in range(len(track.Bars)):
        timeBar = int(startTick + id_bar * nbBeatsPerBar * TICKS_PER_BEAT)
        currBar = track.Bars[id_bar]
        for soundEvent in currBar.SoundEvents:
            noteon, noteoff = CreateEventsStructs(
                soundEvent,
                timeBar + soundEvent.Beat * TICKS_PER_BEAT,
                soundEvent.Velocity
            )
            events += [noteon, noteoff]

    """
    events.append(
        mido.MetaMessage(
            "end_of_track",
            50
        )
    )
    """

    return events


def EventsToMido(events, channelId):
    # sort by time
    events.sort(key=lambda x: x.Time, reverse=False)

    messages = []
    for id_event in range(0, len(events)):
        timedelta = events[id_event].Time
        if id_event > 0:
            timedelta -= events[id_event - 1].Time
        messages.append(
            ConvertNoteStructToMidoMessage(
                events[id_event],
                timedelta,
                channelId
            )
        )

    return messages
