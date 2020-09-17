import csv
import expl_tools as tools
import numpy as np
import simulate as s
import matplotlib.pyplot as plt

US_HEADER_ROWS = 3
US_REAL_DATE = 0
US_DAY_OF_YEAR = US_REAL_DATE + 1
US_JH_DAY = US_DAY_OF_YEAR + 1
US_JH_DAILY_NEW = US_JH_DAY + 1
US_JH_CUMULATIVE = US_JH_DAILY_NEW + 1
US_JH_DAILY_NEW_7_DAY = US_JH_CUMULATIVE + 1
US_JH_DEATHS = US_JH_DAILY_NEW_7_DAY + 1


# def plot_set_series(run_set, series, title, xlabel='days',
#                     ylabel='count', legend_loc='upper left'):
#     """
#     Plot some series from all of the runs in the set.
#
#     :param run_set: (dict, required) a dictionary containing the set of runs where
#     the key is the label for the run, and the value is the data from the run.
#     :param series: (str, required) The name of the series to be plotted.
#     :param title: (str, required) The title for the plot.
#     :param events: (dict, {label: ([x1,x2,...],[y1,y2,...])}, optional, default=None) Events
#     to be plotted on the graph.
#     :param xlabel: (str, optional, default='days') The X axis label.
#     """
#
#     # figure out the axis and grid. If a simulation is extended or
#     # shortened, we need to adjust the grid accordingly - specifically
#     # we are talking about the X or duration grid. Grid lines in weeks
#     # are pretty intuitive, if they get too dense, that's a problem:
#     #     tic_spacing - generally, 2 weeks (14 days) is good - but -
#     #     if the simulation length gets too long we need to adjust that
#     #     to a wider/narrower interval so the presentation makes sense
#     plt.clf()
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     for label, data in run_set.items():
#         tic_spacing = 14 if data['simulation_days'] <= 211 else 28
#         plt.xticks(np.arange(0, data['simulation_days'], tic_spacing))
#         break
#     plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
#     herd_start = []
#     heard_value = []
#     for label, data in run_set.items():
#         max_new_day = data['max_new_daily_cases_day']
#         herd_start.append(max_new_day)
#         heard_value.append(data[series][max_new_day])
#         plt.plot(data[series], label=label)
#     plt.scatter(herd_start, heard_value, label='herd immunity')
#     plt.legend(loc=legend_loc)
#     plt.show()
#     plt.pause(0.1)
#     return
#
#
# def average_runs(ref_run, *runs):
#     days = ref_run['simulation_days']
#     ref_run['max_new_daily_cases_day'] = 0
#     for day in range(days + 1):
#         for run in runs:
#             ref_run['cumulative_cases_series'][day] += run['cumulative_cases_series'][day]
#             ref_run['daily_new_cases_series'][day] += run['daily_new_cases_series'][day]
#             ref_run['cumulative_deaths_series'][day] += run['cumulative_deaths_series'][day]
#         ref_run['cumulative_cases_series'][day] /= (len(runs) + 1)
#         ref_run['daily_new_cases_series'][day] /= (len(runs) + 1)
#         ref_run['cumulative_deaths_series'][day] /= (len(runs) + 1)
#         if ref_run['daily_new_cases_series'][day] > ref_run['daily_new_cases_series'][
#             ref_run['max_new_daily_cases_day']]:
#             ref_run['max_new_daily_cases_day'] = day
#     # for run in runs:
#     #     ref_run['max_new_daily_cases_day'] += run['max_new_daily_cases_day']
#     # ref_run['max_new_daily_cases_day'] = int(ref_run['max_new_daily_cases_day'] / (len(runs) + 1))
#
#
def characterize_phases(run_set):
    phase_summaries = {}
    for data in run_set.values():
        for key, phase in data['phases'].items():
            phase_summary = phase_summaries.get(key, None)
            if phase_summary is None:
                phase_summary = {}
                phase_summaries[key] = phase_summary
                phase_summary['start_day'] = phase['start_day']
                phase_summary['confirmed_new'] = data[s.NEW_CONFIRMED_CASES_SERIES][phase['start_day']]
                phase_summary['confirmed_cumulative'] = data[s.CUMULATIVE_CONFIRMED_CASES_SERIES][phase['start_day']]
                phase_summary['deaths'] = data[s.CUMULATIVE_DEATHS_SERIES][phase['start_day']]
            else:
                phase_summary['start_day'] += phase['start_day']
                phase_summary['confirmed_new'] += data[s.NEW_CONFIRMED_CASES_SERIES][phase['start_day']]
                phase_summary['confirmed_cumulative'] += data[s.CUMULATIVE_CONFIRMED_CASES_SERIES][phase['start_day']]
                phase_summary['deaths'] += data[s.CUMULATIVE_DEATHS_SERIES][phase['start_day']]

    for key, phase_summary in phase_summaries.items():
        print(f'{key}:')
        print(f'  start day:            {phase_summary["start_day"] / len(run_set)}')
        print(f'  confirmed daily new:  {phase_summary["confirmed_new"] / len(run_set)}')
        print(f'  cumulative confirmed: {phase_summary["confirmed_cumulative"] / len(run_set)}')
        print(f'  cumulative deaths:    {phase_summary["deaths"] / len(run_set)}')


data_dir = './data/simple_v3/'


# us_set = tools.read_run_set(data_dir, 'us_3280K', 5)
us_set_lock = tools.read_run_set(data_dir, 'us_3280K_lock', 10)
us_set_restart = tools.read_run_set(data_dir, 'us_3280K_restart', 10)
# us_set_restrict_school = tools.read_run_set(data_dir, 'us_3280K_restrict_schl', 5)
characterize_phases(us_set_lock)

us_daily_new = []
us_daily_new_7_day = []
us_cumulative = []
us_deaths = []
with open('./data/us/US.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    row_index = 0
    for row in reader:
        row_index += 1
        if row_index <= US_HEADER_ROWS:
            # skip the header rows
            continue

        if '' != row[US_JH_DAILY_NEW]:
            us_daily_new.append(int(row[US_JH_DAILY_NEW]) / 100)
        if '' != row[US_JH_DAILY_NEW_7_DAY]:
            us_daily_new_7_day.append(int(row[US_JH_DAILY_NEW_7_DAY]) / 100)
        if '' != row[US_JH_CUMULATIVE]:
            us_cumulative.append(int(row[US_JH_CUMULATIVE]) / 100)
        if '' != row[US_JH_DEATHS]:
            us_deaths.append(int(row[US_JH_DEATHS]) / 100)


# title_template = '{} Simulation, pop: 3,280,000'
# ave_new_cases = tools.plot_run_set_series(
#     us_set, s.NEW_CASES_SERIES, title_template)
#
# ave_new_confirmed_cases = tools.plot_run_set_series(
#     us_set, s.NEW_CONFIRMED_CASES_SERIES, title_template)
#
# ave_hospitalizations = tools.plot_run_set_series(
#     us_set, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)
#
# ave_cases = tools.plot_run_set_series(
#     us_set, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)
#
# ave_deaths = tools.plot_run_set_series(
#     us_set, s.CUMULATIVE_DEATHS_SERIES, title_template)

title_template = '{} Simulation, 2nd Wave Lock Down pop: 3,280,000'
ave_new_cases_lock = tools.plot_run_set_series(
    us_set_lock, s.NEW_CASES_SERIES, title_template)

ave_new_confirmed_cases_lock = tools.plot_run_set_series(
    us_set_lock, s.NEW_CONFIRMED_CASES_SERIES, title_template)

ave_hospitalizations_lock = tools.plot_run_set_series(
    us_set_lock, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)

ave_cases_lock = tools.plot_run_set_series(
    us_set_lock, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)

ave_deaths_lock = tools.plot_run_set_series(
    us_set_lock, s.CUMULATIVE_DEATHS_SERIES, title_template)

title_template = '{} Simulation, 2nd Wave Restriction pop: 3,280,000'
ave_new_cases_restrict = tools.plot_run_set_series(
    us_set_restart, s.NEW_CASES_SERIES, title_template)

ave_new_confirmed_cases_restrict = tools.plot_run_set_series(
    us_set_restart, s.NEW_CONFIRMED_CASES_SERIES, title_template)

ave_hospitalizations_restrict = tools.plot_run_set_series(
    us_set_restart, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)

ave_cases_restrict = tools.plot_run_set_series(
    us_set_restart, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)

ave_deaths_restrict = tools.plot_run_set_series(
    us_set_restart, s.CUMULATIVE_DEATHS_SERIES, title_template)

# title_template = '{} Simulation, 2nd Wave Restriction,\nschool reopen day 175, pop: 3,280,000'
# ave_new_cases_restrict_school = tools.plot_run_set_series(
#     us_set_restrict_school, s.NEW_CASES_SERIES, title_template)
#
# ave_new_confirmed_cases_restrict_school = tools.plot_run_set_series(
#     us_set_restrict_school, s.NEW_CONFIRMED_CASES_SERIES, title_template)
#
# ave_hospitalizations_restrict_school = tools.plot_run_set_series(
#     us_set_restrict_school, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)
#
# ave_cases_restrict_school = tools.plot_run_set_series(
#     us_set_restrict_school, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)
#
# ave_deaths_restrict_school = tools.plot_run_set_series(
#     us_set_restrict_school, s.CUMULATIVE_DEATHS_SERIES, title_template)

new_cases_confirmed_set = {
    'actual new cases, Johns Hopkins University': us_daily_new_7_day,
    # 'unrestricted reopen, Re=1.56': ave_new_confirmed_cases,
    "masks restrictions": ave_new_confirmed_cases_lock,
    "restart": ave_new_confirmed_cases_restrict
    # "wear masks, open schools at 175": ave_new_confirmed_cases_restrict_school
}
tools.plot_curves(new_cases_confirmed_set, 'Best and Worst New Confirmed Cases Scenarios', hilight=4)

cumulative_cases_set = {
    'actual cases, Johns Hopkins University': us_cumulative,
    # 'unrestricted reopen, Re=1.56': ave_cases,
    "masks restrictions": ave_cases_lock,
    "restart": ave_cases_restrict
    # "wear masks, open schools at 175": ave_cases_restrict_school
}
tools.plot_curves(cumulative_cases_set, 'Best and Worst Cumulative Cases Scenarios', hilight=4)

cumulative_deaths_set = {
    'actual deaths, Johns Hopkins University': us_deaths,
    # 'unrestricted reopen, Re=1.56': ave_deaths,
    "masks restrictions": ave_deaths_lock,
    "restart": ave_deaths_restrict
    # "wear masks, open schools at 175": ave_deaths_restrict_school
}
tools.plot_curves(cumulative_deaths_set, 'Best and Worst Cumulative Deaths Scenarios', hilight=4)

hospitalizations_set = {
    # 'unrestricted reopen, Re=1.56': ave_hospitalizations,
    "masks restrictions": ave_hospitalizations_lock,
    "restart": ave_hospitalizations_restrict
    # "wear masks, open schools at 175": ave_hospitalizations_restrict_school
}
tools.plot_curves(hospitalizations_set, 'Best and Worst Hospitalizations Scenarios')
