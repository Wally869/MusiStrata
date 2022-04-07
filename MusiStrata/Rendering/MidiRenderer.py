from MusiStrata.Interfaces import IRenderer

from MusiStrata.Components import Song


class MidiRenderer(IRenderer):
    @classmethod
    def Render(cls, song: Song, outfile: str):
        from .MidoConverter import ConvertSong

        ConvertSong(song, outfile)
