import json
import numpy as np
import matplotlib.pyplot as plt


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
                xlabel='days', ylabel='count'):
    """
    Plot a set of curves

    :param curves: (dict, required) A dictionary of data to plot where the
    key is the label and value is the curve to plot.
    :param title: (str, required) The title for the plot.
    :param xlabel: (str, optional, default='days') The X axis label.
    :param ylabel: (str, optional, default='count') The Y axis label.
    :return: None
    """
    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(np.arange(0, 211, 14))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    for label, data in curves.items():
        plt.plot(data, label=label)
    plt.legend()
    plt.show()
    plt.pause(0.1)


def plot_run_set(run_set, series, title, events=None,
                 xlabel='days', ylabel='count', average=True):
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
    ave = [0 for _ in range(run_set['seeded']['simulation_days'] + 1)]
    for data in run_set.values():
        series_data = data[series]
        for i in range(len(series_data)):
            ave[i] += series_data[i]
    for i in range(len(ave)):
        ave[i] /= len(run_set)

    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(np.arange(0, 211, 14))
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
