"""
Tests for DataPoint
"""

import datetime

import pytest

from energy_plotter.datapoint import (DataPoint, NoValueForAttribute,
                                      ImmutableMutationError)


def test_datapoint_pulses():
    """
    Test creating a data point with set pulse count.
    """
    datapoint = DataPoint(pulses=9)
    assert datapoint.pulses == 9


def test_datapoint_timestamp():
    """
    Test creating a data point with set timestamp.
    """
    timestamp = datetime.datetime(2020, 11, 28, 18, 45)
    datapoint = DataPoint(timestamp=timestamp)
    assert datapoint.timestamp == timestamp


def test_datapoint_timestamp_string():
    """
    Test that providing a timestamp as a string sets the timestamp correctly.
    """
    timestamp = datetime.datetime(2020, 11, 28, 18, 45)
    datapoint = DataPoint(timestamp="2020-11-28-18:45")
    assert datapoint.timestamp == timestamp


def test_illegal_timestamp_type():
    """
    Test that giving an illegal type timestamp raises an error
    """
    datapoint = DataPoint()
    with pytest.raises(ValueError):
        datapoint.timestamp = 2020


def test_pulses_from_string():
    """
    Ensure that pulses can be parsed from a string
    """
    datapoint = DataPoint(pulses="5")
    assert datapoint.pulses == 5


def test_negative_pulses():
    """
    Check that negative values for pulses are not accepted
    """
    datapoint = DataPoint()
    with pytest.raises(ValueError):
        datapoint.pulses = -1


def test_fetch_unset_pulses():
    """
    Ensure that trying to access unset pulses raises an error.
    """
    datapoint = DataPoint()
    with pytest.raises(NoValueForAttribute):
        datapoint.pulses  # pylint: disable=pointless-statement


def test_fetch_unset_timestamp():
    """
    Ensure that trying to access unset pulses raises an error.
    """
    datapoint = DataPoint()
    with pytest.raises(NoValueForAttribute):
        datapoint.timestamp  # pylint: disable=pointless-statement


def test_immutable_pulses():
    """
    Ensure that pulses cannot be altered after setting.
    """
    datapoint = DataPoint(pulses=9)
    with pytest.raises(ImmutableMutationError):
        datapoint.pulses = 7


def test_immutable_timestamp():
    """
    Ensure that timestamp cannot be altered after setting.
    """
    timestamp = datetime.datetime(2020, 11, 28, 18, 45)
    datapoint = DataPoint(timestamp)
    with pytest.raises(ImmutableMutationError):
        datapoint.timestamp = "2021-02-01"


def test_datapoint_from_string():
    """
    Test initializing datapoint based on a string.
    """
    datapoint = DataPoint.from_string("2021-01-30-23:43\t1558")
    assert datapoint.pulses == 1558
    assert datapoint.timestamp == datetime.datetime(2021, 1, 30, 23, 43)

    datapoint = DataPoint.from_string("2021-01-30-23:43   1558")
    assert datapoint.pulses == 1558
    assert datapoint.timestamp == datetime.datetime(2021, 1, 30, 23, 43)


def test_illegal_datapoint_string():
    """
    Test that an exception is raised when datapoint string doesn't have both
    datetime and pulse count
    """
    with pytest.raises(ValueError) as err:
        # pylint: disable=unused-variable
        datapoint = DataPoint.from_string("2021-01-30-23:43   ")  # noqa: F841
    assert "isn't a valid data entry" in str(err.value)
