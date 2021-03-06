"""
Tests for DataSet
"""

import datetime

import pytest

import conf
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
def pulses_fx():
    """
    Return a list of file pulse counts.
    """
    return [65, 9438, 0, 432, 9]


# pylint: disable=redefined-outer-name

@pytest.fixture
def datapoints_fx(timestamps_fx, pulses_fx):
    """
    Return a list of datapoints for the timestamps from timestamp_fx
    """
    return [DataPoint(timestamp=ts, pulses=p)
            for (ts, p) in zip(timestamps_fx, pulses_fx)]


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


def test_update(datapoints_fx):
    """
    Test adding multiple data points to the set from a list or DataSet
    """
    dset1 = DataSet()
    dset1.update(datapoints_fx)
    assert list(dset1) == datapoints_fx

    dset2 = DataSet()
    dset2.update(dset1)
    assert list(dset2) == datapoints_fx


def test_init_with_data(datapoints_fx):
    """
    Test initializing DataSet with data
    """
    dset = DataSet(datapoints_fx)
    assert list(dset) == datapoints_fx


def test_dataset_timestamps(datapoints_fx, timestamps_fx):
    """
    Test the timestamps property.
    """
    dset = DataSet()
    assert dset.timestamps == []
    dset.update(datapoints_fx)
    assert dset.timestamps == timestamps_fx


def test_dataset_pulses(datapoints_fx, pulses_fx):
    """
    Test the pulses property.
    """
    dset = DataSet()
    assert dset.pulses == []
    dset.update(datapoints_fx)
    assert dset.pulses == pulses_fx


def test_dataset_kwhs(datapoints_fx, pulses_fx):
    """
    Test the kwhs property
    """
    dset = DataSet()
    assert dset.kwhs == []
    dset.update(datapoints_fx)
    assert dset.kwhs == [p * conf.KWH_PER_PULSE for p in pulses_fx]
