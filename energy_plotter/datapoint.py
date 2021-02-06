"""
Representation of one point of pulse count data.
"""

import datetime


class DataPoint():
    """
    A single measurement.
    """

    def __init__(self, timestamp=None, pulses=None):
        """
        Create a new point of data.

        :timestamp: datetime representation of the measurement time
        :pulses: number of counted pulses
        """
        self._timestamp = None
        self._pulses = None
        self.timestamp = timestamp
        self.pulses = pulses

    @classmethod
    def from_string(cls, data_str):
        """
        Return a new DataPoint based on a given data string.

        The string mut contain a timestamp (YYYY-mm-dd-HH:mm, e.g.
        "2021-01-29-23:43") and the number of pulses separated with
        whitespace.
        """
        help_str = ("The string mut contain a timestamp (YYYY-mm-dd-HH:mm, "
                    "e.g. '2021-01-29-23:43') and the number of pulses "
                    "separated with whitespace.")
        parts = data_str.split()
        if len(parts) != 2:
            raise ValueError("String '{}' isn't a valid data entry. {}"
                             "".format(data_str, help_str))
        return cls(timestamp=parts[0], pulses=parts[1])

    @property
    def timestamp(self):
        """
        Time of the observation
        """
        if not self._timestamp:
            raise NoValueForAttribute("Timestamp not set")
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp):
        """
        Set a value for the timestamp.

        Timestamp can be provided either as a string in format
        YYYY-MM-DD-hh:mm or directly as a datetime.

        After being set once, the value cannot be altered.
        """
        if self._timestamp:
            raise ImmutableMutationError("Timestamp value has already "
                                         "been set: it cannot be altered.")
        if new_timestamp is None:
            return
        if isinstance(new_timestamp, str):
            self._timestamp = datetime.datetime.strptime(new_timestamp,
                                                         "%Y-%m-%d-%H:%M")
            return
        if isinstance(new_timestamp, datetime.datetime):
            self._timestamp = new_timestamp
            return

        raise ValueError("Illegal timestamp value of type {} encountered."
                         "".format(type(new_timestamp).__name__))

    @property
    def pulses(self):
        """
        Number of pulses.
        """
        if not self._pulses:
            raise NoValueForAttribute("Pulse count number not set")
        return self._pulses

    @pulses.setter
    def pulses(self, new_pulses):
        """
        Set value for observed pulse count.

        The value must be castable to an integer.
        """
        if self._pulses:
            raise ImmutableMutationError("Pulse count value has already "
                                         "been set: it cannot be altered.")
        if new_pulses is None:
            return
        pulses = int(new_pulses)
        if pulses < 0:
            raise ValueError("Pulse count cannot be negative")

        self._pulses = pulses

    def __eq__(self, obj):
        """
        Two DataPoints are considered equal if they are for the same time.
        """
        if not isinstance(obj, self.__class__):
            return False
        return obj._timestamp == self._timestamp

    def __gt__(self, obj):
        if not isinstance(obj, self.__class__):
            raise TypeError("Trying to compare incompatible classes {} and {}"
                            "".format(type(self).__name__, type(obj).__name__))
        if self._timestamp is None or obj._timestamp is None:
            raise NoValueForAttribute("Cannot compare DataPoints without"
                                      "timestamps")
        return self._timestamp > obj._timestamp

    def __lt__(self, obj):
        if not isinstance(obj, self.__class__):
            raise TypeError("Trying to compare incompatible classes {} and {}"
                            "".format(type(self).__name__, type(obj).__name__))
        if self._timestamp is None or obj._timestamp is None:
            raise NoValueForAttribute("Cannot compare DataPoints without"
                                      "timestamps")
        return self._timestamp < obj._timestamp

    def __le__(self, obj):
        return self == obj or self < obj

    def __ge__(self, obj):
        return self == obj or self > obj

    def __hash__(self):
        if self._timestamp is None:
            return 0
        return hash(self._timestamp)


class NoValueForAttribute(Exception):
    """
    Exception for situations when a value is not found for attribute
    """


class ImmutableMutationError(Exception):
    """
    Exception for situations when changing an immutable value is attempted.
    """
