import json
import numpy as np
import matplotlib.pyplot as plt
import simulate as s


def read_data_file(file_name):
    """
    Read a JSON data file produced by a simulation

    :param file_name: (str, required) The file name.
    :return: (dict)The JSON data as a dictionary.
    """
    with open(file_name, "r") as data_file:
        return json.load(data_file)


def read_run_set(data_directory, base_file, set_size=10):
    """
    Reads a set of JSON data files from a run. Typically a run includes a seeded
    reference run and 10 additional random runs.

    :param data_directory: (str, required) The data directory (include the trailing'/'
    :param base_file: (str, required) The base name for the file with no extension.
    :param set_size: (int, optional, default=10) The number of random runs in the set
    in addition to the seeded run.
    :return: (dict) a dictionary containing the set of runs where the key is the label
    for the run, and the value is the data from the run.
    """
    run_set = {'seeded': read_data_file(f'{data_directory}{base_file}.json')}
    for run in range(set_size):
        run_set[f'run {run}'] = read_data_file(
            f'{data_directory}{base_file}_{run}.json')
    return run_set


def plot_curves(curves, title,
                xlabel='days', ylabel='count', hilight=2):
    """
    Plot a set of curves

    :param curves: (dict, required) A dictionary of data to plot where the
    key is the label and value is the curve to plot.
    :param title: (str, required) The title for the plot.
    :param xlabel: (str, optional, default='days') The X axis label.
    :param ylabel: (str, optional, default='count') The Y axis label.
    :param hilight: (int, optional, default=1) The Y axis label.
    :return: None
    """
    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    max_len = 0
    for label, data in curves.items():
        if len(data) > max_len:
            max_len = len(data)
    tic_spacing = 14 if max_len <= 212 else 28
    plt.xticks(np.arange(0, max_len, tic_spacing))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    z = 1000
    width = hilight
    for label, data in curves.items():
        plt.plot(data, label=label, zorder=z, linewidth=width)
        width = 2
        z -= 50
    plt.legend()
    plt.show()
    plt.pause(0.1)


def plot_run_set_series(run_set, series, title_template, events=None,
                        xlabel='days', average=True):
    """
    Plot some series from all of the runs in the set.

    :param run_set: (dict, required) a dictionary containing the set of runs where
    the key is the label for the run, and the value is the data from the run.
    :param series: (str, required) The name of the series to be plotted.
    :param title: (str, required) The title for the plot.
    :param events: (dict, {label: ([x1,x2,...],[y1,y2,...])}, optional, default=None) Events
    to be plotted on the graph.
    :param xlabel: (str, optional, default='days') The X axis label.
    :param ylabel: (str, optional, default='count') The Y axis label.
    :return: (list) the average for the plotted series.
    """

    # compute the average - this gets returned even if it doesn't
    # get plotted.
    ave = [0 for _ in range(run_set['seeded'][s.SIMULATION_DAYS] + 1)]
    for data in run_set.values():
        series_data = data[series]
        for i in range(len(series_data)):
            ave[i] += series_data[i]
    for i in range(len(ave)):
        ave[i] /= len(run_set)

    # figure out the axis and grid. If a simulation is extended or
    # shortened, we need to adjust the grid accordingly - specifically
    # we are talking about the X or duration grid. Grid lines in weeks
    # are pretty intuitive, if they get too dense, that's a problem:
    #     tic_spacing - generally, 2 weeks (14 days) is good - but -
    #     if the simulation length gets too long we need to adjust that
    #     to a wider/narrower interval so the presentation makes sense
    plt.clf()
    plt.title(title_template.format(series.title()))
    plt.xlabel(xlabel)
    plt.ylabel(series)
    tic_spacing = 14 if run_set['seeded'][s.SIMULATION_DAYS] <= 211 else 28
    plt.xticks(np.arange(0, run_set['seeded'][s.SIMULATION_DAYS], tic_spacing))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    if events is not None:
        for label, data in events.items():
            plt.scatter(data[0], data[1], label=label)
    for label, data in run_set.items():
        plt.plot(data[series], label=label)
    if average:
        plt.plot(ave, color='black', label='average', linewidth=3)
    plt.legend()
    plt.show()
    plt.pause(0.1)
    return ave
