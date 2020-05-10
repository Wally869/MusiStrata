from enum import Enum


# Can do some work to extend enums?
class ExtendedEnum(Enum):
    @classmethod
    def GetAllElements(cls):
        # return [c for c in cls]
        return list(cls._member_map_.values())

    @classmethod
    def GetAllNames(cls):
        # return [c.name for c in cls]
        return cls._member_names_

    @classmethod
    def GetAllValues(cls):
        return [c.value for c in cls]

    @classmethod
    def GetElementFromName(cls, name: str):
        # raise KeyError("Element not in Enum.")
        try:
            return cls._member_map_[name]
        except KeyError:
            raise KeyError("Element not in Enum")

    @classmethod
    def GetElementFromValue(cls, value):
        for c in cls:
            if c.value == value:
                return c
        raise KeyError("Value not in Enum.")

    def GetPosition(self):
        allElems = self.GetAllElements()
        for idItem in range(len(allElems)):
            if allElems[idItem].name == self.name:
                return idItem


class OrderedEnum(ExtendedEnum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @classmethod
    def FindNameForValue(cls, val):
        for c in cls:
            if c.value == val:
                return c.name
        raise ValueError("Value not in {}".format(cls))


class LoopingOrderedEnum(OrderedEnum):
    def __add__(self, other: int):
        if type(other) != int:
            return NotImplemented

        if other < 0:
            return self.__sub__(
                abs(other)
            )

        nbLoops = 0

        nbElements = len(self.GetAllElements())

        # replace by self.value
        # currId = self.GetPosition() - other
        currId = self.value + other

        while currId >= nbElements:
            currId -= nbElements
            nbLoops += 1

        return self.GetAllElements()[currId], nbLoops

    def __sub__(self, other):
        # Order-dependent implementation of __sub__ if objects of same class
        if self.__class__ is other.__class__:
            outValue = self.value - other.value
            if outValue < 0:
                outValue += len(self.GetAllElements())

            return outValue

        elif type(other) == int:
            if other < 0:
                return self.__add__(
                    abs(other)
                )

            nbLoops = 0
            nbElements = len(self.GetAllElements())

            # currId = self.GetPosition() - other
            currId = self.value - other

            while currId < 0:
                currId += nbElements
                nbLoops -= 1

            return self.GetAllElements()[currId], nbLoops

        else:
            return NotImplemented
