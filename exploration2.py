import json
import numpy as np
import matplotlib.pyplot as plt


def read_data_file(file_name):
    with open(file_name, "r") as data_file:
        return json.load(data_file)


test = read_data_file("./data/expl2/test.json")
with open("./data/expl2/test_200.json", "r") as fr:
    test_200 = json.load(fr)
with open("./data/expl2/test_1000.json", "r") as fr:
    test_1000 = json.load(fr)
with open("./data/expl2/test_2500.json", "r") as fr:
    test_2500 = json.load(fr)
with open("./data/expl2/test_5000.json", "r") as fr:
    test_5000 = json.load(fr)

with open("./data/expl2/report_200_reopen_1_105.json", "r") as fr:
    report_1_105_seeded = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_0.json", "r") as fr:
    report_1_105_0 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_1.json", "r") as fr:
    report_1_105_1 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_2.json", "r") as fr:
    report_1_105_2 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_3.json", "r") as fr:
    report_1_105_3 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_4.json", "r") as fr:
    report_1_105_4 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_5.json", "r") as fr:
    report_1_105_5 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_6.json", "r") as fr:
    report_1_105_6 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_7.json", "r") as fr:
    report_1_105_7 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_8.json", "r") as fr:
    report_1_105_8 = json.load(fr)
with open("./data/expl2/report_200_reopen_1_105_9.json", "r") as fr:
    report_1_105_9 = json.load(fr)

with open("./data/expl2/report_200_lock_0_68.json", "r") as fr:
    report_lock_0_68_seeded = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_0.json", "r") as fr:
    report_lock_0_68_0 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_1.json", "r") as fr:
    report_lock_0_68_1 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_2.json", "r") as fr:
    report_lock_0_68_2 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_3.json", "r") as fr:
    report_lock_0_68_3 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_4.json", "r") as fr:
    report_lock_0_68_4 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_5.json", "r") as fr:
    report_lock_0_68_5 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_6.json", "r") as fr:
    report_lock_0_68_6 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_7.json", "r") as fr:
    report_lock_0_68_7 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_8.json", "r") as fr:
    report_lock_0_68_8 = json.load(fr)
with open("./data/expl2/report_200_lock_0_68_9.json", "r") as fr:
    report_lock_0_68_9 = json.load(fr)

with open("./data/expl2/report_200_lock_0_85.json", "r") as fr:
    report_lock_0_85_seeded = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_0.json", "r") as fr:
    report_lock_0_85_0 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_1.json", "r") as fr:
    report_lock_0_85_1 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_2.json", "r") as fr:
    report_lock_0_85_2 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_3.json", "r") as fr:
    report_lock_0_85_3 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_4.json", "r") as fr:
    report_lock_0_85_4 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_5.json", "r") as fr:
    report_lock_0_85_5 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_6.json", "r") as fr:
    report_lock_0_85_6 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_7.json", "r") as fr:
    report_lock_0_85_7 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_8.json", "r") as fr:
    report_lock_0_85_8 = json.load(fr)
with open("./data/expl2/report_200_lock_0_85_9.json", "r") as fr:
    report_lock_0_85_9 = json.load(fr)

# cumulative cases, multiple runs
plt.clf()
plt.title(
    f'Cumulative Cases\n for Multiple Runs')
plt.xlabel('days')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.ylabel('cumulative number')
plt.plot(report_1_105_seeded['cumulative_cases_series'], label='seeded')
plt.plot(report_1_105_0['cumulative_cases_series'], label='run 0')
plt.plot(report_1_105_1['cumulative_cases_series'], label='run 1')
plt.plot(report_1_105_2['cumulative_cases_series'], label='run 2')
plt.plot(report_1_105_3['cumulative_cases_series'], label='run 3')
plt.plot(report_1_105_4['cumulative_cases_series'], label='run 4')
plt.plot(report_1_105_5['cumulative_cases_series'], label='run 5')
plt.plot(report_1_105_6['cumulative_cases_series'], label='run 6')
plt.plot(report_1_105_7['cumulative_cases_series'], label='run 7')
plt.plot(report_1_105_8['cumulative_cases_series'], label='run 8')
plt.plot(report_1_105_9['cumulative_cases_series'], label='run 9')
plt.legend()
plt.show()
plt.pause(0.1)

# active cases, multiple runs
plt.clf()
plt.title(
    f'Active Cases for Multiple Runs\n'
    f'lock down Ro=0.51')
plt.xlabel('days')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.ylabel('cumulative number')
plt.plot(report_1_105_seeded['active_cases_series'], label='seeded')
plt.plot(report_1_105_0['active_cases_series'], label='run 0')
plt.plot(report_1_105_1['active_cases_series'], label='run 1')
plt.plot(report_1_105_2['active_cases_series'], label='run 2')
plt.plot(report_1_105_3['active_cases_series'], label='run 3')
plt.plot(report_1_105_4['active_cases_series'], label='run 4')
plt.plot(report_1_105_5['active_cases_series'], label='run 5')
plt.plot(report_1_105_6['active_cases_series'], label='run 6')
plt.plot(report_1_105_7['active_cases_series'], label='run 7')
plt.plot(report_1_105_8['active_cases_series'], label='run 8')
plt.plot(report_1_105_9['active_cases_series'], label='run 9')
plt.legend()
plt.show()
plt.pause(0.1)

# active cases, multiple runs
plt.clf()
plt.title(
    f'Active Cases for Multiple Runs\n'
    f'lock down Ro=0.68')
plt.xlabel('days')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.ylabel('cumulative number')
plt.plot(report_lock_0_68_seeded['active_cases_series'], label='seeded')
plt.plot(report_lock_0_68_0['active_cases_series'], label='run 0')
plt.plot(report_lock_0_68_1['active_cases_series'], label='run 1')
plt.plot(report_lock_0_68_2['active_cases_series'], label='run 2')
plt.plot(report_lock_0_68_3['active_cases_series'], label='run 3')
plt.plot(report_lock_0_68_4['active_cases_series'], label='run 4')
plt.plot(report_lock_0_68_5['active_cases_series'], label='run 5')
plt.plot(report_lock_0_68_6['active_cases_series'], label='run 6')
plt.plot(report_lock_0_68_7['active_cases_series'], label='run 7')
plt.plot(report_lock_0_68_8['active_cases_series'], label='run 8')
plt.plot(report_lock_0_68_9['active_cases_series'], label='run 9')
plt.legend()
plt.show()
plt.pause(0.1)

# active cases, multiple runs
plt.clf()
plt.title(
    f'Active Cases for Multiple Runs\n'
    f'lock down Ro=0.85')
plt.xlabel('days')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.ylabel('cumulative number')
plt.plot(report_lock_0_85_seeded['active_cases_series'], label='seeded')
plt.plot(report_lock_0_85_0['active_cases_series'], label='run 0')
plt.plot(report_lock_0_85_1['active_cases_series'], label='run 1')
plt.plot(report_lock_0_85_2['active_cases_series'], label='run 2')
plt.plot(report_lock_0_85_3['active_cases_series'], label='run 3')
plt.plot(report_lock_0_85_4['active_cases_series'], label='run 4')
plt.plot(report_lock_0_85_5['active_cases_series'], label='run 5')
plt.plot(report_lock_0_85_6['active_cases_series'], label='run 6')
plt.plot(report_lock_0_85_7['active_cases_series'], label='run 7')
plt.plot(report_lock_0_85_8['active_cases_series'], label='run 8')
plt.plot(report_lock_0_85_9['active_cases_series'], label='run 9')
plt.legend()
plt.show()
plt.pause(0.1)

# cumulative deaths curves for various Ro
plt.clf()
plt.title(
    f'Cumulative Deaths Simulation\n for various lock down timing')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(test['cumulative_deaths_series'], label='no lock down')
plt.plot(test_200['cumulative_deaths_series'], label='lock down @ 200 cases')
plt.plot(test_1000['cumulative_deaths_series'], label='lock down @ 1000 cases')
plt.plot(test_2500['cumulative_deaths_series'], label='lock down @ 2500 cases')
plt.plot(test_5000['cumulative_deaths_series'], label='lock down @ 5000 cases')
plt.legend()
plt.show()
plt.pause(0.1)

# Active cases curves for various Ro
plt.clf()
plt.title(
    f'Active Cases Simulation\n for various lock down and reopen timing')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(test['active_cases_series'], label='no lock down')
plt.plot(test_200['active_cases_series'], label='lock down @ 200 cases')
plt.plot(test_1000['active_cases_series'], label='lock down @ 1000 cases')
plt.plot(test_2500['active_cases_series'], label='lock down @ 2500 cases')
plt.plot(test_5000['active_cases_series'], label='lock down @ 5000 cases')
plt.legend()
plt.show()
plt.pause(0.1)

# cumulative cases curves for various R0
plt.clf()
plt.title(
    f'Cumulative Cases Simulation\n for various lock down and reopen timing')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(test_200['cumulative_cases_series'], label='lock down @ 200 cases')
plt.plot(test_1000['cumulative_cases_series'], label='lock down @ 1000 cases')
plt.plot(test_2500['cumulative_cases_series'], label='lock down @ 2500 cases')
plt.plot(test_5000['cumulative_cases_series'], label='lock down @ 5000 cases')
plt.legend()
plt.show()
plt.pause(0.1)

# cumulative deaths curves for various Ro
plt.clf()
plt.title(
    f'Cumulative Deaths Simulation\n for various lock down and reopen timing')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(test_200['cumulative_deaths_series'], label='lock down @ 200 cases')
plt.plot(test_1000['cumulative_deaths_series'], label='lock down @ 1000 cases')
plt.plot(test_2500['cumulative_deaths_series'], label='lock down @ 2500 cases')
plt.plot(test_5000['cumulative_deaths_series'], label='lock down @ 5000 cases')
plt.scatter([6, 11, 13, 15, 38, 43, 49, 46], [2, 4, 8, 14, 19, 86, 238, 335])
plt.legend()
plt.show()
plt.pause(0.1)

# Active cases curves for various Ro
plt.clf()
plt.title(
    f'Active Cases Simulation\n for various lock down and reopen timing')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(test_200['active_cases_series'], label='lock down @ 200 cases')
plt.plot(test_1000['active_cases_series'], label='lock down @ 1000 cases')
plt.plot(test_2500['active_cases_series'], label='lock down @ 2500 cases')
plt.plot(test_5000['active_cases_series'], label='lock down @ 5000 cases')
plt.scatter([6, 11, 13, 15, 38, 43, 49, 46], [204, 1066, 2057, 3833, 74, 459, 675, 1084])
plt.legend()
plt.show()
plt.pause(0.1)
