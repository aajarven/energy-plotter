"""
Tests for DataSet
"""

import datetime

import pytest

from energy_plotter.datapoint import DataPoint
from energy_plotter.dataset import DataSet


@pytest.fixture
def timestamps_fx():
    """
    Return a list of five timestamps, earliest of them first in the list.
    """
    return [datetime.datetime(2020, 6, 8, 10, 11),
            datetime.datetime(2020, 6, 9, 8, 50),
            datetime.datetime(2021, 1, 28, 00, 14),
            datetime.datetime(2021, 1, 28, 00, 15),
            datetime.datetime(2021, 1, 28, 1, 0)]

@pytest.fixture
def datapoints_fx(timestamps_fx):
    """
    Return a list of datapoints for the timestamps from timestamp_fx
    """
    return [DataPoint(timestamp=ts, pulses=8) for ts in timestamps_fx]

# pylint: disable=redefined-outer-name


def test_one_element(datapoints_fx):
    """
    Test creating an empty DataSet and adding one element to it.
    """
    dset = DataSet()
    assert len(dset) == 0

    dset.add(datapoints_fx[0])
    assert len(dset) == 1
    assert dset[0] == datapoints_fx[0]


def test_add_wrong_type_element(timestamps_fx):
    """
    Ensure that DataSet raises a TypeError when wrong type data is added
    """
    dset = DataSet()
    with pytest.raises(TypeError):
        dset.add(timestamps_fx[0])


def test_dataset_ordering(datapoints_fx):
    """
    Check that data points are in timestamp order even if not added that way.
    """
    dset = DataSet()
    input_order = [2, 4, 1, 0, 3]
    for index in input_order:
        dset.add(datapoints_fx[index])
    assert list(dset) == datapoints_fx
