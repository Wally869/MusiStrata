

# Creating pseudo enum that work with Transcrypt

"""
ALL_NOTES = [
    "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"
]

class test(EnumManager_Ordered_Looping):
    KeyValuesMap={ALL_NOTES[i]: i for i in range(len(ALL_NOTES))}
    KeyList=ALL_NOTES
    ValuesList=[i for i in range(len(ALL_NOTES))]

"""

class EnumElement(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class EnumManager(object):
    KeyValuesMap = None
    KeyList = None
    ValuesList = None
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "<{} - name: {}, value: {}>".format(self.__class__, self.name, self.value) 

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self.KeyValuesMap[self.name]

    def GetElementFromValue(self, value):
        for key in self.KeyList:
            if self.KeyValuesMap[key] == value:
                return self.__class__(key)
        return None


class EnumManager_Ordered(EnumManager):
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


class EnumManager_Ordered_Looping(EnumManager_Ordered):
    def __add__(self, other):
        if other < 0:
            return self - other
        newValue = self.value + other
        deltaRange = 0
        while newValue >= len(self.KeyList):
            newValue -= len(self.KeyList)
            deltaRange += 1
        return self.__class__(self.KeyList[newValue]), deltaRange
    
    def __sub__(self, other):
        if other < 0:
            return self + other
        newValue = self.value - other
        deltaRange = 0
        while newValue < 0:
            newValue += len(self.KeyList)
            deltaRange -= 1
        return self.__class__(self.KeyList[newValue]), deltaRange

