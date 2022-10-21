from MusiStrata.Interfaces.Components import ISong

class IRenderer(object):
    @classmethod
    def Render(cls, song: ISong, outfile: str):
        raise NotImplementedError("{} - Render Method not Implemented", {type(cls)})
