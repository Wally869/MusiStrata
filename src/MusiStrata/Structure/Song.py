from typing import List, Tuple, Dict, Union
from typing_extensions import Self

from dataclasses import dataclass, field

from .Track import Track

@dataclass
class Song:
    Tempo: int = 80
    BeatsPerBar: int = 4
    Tracks: List[Track] = field(default_factory=list)

    def __str__(self):
        return "Song(Tempo={}, BeatsPerBar={}, {} Tracks)".format(
            self.Tempo, self.BeatsPerBar, len(self.Tracks)
        )

    def ToDict(self) -> Dict:
        dictRepr = {
            "Tempo": self.Tempo,
            "BeatsPerBar": self.BeatsPerBar,
            "Tracks": [t.ToDict() for t in self.Tracks],
        }
        return dictRepr

    def ToJSON(self) -> str:
        from json import dumps as _dumps

        return _dumps(self.ToDict())

    @classmethod
    def FromDict(cls, dictRepr: Dict):
        return Song(
            Tempo=dictRepr["Tempo"],
            BeatsPerBar=dictRepr["BeatsPerBar"],
            Tracks=[Track.FromDict(elem) for elem in dictRepr["Tracks"]],
        )

    @classmethod
    def FromJSON(cls, jsonData: str):
        from json import loads as _loads

        dictRepr = _loads(jsonData)
        return cls.FromDict(dictRepr)
