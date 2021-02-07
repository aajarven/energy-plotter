"""
Tool for plotting data from a time range.
"""

import datetime
import matplotlib.dates
import matplotlib.pyplot as plt

from energy_plotter.data_reader import PulseReader


class Plot():
    """
    Create plots for specific time range.
    """

    def __init__(self, datadir):
        """
        Create a plot tool for data in specific directory.
        """
        self._reader = PulseReader(datadir)

    def day_graph(self, date, outfile):
        """
        Produce a line graph of the energy data for a day.

        Create a line graph for all available data gathered during a single
        day.

        :start: datetime.date of the day for which the plot is created
        :outile: file in which the plot is to be written
        """
        data = self._reader.read_day(date)
        fig, ax = plt.subplots()  # pylint: disable=unused_variable
        ax.plot(data.timestamps, data.kwhs, color="k", linewidth=0.75)
        ax.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=3))
        ax.xaxis.set_minor_locator(matplotlib.dates.HourLocator())
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
        ax.set_xlim([self._day_start(date),
                     self._day_start(date + datetime.timedelta(days=1))])
        ax.set_xlabel("kellonaika")
        ax.set_ylabel("kWh")
        ax.set_title(
                date.strftime("Minuuttikohtainen energiankulutus %d.%m.%Y"))
        plt.savefig(outfile)

    def _day_start(self, date):  # pylint: disable=no-self-use
        return datetime.datetime(date.year, date.month, date.day, 0, 0)
