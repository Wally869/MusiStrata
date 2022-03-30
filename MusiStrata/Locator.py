from typing import List, Any

from sys import modules



class BaseLocator(object):
    _Registered = {}
    _Instance = None

    def __init__(self):
        if self._Instance is None:
            self.Instance = self

    @staticmethod
    def Instance() -> "Locator":
        #if BaseLocator._Instance is None:
        #    cls._Instance = Locator()
        #return cls._Instance
        return BaseLocator()

    @classmethod
    def Get(cls, key) -> Any:
        return cls.Instance()._Registered[key]

    @classmethod
    def Register(cls, key, value):
        cls.Instance()._Registered[key] = value


class Locator(BaseLocator):
    @classmethod
    def Renderer(cls):
        import NotePlayer
        return NotePlayer
    

