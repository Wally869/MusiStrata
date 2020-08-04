---
layout: default
title: Intervals
parent: Components
nav_order: 3
---


# Intervals

## Overview

In Music Theory, the distance between 2 Notes is called an Interval. Intervals are defined by their number, their quality and the distance in terms on semitones.  
Some combinations are considered consonants (i.e. nice sounding) while others are dissonants.  
The use of this class requires some knowledge interval numbers and interval quality, so if you need a refresher [check out Wikipedia.](https://en.wikipedia.org/wiki/Interval_\(music\))

```python
# All Intervals can be found in ALL_INTERVALS, sorted by tonal distance
>> Intervals.ALL_INTERVALS

# Create an Interval object by specifying an Interval Number and a Quality
>> interval = Interval(4, "Perfect")
Interval(4-Augmented--6 semitones)

# An invalid interval definition will throw an error
>> Interval(4, "Major")
KeyError: 'Wrong Inputs: (IntervalNumber: 4, Quality: Major) is not a valid combination for an interval.'

```

## Notes and Intervals

Adding a Note to an Interval returns a tuple (Note, Error).
The error returned is usually None, except if it is not possible to generate the target interval.

In that case the Note returned will be equal to the base note plus the tonal distance of the target interval and the error will be a ValueError displaying the details of the target interval and the generated interval.

The error is returned and not thrown so execution is not interrupted.

```python
>> i = Interval(IntervalNumber=3, Quality="Major")
# Can add interval to a note, returns a tuple (Note, error)
# error is None, except when unable to compute a note from the given starting note and interval
# Here no error since it is possible to create a Major Third from a C note
>> n + i
(Note(E5), None)

>> i2 = Interval(IntervalNumber=2, Quality="Augmented")
# In this case it is not possible to generate an Augmented Second from a C note
# Intervals are linked to a number of semitones, so it returns Note + number of semitones associated with the interval
# and an error as second element of the return tuple (error is very verbose)
>> n + i2
(Note(Ds5), ValueError('Invalid from given starting note. Target: Interval(2-Augmented--3 semitones), Generated: Interval(3-Minor--3 semitones)'))
```
