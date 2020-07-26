


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


class Library(object):
    BaseName = "Library"
    Records = None
    _Fields = None

    def __init__(self, rawData, nameLibrary = None):
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

    def GetFromValueInField(self, field, value):
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

    def __getitem__(self, idRecord):
        return self.Records[idRecord]

    @property
    def Fields(self):
        return self._Fields

    def GetRecordsFields(self):
        return self._Fields

    def GetFromFilters(self, filters):
        """
        filters must be in the form (field, operator, value) as strings
        """
        strQuery = ""
        for id, fil in enumerate(filters):
            strQuery += "x.{} {} {}".format(*fil)
            if id < len(filters) - 1:
                strQuery += " and "
        return list(
            filter(
                lambda x: eval(strQuery),
                self.Records
            )
        )

    def GetAllValuesFromField(self, field):
        return [rec[field] for rec in self.Records]
