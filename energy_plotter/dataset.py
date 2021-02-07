"""
A class for pulse count data.
"""

from sortedcontainers import SortedSet

from energy_plotter.datapoint import DataPoint


class DataSet(SortedSet):   # pylint: disable=too-many-ancestors
    """
    A container class for storing pulse count data.

    The dataset is ordered by timestamp of the observation and cannot contain
    duplicate measurements.
    """

    def add(self, value):
        """
        Add a new DataPoint to the dataset.
        """
        if not isinstance(value, DataPoint):
            raise TypeError("DataSet can only be used with DataPoints")
        super().add(value)

    @property
    def timestamps(self):
        """
        Return a list of all the timestmaps in the dataset.
        """
        return [dp.timestamp for dp in self]

    @property
    def pulses(self):
        """
        Return a list of all the pulse counts in the dataset.
        """
        return [dp.pulses for dp in self]

    @property
    def kwhs(self):
        """
        Return a list of kwh measurements in the dataset.
        """
        return [dp.kwh for dp in self]
