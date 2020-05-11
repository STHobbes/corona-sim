import json
import numpy as np
import matplotlib.pyplot as plt


def read_data_file(file_name):
    with open(file_name, "r") as data_file:
        return json.load(data_file)


def read_run_set(data_directory, base_file, set_size=10):
    run_set = {'seeded': read_data_file(f'{data_directory}{base_file}.json')}
    for run in range(set_size):
        run_set[f'run {run}'] = read_data_file(
            f'{data_directory}{base_file}_{run}.json')
    return run_set


def plot_run_set(run_set, series, title, events=None,
                 xlabel='days', ylabel='count'):
    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(np.arange(0, 211, 14))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    if events is not None:
        plt.scatter(events[0], events[1])
    for label, data in run_set.items():
        plt.plot(data[series], label=label)
    plt.legend()
    plt.show()
    plt.pause(0.1)


data_dir = './data/expl2/'
# Read the test set for starting the 'stay at home' at different populations
test_set = {
    'no lock down': read_data_file(f'{data_dir}test.json'),
    'lock down @ 200 cases': read_data_file(f'{data_dir}test_200.json'),
    'lock down @ 1000 cases': read_data_file(f'{data_dir}test_1000.json'),
    'lock down @ 2500 cases': read_data_file(f'{data_dir}test_2500.json'),
    'lock down @ 5000 cases': read_data_file(f'{data_dir}test_5000.json')
}

# Read the test run sets for different 'stay at home' Ro values.
report_1_105 = read_run_set(data_dir, 'report_200_reopen_1_105')

report_lock_0_68 = read_run_set(data_dir, 'report_200_lock_0_68')

report_lock_0_85 = read_run_set(data_dir, 'report_200_lock_0_85')

# Plot the run sets for a similar scenarios start. lock down, and reopen
# with different Ro during lock down.
plot_run_set(report_1_105, 'cumulative_cases_series',
             f'Cumulative Cases for Multiple Runs\nlock down Ro=0.51',
             ylabel='cumulative number')

plot_run_set(report_1_105, 'active_cases_series',
             f'Active Cases for Multiple Runs\nlock down Ro=0.51',
             ylabel='daily count')

plot_run_set(report_lock_0_68, 'active_cases_series',
             f'Active Cases for Multiple Runs\nlock down Ro=0.68',
             ylabel='daily count')

plot_run_set(report_lock_0_85, 'active_cases_series',
             f'Active Cases for Multiple Runs\nlock down Ro=0.85',
             ylabel='daily count')

# Plots for various lock down thresholds.
plot_run_set(test_set, 'cumulative_deaths_series',
             f'Cumulative Deaths Simulation\n for various lock down timing',
             ylabel='cumulative deaths')

plot_run_set(test_set, 'active_cases_series',
             f'Active Cases Simulation\n for various lock down and reopen timing',
             ylabel='daily count')

# Plots for various lock down thresholds removing the 'no lock down' case so the
# scaling of the graphs gives us a better idea of what really happens.
del test_set['no lock down']
plot_run_set(test_set, 'cumulative_cases_series',
             f'Cumulative Cases Simulation\n for various lock down timing',
             ylabel='cumulative cases')

plot_run_set(test_set, 'cumulative_deaths_series',
             f'Cumulative Deaths Simulation\n for various lock down timing',
             ylabel='cumulative deaths',
             events=([6, 11, 13, 15, 38, 43, 49, 46],
                     [2, 4, 8, 14, 19, 86, 238, 335]))

plot_run_set(test_set, 'active_cases_series',
             f'Active Cases Simulation\n for various lock down timing',
             ylabel='daily count',
             events=([6, 11, 13, 15, 38, 43, 49, 46],
                     [204, 1066, 2057, 3833, 74, 459, 675, 1084]))
