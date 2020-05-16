from __future__ import annotations

from typing import List


# placeholder for readability. Or can be used?
class Record(object):
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            self.__setattr__(kwarg, kwargs[kwarg])

    def __getitem__(self, item):
        return eval("self.{}".format(item))

    def __str__(self):
        outstr = "Record(" + str(self.__dict__) + ")"
        return outstr

    def __repr__(self):
        return self.__str__()


# Might take queries implementation from generator db to allow more subsetting abilities
class Library(object):
    BaseName: str = "Library"
    Records: List[Record] = None
    _Fields: List[str] = None

    def __init__(self, rawData: List[Dict], nameLibrary: str = None):
        if nameLibrary is not None:
            self.Name = nameLibrary
        else:
            self.Name = self.BaseName

        records = []
        for elem in rawData:
            records.append(
                Record(**elem)
            )
        self.Records = records
        self._Fields = list(rawData[0].keys())

    def __str__(self):
        return str("{}({} Records)".format(self.Name, len(self.Records)))

    def __repr__(self):
        return self.__str__()

    def GetFromValueInField(self, field: str, value: Union[str, int]) -> List[Record]:
        if type(value) == str:
            value = "'" + value + "'"
        found = eval(
            "list(filter(lambda x: x.{} == {}, self.Records))".format(field, value)
        )
        if len(found) == 0:
            print("{} - KeyError: {} not found in {}. Returning default value. \n".format(self.Name, value, field))
            found = [self.Records[0]]
        return found

    def __len__(self):
        return len(self.Records)

    def __getitem__(self, idRecord: int):
        return self.Records[idRecord]

    @property
    def Fields(self):
        return self._Fields

    def GetRecordsFields(self):
        return self._Fields
