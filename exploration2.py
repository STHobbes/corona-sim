import json
import matplotlib.pyplot as plt

with open("./data/expl2/test.json", "r") as fr:
    test = json.load(fr)
with open("./data/expl2/test_200.json", "r") as fr:
    test_200 = json.load(fr)
with open("./data/expl2/test_1000.json", "r") as fr:
    test_1000 = json.load(fr)
with open("./data/expl2/test_2500.json", "r") as fr:
    test_2500 = json.load(fr)
with open("./data/expl2/test_5000.json", "r") as fr:
    test_5000 = json.load(fr)


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
