class IRenderer(object):
    @classmethod
    def Render(cls, song: "Song", outfile: str):
        raise NotImplementedError("{} - Render Method not Implemented", {type(cls)})
