"""
Tests for DataReader class.
"""

import datetime

import pytest

from energy_plotter.data_reader import PulseReader
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
    Test that read_day returns correct number of data points from the file
    """
    data = reader_fx.read_day(datetime.date(2021, 2, 4))
    assert len(data) == 24 * 60
