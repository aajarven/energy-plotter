"""
Tools for reading input data.
"""

import glob
import os


from energy_plotter.datapoint import DataPoint
from energy_plotter.dataset import DataSet


class PulseReader():
    """
    Read pulse count data from files.

    Data from each day is expected to be in a single file, named with the date
    of the data collection in format YYYY-mm-dd (e.g. "2021-01-29.txt"). Each
    line in the file should contain a timestamp (YYYY-mm-dd-HH:mm, e.g.
    "2021-01-29-23:43") and the number of pulses separated with whitespace.
    """

    def __init__(self, datadir):
        """
        Initialize the reader.

        :datadir: location of the data files
        """
        self.datadir = datadir

    def read_day(self, data_day):
        """
        Return the data of a single day.

        :data_day: datetime representation of the target day
        """
        data = DataSet()
        with open(self._data_file(data_day), "r") as data_file:
            for line in data_file:
                data.add(DataPoint.from_string(line))
        return data

    def _data_file(self, data_day):
        """
        Return path to the file containing data for given date.

        Raises a DataNotFound error if no data file is found, or a ValueError
        if more than one data files exist for the given date.

        :data_day: Datetime representation of the target day
        :returns: path to a data file if one is found
        """
        # pylint: disable=no-self-use
        timestamp = data_day.strftime("%Y-%m-%d")
        matching_files = glob.glob(os.path.join(self.datadir,
                                                "{}.*".format(timestamp)))
        if not matching_files:
            raise DataNotFound("Data not found for date {}".format(timestamp))
        if len(matching_files) > 1:
            raise ValueError("More than one data file found for date {}: {}"
                             "".format(timestamp, ", ".join(matching_files)))
        return matching_files[0]


class DataNotFound(ValueError):
    """
    Error for situation where accessing non-existent data is attempted
    """
