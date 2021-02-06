"""
Tests for DataReader class.
"""

import datetime

import pytest

from energy_plotter.data_reader import PulseReader, DataNotFound
from energy_plotter.datapoint import DataPoint


@pytest.fixture()
def reader_fx():
    """
    Data reader for the test data directory
    """
    return PulseReader("tests/data")

# pylint: disable=redefined-outer-name


def test_read_day(reader_fx):
    """
    Test that read_day returns correct number of data points from the file and
    has read the first, last and one intermittent data point correctly.

    Equality of data points is determined based on the timestamp only, so the
    pulse count must be verified manually.
    """
    data = reader_fx.read_day(datetime.date(2021, 2, 4))
    assert len(data) == 24 * 60

    first_dp = DataPoint(timestamp=datetime.datetime(2021, 2, 4, 0, 0),
                         pulses=1810)
    nth_dp = DataPoint(timestamp=datetime.datetime(2021, 2, 4, 18, 10),
                       pulses=2270)
    last_dp = DataPoint(timestamp=datetime.datetime(2021, 2, 4, 23, 59),
                        pulses=3082)

    assert data.index(first_dp) == 0
    assert data[0].pulses == first_dp.pulses

    nth_index = data.index(nth_dp)
    assert nth_index > 0
    assert data[nth_index].pulses == nth_dp.pulses

    last_index = data.index(last_dp)
    assert last_index > 0
    assert data[last_index].pulses == last_dp.pulses


def test_read_nonexistent_day(reader_fx):
    """
    Test that a DataNotFound error is raised when data file doesn't exist.
    """
    with pytest.raises(DataNotFound):
        reader_fx.read_day(datetime.date(2020, 2, 1))


def test_read_ambiguous_file(reader_fx):
    """
    Test that a ValueError is raised when ambiguous data is requested.

    Such an error must be raised when there are more than one file for a date:
    in this case a txt file and a csv.
    """
    with pytest.raises(ValueError) as err:
        reader_fx.read_day(datetime.date(2020, 2, 5))
    assert "More than one data file found for date" in str(err.value)
