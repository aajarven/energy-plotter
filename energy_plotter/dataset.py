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