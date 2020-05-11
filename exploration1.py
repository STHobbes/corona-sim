import json
import matplotlib.pyplot as plt

# These are all of the data files I generated while doing
# exploration 1. The naming convection is 'R0_' + the
# value of R0 with an underscore substituted for the decimal
# point + '_pop_' + population + '.json'. These are all '.json'
# files so I can use the '.json' reader packaged with python.
with open("./data/expl1/R0_0_50_pop_10000.json", "r") as fr:
    R0_0_50_pop_10000 = json.load(fr)
with open("./data/expl1/R0_0_65_pop_10000.json", "r") as fr:
    R0_0_65_pop_10000 = json.load(fr)
with open("./data/expl1/R0_0_80_pop_10000.json", "r") as fr:
    R0_0_80_pop_10000 = json.load(fr)
with open("./data/expl1/R0_0_90_pop_10000.json", "r") as fr:
    R0_0_90_pop_10000 = json.load(fr)
with open("./data/expl1/R0_1_00_pop_10000.json", "r") as fr:
    R0_1_00_pop_10000 = json.load(fr)
with open("./data/expl1/R0_1_10_pop_10000.json", "r") as fr:
    R0_1_10_pop_10000 = json.load(fr)
with open("./data/expl1/R0_1_20_pop_500.json", "r") as fr:
    R0_1_20_pop_500 = json.load(fr)
with open("./data/expl1/R0_1_20_pop_1000.json", "r") as fr:
    R0_1_20_pop_1000 = json.load(fr)
with open("./data/expl1/R0_1_20_pop_5000.json", "r") as fr:
    R0_1_20_pop_5000 = json.load(fr)
with open("./data/expl1/R0_1_20_pop_10000.json", "r") as fr:
    R0_1_20_pop_10000 = json.load(fr)
with open("./data/expl1/R0_1_20_pop_50000.json", "r") as fr:
    R0_1_20_pop_50000 = json.load(fr)
with open("./data/expl1/R0_1_20_pop_100000.json", "r") as fr:
    R0_1_20_pop_100000 = json.load(fr)
with open("./data/expl1/R0_1_50_pop_10000.json", "r") as fr:
    R0_1_50_pop_10000 = json.load(fr)
with open("./data/expl1/R0_2_00_pop_10000.json", "r") as fr:
    R0_2_00_pop_10000 = json.load(fr)
with open("./data/expl1/R0_3_00_pop_10000.json", "r") as fr:
    R0_3_00_pop_10000 = json.load(fr)
with open("./data/expl1/R0_4_00_pop_10000.json", "r") as fr:
    R0_4_00_pop_10000 = json.load(fr)
with open("./data/expl1/R0_6_00_pop_10000.json", "r") as fr:
    R0_6_00_pop_10000 = json.load(fr)

# -----------------------------------------------------------------------------
# population of 10,000 with different Ro values
# -----------------------------------------------------------------------------
# cumulative cases curves for various R0
plt.clf()
plt.title(
    f'Cumulative Cases Simulation\n for various Ro, population 10000')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(R0_6_00_pop_10000['cumulative_cases_series'], label='Ro = 6')
plt.plot(R0_4_00_pop_10000['cumulative_cases_series'], label='Ro = 4.0')
plt.plot(R0_3_00_pop_10000['cumulative_cases_series'], label='Ro = 3.0')
plt.plot(R0_2_00_pop_10000['cumulative_cases_series'], label='Ro = 2.0')
plt.plot(R0_1_50_pop_10000['cumulative_cases_series'], label='Ro = 1.5')
plt.plot(R0_1_20_pop_10000['cumulative_cases_series'], label='Ro = 1.2')
plt.plot(R0_1_10_pop_10000['cumulative_cases_series'], label='Ro = 1.10')
plt.plot(R0_1_00_pop_10000['cumulative_cases_series'], label='Ro = 1.00')
plt.plot(R0_0_90_pop_10000['cumulative_cases_series'], label='Ro = 0.90')
plt.plot(R0_0_80_pop_10000['cumulative_cases_series'], label='Ro = 0.80')
plt.plot(R0_0_65_pop_10000['cumulative_cases_series'], label='Ro = 0.65')
plt.plot(R0_0_50_pop_10000['cumulative_cases_series'], label='Ro = 0.50')
plt.legend()
plt.show()
plt.pause(0.1)

# cumulative deaths curves for various Ro
plt.clf()
plt.title(
    f'Cumulative Deaths Simulation\n for various Ro, population 10000')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(R0_6_00_pop_10000['cumulative_deaths_series'], label='Ro = 6')
plt.plot(R0_4_00_pop_10000['cumulative_deaths_series'], label='Ro = 4.0')
plt.plot(R0_3_00_pop_10000['cumulative_deaths_series'], label='Ro = 3.0')
plt.plot(R0_2_00_pop_10000['cumulative_deaths_series'], label='Ro = 2.0')
plt.plot(R0_1_50_pop_10000['cumulative_deaths_series'], label='Ro = 1.5')
plt.plot(R0_1_20_pop_10000['cumulative_deaths_series'], label='Ro = 1.2')
plt.plot(R0_1_10_pop_10000['cumulative_deaths_series'], label='Ro = 1.10')
plt.plot(R0_1_00_pop_10000['cumulative_deaths_series'], label='Ro = 1.00')
plt.plot(R0_0_90_pop_10000['cumulative_deaths_series'], label='Ro = 0.90')
plt.plot(R0_0_80_pop_10000['cumulative_deaths_series'], label='Ro = 0.80')
plt.plot(R0_0_65_pop_10000['cumulative_deaths_series'], label='Ro = 0.65')
plt.plot(R0_0_50_pop_10000['cumulative_deaths_series'], label='Ro = 0.50')
plt.legend()
plt.show()
plt.pause(0.1)

# Active cases curves for various Ro
plt.clf()
plt.title(
    f'Active Cases Simulation\n for various Ro, population 10000')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(R0_6_00_pop_10000['active_cases_series'], label='Ro = 6.0')
plt.plot(R0_4_00_pop_10000['active_cases_series'], label='Ro = 4.0')
plt.plot(R0_3_00_pop_10000['active_cases_series'], label='Ro = 3.0')
plt.plot(R0_2_00_pop_10000['active_cases_series'], label='Ro = 2.0')
plt.plot(R0_1_50_pop_10000['active_cases_series'], label='Ro = 1.5')
plt.plot(R0_1_20_pop_10000['active_cases_series'], label='Ro = 1.2')
plt.plot(R0_1_10_pop_10000['active_cases_series'], label='Ro = 1.10')
plt.plot(R0_1_00_pop_10000['active_cases_series'], label='Ro = 1.00')
plt.plot(R0_0_90_pop_10000['active_cases_series'], label='Ro = 0.90')
plt.plot(R0_0_80_pop_10000['active_cases_series'], label='Ro = 0.80')
plt.plot(R0_0_65_pop_10000['active_cases_series'], label='Ro = 0.65')
plt.plot(R0_0_50_pop_10000['active_cases_series'], label='Ro = 0.50')
plt.legend()
plt.show()
plt.pause(0.1)

# Active cases curves for various Ro - just cases where R0 <= 1.5 so the
# detail is more evident in the lower Ro cases
plt.clf()
plt.title(
    f'Active Cases Simulation\n for various Ro, population 10000')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(R0_1_50_pop_10000['active_cases_series'], label='Ro = 1.5')
plt.plot(R0_1_20_pop_10000['active_cases_series'], label='Ro = 1.2')
plt.plot(R0_1_10_pop_10000['active_cases_series'], label='Ro = 1.10')
plt.plot(R0_1_00_pop_10000['active_cases_series'], label='Ro = 1.00')
plt.plot(R0_0_90_pop_10000['active_cases_series'], label='Ro = 0.90')
plt.plot(R0_0_80_pop_10000['active_cases_series'], label='Ro = 0.80')
plt.plot(R0_0_65_pop_10000['active_cases_series'], label='Ro = 0.65')
plt.plot(R0_0_50_pop_10000['active_cases_series'], label='Ro = 0.50')
plt.legend()
plt.show()
plt.pause(0.1)

# -----------------------------------------------------------------------------
# Ro of 1.2 for various population sizes
# -----------------------------------------------------------------------------
# Comparing what happens with different populations
plt.clf()
plt.title(
    f'Cumulative Cases Simulation\n for Ro = 1.2, various populations')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(R0_1_20_pop_500['cumulative_cases_series'], label='500')
plt.plot(R0_1_20_pop_1000['cumulative_cases_series'], label='1000')
plt.plot(R0_1_20_pop_5000['cumulative_cases_series'], label='5000')
plt.plot(R0_1_20_pop_10000['cumulative_cases_series'], label='10000')
plt.plot(R0_1_20_pop_50000['cumulative_cases_series'], label='50000')
plt.plot(R0_1_20_pop_100000['cumulative_cases_series'], label='100000')
plt.legend()
plt.show()
plt.pause(0.1)

# Comparing what happens with different population in the first 25 days,
# Note,refer to Day 4: Basic Python Collections to review what
# the [0:25] syntax means.
plt.clf()
plt.title(
    f'Cumulative Cases Simulation\n for Ro = 1.2, various populations')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.plot(R0_1_20_pop_500['cumulative_cases_series'][0:25], label='500')
plt.plot(R0_1_20_pop_1000['cumulative_cases_series'][0:25], label='1000')
plt.plot(R0_1_20_pop_5000['cumulative_cases_series'][0:25], label='5000')
plt.plot(R0_1_20_pop_10000['cumulative_cases_series'][0:25], label='10000')
plt.plot(R0_1_20_pop_50000['cumulative_cases_series'][0:25], label='50000')
plt.plot(R0_1_20_pop_100000['cumulative_cases_series'][0:25], label='100000')
plt.legend()
plt.show()
plt.pause(0.1)

# Comparing what happens with different population as a % of the population
# to see when the population is large enough that the noise created by the
# stochastic nature of the simulation does not dominate the simulation.
pop = [500, 1000, 5000, 10000, 50000, 100000]
had_covid = [float(R0_1_20_pop_500['cumulative_cases'] * 100) / pop[0],
             float(R0_1_20_pop_1000['cumulative_cases'] * 100) / pop[1],
             float(R0_1_20_pop_5000['cumulative_cases'] * 100) / pop[2],
             float(R0_1_20_pop_10000['cumulative_cases'] * 100) / pop[3],
             float(R0_1_20_pop_50000['cumulative_cases'] * 100) / pop[4],
             float(R0_1_20_pop_100000['cumulative_cases'] * 100) / pop[5]]
max_active = [float(R0_1_20_pop_500['max_active_cases'] * 100) / pop[0],
              float(R0_1_20_pop_1000['max_active_cases'] * 100) / pop[1],
              float(R0_1_20_pop_5000['max_active_cases'] * 100) / pop[2],
              float(R0_1_20_pop_10000['max_active_cases'] * 100) / pop[3],
              float(R0_1_20_pop_50000['max_active_cases'] * 100) / pop[4],
              float(R0_1_20_pop_100000['max_active_cases'] * 100) / pop[5]]
died = [float(R0_1_20_pop_500['cumulative_deaths'] * 100) / pop[0],
        float(R0_1_20_pop_1000['cumulative_deaths'] * 100) / pop[1],
        float(R0_1_20_pop_5000['cumulative_deaths'] * 100) / pop[2],
        float(R0_1_20_pop_10000['cumulative_deaths'] * 100) / pop[3],
        float(R0_1_20_pop_50000['cumulative_deaths'] * 100) / pop[4],
        float(R0_1_20_pop_100000['cumulative_deaths'] * 100) / pop[5]]
plt.clf()
plt.title(
    f'Percent of population affected as a\n function of population size for Ro=1.2')
plt.xlabel('Ro')
plt.ylabel('% of population')
plt.plot(pop, had_covid, label='fell ill')
plt.plot(pop, died, label='deaths')
plt.plot(pop, max_active, label='max active cases')
plt.legend()
plt.show()
plt.pause(0.1)

# -----------------------------------------------------------------------------
# population of 10,000 with different Ro values - % of population
# -----------------------------------------------------------------------------
Ro = [0.5, 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0, 6.0]
had_covid = [float(R0_0_50_pop_10000['cumulative_cases']) / 100.0,
             float(R0_0_65_pop_10000['cumulative_cases']) / 100.0,
             float(R0_0_80_pop_10000['cumulative_cases']) / 100.0,
             float(R0_0_90_pop_10000['cumulative_cases']) / 100.0,
             float(R0_1_00_pop_10000['cumulative_cases']) / 100.0,
             float(R0_1_10_pop_10000['cumulative_cases']) / 100.0,
             float(R0_1_20_pop_10000['cumulative_cases']) / 100.0,
             float(R0_1_50_pop_10000['cumulative_cases']) / 100.0,
             float(R0_2_00_pop_10000['cumulative_cases']) / 100.0,
             float(R0_3_00_pop_10000['cumulative_cases']) / 100.0,
             float(R0_4_00_pop_10000['cumulative_cases']) / 100.0,
             float(R0_6_00_pop_10000['cumulative_cases']) / 100.0]

max_active = [float(R0_0_50_pop_10000['max_active_cases']) / 100.0,
              float(R0_0_65_pop_10000['max_active_cases']) / 100.0,
              float(R0_0_80_pop_10000['max_active_cases']) / 100.0,
              float(R0_0_90_pop_10000['max_active_cases']) / 100.0,
              float(R0_1_10_pop_10000['max_active_cases']) / 100.0,
              float(R0_1_00_pop_10000['max_active_cases']) / 100.0,
              float(R0_1_20_pop_10000['max_active_cases']) / 100.0,
              float(R0_1_50_pop_10000['max_active_cases']) / 100.0,
              float(R0_2_00_pop_10000['max_active_cases']) / 100.0,
              float(R0_3_00_pop_10000['max_active_cases']) / 100.0,
              float(R0_4_00_pop_10000['max_active_cases']) / 100.0,
              float(R0_6_00_pop_10000['max_active_cases']) / 100.0]

died = [float(R0_0_50_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_0_65_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_0_80_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_0_90_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_1_00_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_1_10_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_1_20_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_1_50_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_2_00_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_3_00_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_4_00_pop_10000['cumulative_deaths']) / 100.0,
        float(R0_6_00_pop_10000['cumulative_deaths']) / 100.0]
plt.clf()
plt.title(
    f'Percent of population affected as a function\n'
    f'of Ro for simulated population=10,000')
plt.xlabel('Ro')
plt.ylabel('% of population')
plt.plot(Ro, had_covid, label='fell ill')
plt.plot(Ro, died, label='deaths')
plt.plot(Ro, max_active, label='max active cases')
plt.legend()
plt.show()
plt.pause(0.1)

plt.clf()
plt.title(
    f'Percent of population death as a function\n'
    f'of Ro for simulated population=10,000')
plt.xlabel('Ro')
plt.ylabel('% of population')
plt.plot(Ro, died, label='deaths')
plt.show()
plt.pause(0.1)
