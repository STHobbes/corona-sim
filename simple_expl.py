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
US_JH_CALC_DAILY_NEW = US_JH_DAILY_NEW + 1
US_JH_CUMULATIVE = US_JH_CALC_DAILY_NEW + 1
US_JH_DAILY_NEW_7_DAY = US_JH_CUMULATIVE + 1
US_JH_DEATHS = US_JH_DAILY_NEW_7_DAY + 1


def plot_set_series(run_set, series, title, xlabel='days',
                    ylabel='count', legend_loc='upper left'):
    """
    Plot some series from all of the runs in the set.

    :param run_set: (dict, required) a dictionary containing the set of runs where
    the key is the label for the run, and the value is the data from the run.
    :param series: (str, required) The name of the series to be plotted.
    :param title: (str, required) The title for the plot.
    :param events: (dict, {label: ([x1,x2,...],[y1,y2,...])}, optional, default=None) Events
    to be plotted on the graph.
    :param xlabel: (str, optional, default='days') The X axis label.
    """

    # figure out the axis and grid. If a simulation is extended or
    # shortened, we need to adjust the grid accordingly - specifically
    # we are talking about the X or duration grid. Grid lines in weeks
    # are pretty intuitive, if they get too dense, that's a problem:
    #     tic_spacing - generally, 2 weeks (14 days) is good - but -
    #     if the simulation length gets too long we need to adjust that
    #     to a wider/narrower interval so the presentation makes sense
    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for label, data in run_set.items():
        tic_spacing = 14 if data['simulation_days'] <= 211 else 28
        plt.xticks(np.arange(0, data['simulation_days'], tic_spacing))
        break
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    herd_start = []
    heard_value = []
    for label, data in run_set.items():
        max_new_day = data['max_new_daily_cases_day']
        herd_start.append(max_new_day)
        heard_value.append(data[series][max_new_day])
        plt.plot(data[series], label=label)
    plt.scatter(herd_start, heard_value, label='herd immunity')
    plt.legend(loc=legend_loc)
    plt.show()
    plt.pause(0.1)
    return


def average_runs(ref_run, *runs):
    days = ref_run['simulation_days']
    ref_run['max_new_daily_cases_day'] = 0
    for day in range(days + 1):
        for run in runs:
            ref_run['cumulative_cases_series'][day] += run['cumulative_cases_series'][day]
            ref_run['daily_new_cases_series'][day] += run['daily_new_cases_series'][day]
            ref_run['cumulative_deaths_series'][day] += run['cumulative_deaths_series'][day]
        ref_run['cumulative_cases_series'][day] /= (len(runs) + 1)
        ref_run['daily_new_cases_series'][day] /= (len(runs) + 1)
        ref_run['cumulative_deaths_series'][day] /= (len(runs) + 1)
        if ref_run['daily_new_cases_series'][day] > ref_run['daily_new_cases_series'][
            ref_run['max_new_daily_cases_day']]:
            ref_run['max_new_daily_cases_day'] = day
    # for run in runs:
    #     ref_run['max_new_daily_cases_day'] += run['max_new_daily_cases_day']
    # ref_run['max_new_daily_cases_day'] = int(ref_run['max_new_daily_cases_day'] / (len(runs) + 1))


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


data_dir = './data/simple_v2/'

# ro_set = {
#     'Ro = 6.00': tools.read_data_file(f'{data_dir}Ro6_00_328000.json'),
#     'Ro = 4.50': tools.read_data_file(f'{data_dir}Ro4_50_328000.json'),
#     'Ro = 3.00': tools.read_data_file(f'{data_dir}Ro3_00_328000.json'),
#     'Ro = 2.00': tools.read_data_file(f'{data_dir}Ro2_00_328000.json'),
#     'Ro = 1.50': tools.read_data_file(f'{data_dir}Ro1_50_328000.json'),
#     'Ro = 1.30': tools.read_data_file(f'{data_dir}Ro1_30_328000.json'),
#     'Ro = 1.20': tools.read_data_file(f'{data_dir}Ro1_20_328000.json'),
#     'Ro = 1.10': tools.read_data_file(f'{data_dir}Ro1_10_328000.json')
# }
# ro_subset = {
#     'Ro = 1.10': ro_set['Ro = 1.10'],
#     'Ro = 1.05': tools.read_data_file(f'{data_dir}Ro1_05_328000.json'),
#     'Ro = 1.00': tools.read_data_file(f'{data_dir}Ro1_00_328000.json'),
#     'Ro = 0.95': tools.read_data_file(f'{data_dir}Ro0_95_328000.json'),
#     'Ro = 0.90': tools.read_data_file(f'{data_dir}Ro0_90_328000.json'),
#     'Ro = 0.80': tools.read_data_file(f'{data_dir}Ro0_80_328000.json')
# }
# ro_set_runs = {
#     'Ro = 1.30 - 0': tools.read_data_file(f'{data_dir}Ro1_30_328000_0.json'),
#     'Ro = 1.30 - 1': tools.read_data_file(f'{data_dir}Ro1_30_328000_1.json'),
#     'Ro = 1.30 - 2': tools.read_data_file(f'{data_dir}Ro1_30_328000_2.json'),
#     'Ro = 1.20 - 0': tools.read_data_file(f'{data_dir}Ro1_20_328000_0.json'),
#     'Ro = 1.20 - 1': tools.read_data_file(f'{data_dir}Ro1_20_328000_1.json'),
#     'Ro = 1.20 - 2': tools.read_data_file(f'{data_dir}Ro1_20_328000_2.json'),
#     'Ro = 1.10 - 0': tools.read_data_file(f'{data_dir}Ro1_10_328000_0.json'),
#     'Ro = 1.10 - 1': tools.read_data_file(f'{data_dir}Ro1_10_328000_1.json'),
#     'Ro = 1.10 - 2': tools.read_data_file(f'{data_dir}Ro1_10_328000_2.json'),
#     'Ro = 1.05 - 0': tools.read_data_file(f'{data_dir}Ro1_05_328000_0.json'),
#     'Ro = 1.05 - 1': tools.read_data_file(f'{data_dir}Ro1_05_328000_1.json'),
#     'Ro = 1.05 - 2': tools.read_data_file(f'{data_dir}Ro1_05_328000_2.json'),
#     'Ro = 1.00 - 0': tools.read_data_file(f'{data_dir}Ro1_00_328000_0.json'),
#     'Ro = 1.00 - 1': tools.read_data_file(f'{data_dir}Ro1_00_328000_1.json'),
#     'Ro = 1.00 - 2': tools.read_data_file(f'{data_dir}Ro1_00_328000_2.json'),
#     'Ro = 0.95 - 0': tools.read_data_file(f'{data_dir}Ro0_95_328000_0.json'),
#     'Ro = 0.95 - 1': tools.read_data_file(f'{data_dir}Ro0_95_328000_1.json'),
#     'Ro = 0.95 - 2': tools.read_data_file(f'{data_dir}Ro0_95_328000_2.json'),
#     'Ro = 0.90 - 0': tools.read_data_file(f'{data_dir}Ro0_90_328000_0.json'),
#     'Ro = 0.90 - 1': tools.read_data_file(f'{data_dir}Ro0_90_328000_1.json'),
#     'Ro = 0.90 - 2': tools.read_data_file(f'{data_dir}Ro0_90_328000_2.json'),
#     'Ro = 0.80 - 0': tools.read_data_file(f'{data_dir}Ro0_80_328000_0.json'),
#     'Ro = 0.80 - 1': tools.read_data_file(f'{data_dir}Ro0_80_328000_1.json'),
#     'Ro = 0.80 - 2': tools.read_data_file(f'{data_dir}Ro0_80_328000_2.json')
# }

us_set = tools.read_run_set(data_dir, 'us_3280K', 10)
us_set_lock = tools.read_run_set(data_dir, 'us_3280K_at_home', 10)
us_set_restrict = tools.read_run_set(data_dir, 'us_3280K_restrict', 5)
us_set_restrict_school = tools.read_run_set(data_dir, 'us_3280K_mask_schl', 10)
characterize_phases(us_set_restrict_school)

us_daily_new = []
us_calc_daily_new = []
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
        if '' != row[US_JH_CALC_DAILY_NEW]:
            us_calc_daily_new.append(int(row[US_JH_CALC_DAILY_NEW]) / 100)
        if '' != row[US_JH_DAILY_NEW_7_DAY]:
            us_daily_new_7_day.append(int(row[US_JH_DAILY_NEW_7_DAY]) / 100)
        if '' != row[US_JH_CUMULATIVE]:
            us_cumulative.append(int(row[US_JH_CUMULATIVE]) / 100)
        if '' != row[US_JH_DEATHS]:
            us_deaths.append(int(row[US_JH_DEATHS]) / 100)

# us_set_v2 = tools.read_run_set('./data/simple_v2/', 'us_3280K', 5)
# characterize_phases(us_set_v2)
# title_template = '{} Simulation - v2, pop: 3,280,000'
# ave_new_cases_v2 = tools.plot_run_set_series(
#     us_set_v2, s.NEW_CONFIRMED_CASES_SERIES, title_template)
# new_cases_confirmed_set = {
#     'actual new cases': us_daily_new_7_day,
#     'new cases v2': ave_new_cases_v2
# }
# tools.plot_curves(new_cases_confirmed_set, 'V2 Calibration - daily new cases')
#
# deaths_v2 = tools.plot_run_set_series(
#     us_set_v2, s.CUMULATIVE_DEATHS_SERIES, title_template)
# deaths_set = {
#     'actual deaths': us_deaths,
#     'deaths v2': deaths_v2
# }
# tools.plot_curves(deaths_set, 'V2 Calibration - deaths')
#
# cumulative_v2 = tools.plot_run_set_series(
#     us_set_v2, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)
# cumulative_set = {
#     'actual confirmed cases': us_cumulative,
#     'confirmed cases v2': cumulative_v2
# }
# tools.plot_curves(cumulative_set, 'V2 Calibration - cumulative cases')
#
# average_runs(ro_set['Ro = 1.30'], ro_set_runs['Ro = 1.30 - 1'],
#              ro_set_runs['Ro = 1.30 - 1'], ro_set_runs['Ro = 1.30 - 2'])
# average_runs(ro_set['Ro = 1.20'], ro_set_runs['Ro = 1.20 - 1'],
#              ro_set_runs['Ro = 1.20 - 1'], ro_set_runs['Ro = 1.20 - 2'])
# average_runs(ro_set['Ro = 1.10'], ro_set_runs['Ro = 1.10 - 1'],
#              ro_set_runs['Ro = 1.10 - 2'])
# average_runs(ro_subset['Ro = 1.00'], ro_set_runs['Ro = 1.00 - 0'],
#              ro_set_runs['Ro = 1.00 - 1'], ro_set_runs['Ro = 1.00 - 2'])
# average_runs(ro_subset['Ro = 1.05'], ro_set_runs['Ro = 1.05 - 0'],
#              ro_set_runs['Ro = 1.05 - 1'], ro_set_runs['Ro = 1.05 - 2'])
# average_runs(ro_subset['Ro = 0.95'], ro_set_runs['Ro = 0.95 - 0'],
#              ro_set_runs['Ro = 0.95 - 1'], ro_set_runs['Ro = 0.95 - 2'])
# average_runs(ro_subset['Ro = 0.90'], ro_set_runs['Ro = 0.90 - 0'],
#              ro_set_runs['Ro = 0.90 - 1'], ro_set_runs['Ro = 0.90 - 2'])
# average_runs(ro_subset['Ro = 0.80'], ro_set_runs['Ro = 0.80 - 0'],
#              ro_set_runs['Ro = 0.80 - 1'], ro_set_runs['Ro = 0.80 - 2'])

# plot_set_series(ro_set, 'cumulative_cases_series', 'Cumulative Cases; pop. 328K;\ninitial infection 20',
#                 legend_loc='upper right')
# plot_set_series(ro_set, 'daily_new_cases_series', 'Daily New Cases; pop. 328K;\ninitial infection 20',
#                 legend_loc='upper right')
# plot_set_series(ro_set, 'cumulative_deaths_series', 'Cumulative Death Toll; pop. 328K;\ninitial infection 20',
#                 legend_loc='upper right')
# plot_set_series(ro_subset, 'cumulative_cases_series', 'Cumulative Cases; pop. 328K;\ninitial infection 20')
# plot_set_series(ro_subset, 'daily_new_cases_series', 'Daily New Cases; pop. 328K;\ninitial infection 20')
# plot_set_series(ro_subset, 'cumulative_deaths_series', 'Cumulative Death Toll; pop. 328K;\ninitial infection 20')


title_template = '{} Simulation, pop: 3,280,000'
ave_new_cases = tools.plot_run_set_series(
    us_set, s.NEW_CASES_SERIES, title_template)

ave_new_confirmed_cases = tools.plot_run_set_series(
    us_set, s.NEW_CONFIRMED_CASES_SERIES, title_template)

ave_hospitalizations = tools.plot_run_set_series(
    us_set, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)

ave_cases = tools.plot_run_set_series(
    us_set, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)

ave_deaths = tools.plot_run_set_series(
    us_set, s.CUMULATIVE_DEATHS_SERIES, title_template)

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
    us_set_restrict, s.NEW_CASES_SERIES, title_template)

ave_new_confirmed_cases_restrict = tools.plot_run_set_series(
    us_set_restrict, s.NEW_CONFIRMED_CASES_SERIES, title_template)

ave_hospitalizations_restrict = tools.plot_run_set_series(
    us_set_restrict, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)

ave_cases_restrict = tools.plot_run_set_series(
    us_set_restrict, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)

ave_deaths_restrict = tools.plot_run_set_series(
    us_set_restrict, s.CUMULATIVE_DEATHS_SERIES, title_template)

title_template = '{} Simulation, 2nd Wave Restriction,\nschool reopen day 175, pop: 3,280,000'
ave_new_cases_restrict_school = tools.plot_run_set_series(
    us_set_restrict_school, s.NEW_CASES_SERIES, title_template)

ave_new_confirmed_cases_restrict_school = tools.plot_run_set_series(
    us_set_restrict_school, s.NEW_CONFIRMED_CASES_SERIES, title_template)

ave_hospitalizations_restrict_school = tools.plot_run_set_series(
    us_set_restrict_school, s.ACTIVE_HOSPITALIZED_CASES_SERIES, title_template)

ave_cases_restrict_school = tools.plot_run_set_series(
    us_set_restrict_school, s.CUMULATIVE_CONFIRMED_CASES_SERIES, title_template)

ave_deaths_restrict_school = tools.plot_run_set_series(
    us_set_restrict_school, s.CUMULATIVE_DEATHS_SERIES, title_template)

new_cases_confirmed_set = {
    'actual new cases, 7 day ave., Johns Hopkins University': us_daily_new_7_day,
    'unrestricted reopen, Re=1.56': ave_new_confirmed_cases,
    "new stay at home at 60K/day, Re=0.93": ave_new_confirmed_cases_lock,
    "wear masks at 60K/day, Re=1.00": ave_new_confirmed_cases_restrict,
    "wear masks, open schools at 175, Re=1.07": ave_new_confirmed_cases_restrict_school
}
tools.plot_curves(new_cases_confirmed_set, 'Best and Worst New Confirmed Cases Scenarios', hilight=4)

cumulative_cases_set = {
    'actual cases, Johns Hopkins University': us_cumulative,
    'unrestricted reopen, Re=1.56': ave_cases,
    "new stay at home at 60K/day, Re=0.93": ave_cases_lock,
    "wear masks at 60K/day, Re=1.00": ave_cases_restrict,
    "wear masks, open schools at 175, Re=1.07": ave_cases_restrict_school
}
tools.plot_curves(cumulative_cases_set, 'Best and Worst Cumulative Cases Scenarios', hilight=4)

cumulative_deaths_set = {
    'actual deaths, Johns Hopkins University': us_deaths,
    'unrestricted reopen, Re=1.56': ave_deaths,
    "new stay at home at 60K/day, Re=0.93": ave_deaths_lock,
    "wear masks at 60K/day, Re=1.00": ave_deaths_restrict,
    "wear masks, open schools at 175, Re=1.07": ave_deaths_restrict_school
}
tools.plot_curves(cumulative_deaths_set, 'Best and Worst Cumulative Deaths Scenarios', hilight=4)

hospitalizations_set = {
    'unrestricted reopen, Re=1.56': ave_hospitalizations,
    "new stay at home at 60K/day, Re=0.93": ave_hospitalizations_lock,
    "wear masks at 60K/day, Re=1.00": ave_hospitalizations_restrict,
    "wear masks, open schools at 175, Re=1.07": ave_hospitalizations_restrict_school
}
tools.plot_curves(hospitalizations_set, 'Best and Worst Hospitalizations Scenarios')
