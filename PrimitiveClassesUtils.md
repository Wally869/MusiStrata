---
layout: default
title: PrimitiveClassesUtils
parent: Internals
nav_order: 1
---

# PrimitiveClassesUtils  

## Overview  

This file contains the Record and the Library class.  

The Library class is a sort of object-relational mapping (ORM) to containing a container for elements and specifying convenient filtering.  

The Library class has been implemented for Instruments, Drums and Chords.   


## Records  

Basically an extended Dictionnary. Data is stored in this format for a Library object.

```python
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

```  

## Library  

Converts input elements to Records, stores them, and enables lookup query composition.  

```python
class Library(object):
    BaseName: str = "Library"
    Records: List[Record] = None
    _Fields: List[str] = None

```  

Lookup Queries are handled by the 2 following methods. Extensions of the Library class are based around the concept of wrapping these methods in other methods exposing the fields of interest directly.  


```python
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

    def GetFromFilters(self, filters: List[str]):
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

```
