import json
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import simulate as s
import phase
import covid_state as state


# Create the simulation state and initialize it to the initial state
sim_state = s.create_initial_state(
    state.HEALTH_STATES, state.evaluate_health_for_day,
    state.evaluate_contacts, state.set_testing_for_phase,
    phase.SIMULATION_PHASES, phase.daily_phase_evaluation,
    population=50000)
sim_state[s.CURRENT_CONTAGIOUS_DAYS] = state.get_mean_infectious_days()
phase.set_initial_phase(sim_state)
state.set_testing_for_phase(sim_state[s.CURRENT_TESTING_PROBABILITY])

random.seed(42)
# Everything is setup, get the start time for the simulation
start = time.time()
# OK, let's setup and run the simulation for SIMULATION_DAYS days. The first thing
# we need is the population. For this initial model we will represent each person
# with a dictionary and we will keep their 'state' as one of the health states, and
# 'days' as the number of days they have been at that state. Create a healthy
# population:
for person_id in range(sim_state[s.POPULATION]):
    person = {'id': person_id}
    state.set_default_health_state(person)
    sim_state[s.PEOPLE].append(person)

# OK, now I've got a healthy population - let's infect the 'INITIAL_INFECTION',
# randomly - these may be people who came from an infected area to their second house,
# or went to a place that was infected to shop or work, and then came back into the
# population we are modeling.
for _ in range(sim_state[s.INITIAL_INFECTION]):
    state.set_initial_infected_state(
        sim_state[s.PEOPLE][random.randint(0, sim_state[s.POPULATION] - 1)])

# OK, let's simulate. For each day every person will have DAILY_CONTACTS random
# contacts. If it is a contact between a person who can get infected and an
# infected person, then we will guess whether the person was infected based on
# the TRANSMISSION_POSSIBILITY
sim_state[s.DAILY_POPULATION] = sim_state[s.POPULATION]

s.run_simulation(sim_state)


# print the results of the simulation
phase_desc = ''
print(f'Simulation Summary:')
print(f'  Setup:')
print(f'    Simulation Days:           {sim_state[s.SIMULATION_DAYS]:16,}')
print(f'    Population:                {sim_state[s.POPULATION]:16,}')
print(f'    Initial Infection:         {sim_state[s.INITIAL_INFECTION]:16,}')
# print(f'    Days Contagious:           {HEALTH_STATES["contagious"]["days at state"]:16,}')
print(f'    Phases:')
for key, value in phase.SIMULATION_PHASES.items():
    if 'start day' in value:
        print(f'      {key}:')
        print(f'        start day:               {value["start day"]:14,}')
        print(f'        contacts per day:        {value["daily contacts"]:14,}')
        print(f'        transmission probability:{value["transmission probability"]:14.4f}')
        print(f'        Ro:                      {value["Ro"]:14.4f}')
        if phase_desc != '':
            phase_desc += ', '
        phase_desc += f'{key} Ro={value["Ro"]:.2f}'
print(f'  Daily:')
print(f'    Max Daily New Cases:')
print(f'      On Day:                  {sim_state[s.MAX_NEW_DAILY_CASES]:16,}')
print(f'      Number of New Cases:     {sim_state[s.NEW_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]]:16,}')
print(f'      Cumulative Cases:        {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]]:16,}'
      f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Maximum Active Cases:')
print(f'      On Day:                  {sim_state[s.MAX_ACTIVE_CASES]:16,}')
print(f'      Number of Active Cases:  {sim_state[s.ACTIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]]:16,}')
print(f'      Cumulative Cases:        {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]]:16,}'
      f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Maximum Hospitalized Cases:')
print(f'      On Day:                  {sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS]:16,}')
print(f'      Max Hospitalized Cases:  '
      f'{sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS]]:16,}')
print(f'    Maximum ICU Beds:')
print(f'      On Day:                  {sim_state[s.MAX_ACTIVE_ICU]:16,}')
print(f'      Number of ICU Beds:      '
      f'{sim_state[s.ACTIVE_ICU_CASES_SERIES][sim_state[s.MAX_ACTIVE_ICU]]:16,}')
print(f'  Cumulative:')
print(f'    Cumulative Cases:                {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Recoveries:           {sim_state[s.CUMULATIVE_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Deaths:               {sim_state[s.CUMULATIVE_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Confirmed Cases:      {sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Confirmed Recoveries: {sim_state[s.CUMULATIVE_CONFIRMED_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_CONFIRMED_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Confirmed Deaths:     {sim_state[s.CUMULATIVE_CONFIRMED_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_CONFIRMED_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')

print(f'\nSimulation time: {time.time() - start:.4f}sec\n')

# save the data from this simulation to a file
phases_data = {}
for key, value in phase.SIMULATION_PHASES.items():
    if 'start day' in value:
        phases_data[key] = {
            'start_day': value['start day'],
            'daily_contacts': value['daily contacts'],
            'transmission_probability': value['transmission probability'],
            'Ro': value["Ro"]
        }

data = {'simulation_days': sim_state[s.SIMULATION_DAYS],
        'population': sim_state[s.POPULATION],
        'initial_infection': sim_state[s.INITIAL_INFECTION],
        'phases': phases_data,
        'max_new_daily_cases_day': sim_state[s.MAX_NEW_DAILY_CASES],
        'max_active_cases_day': sim_state[s.MAX_ACTIVE_CASES],
        'max_active_hospitalizations_day': sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS],
        'max_active_ICU_day': sim_state[s.MAX_ACTIVE_ICU],
        'cumulative_cases': sim_state[s.CUMULATIVE_CASES_SERIES][-1],
        'cumulative_recoveries': sim_state[s.CUMULATIVE_RECOVERIES_SERIES][-1],
        'cumulative_deaths': sim_state[s.CUMULATIVE_DEATHS_SERIES][-1],
        'cumulative_cases_series': sim_state[s.CUMULATIVE_CASES_SERIES],
        'active_cases_series': sim_state[s.ACTIVE_CASES_SERIES],
        'active_confirmed_cases_series': sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES],
        'active_hospitalized_cases_series': sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES],
        'active_ICU_cases_series': sim_state[s.ACTIVE_ICU_CASES_SERIES],
        'cumulative_recoveries_series': sim_state[s.CUMULATIVE_RECOVERIES_SERIES],
        'cumulative_deaths_series': sim_state[s.CUMULATIVE_DEATHS_SERIES],
        'daily_new_cases_series': sim_state[s.NEW_CASES_SERIES],
        'daily_new_active_cases_series': sim_state[s.NEW_ACTIVE_CASES_SERIES],
        'daily_new_recoveries_series': sim_state[s.NEW_RECOVERIES_SERIES],
        'daily_new_deaths_series': sim_state[s.NEW_DEATHS_SERIES]}
with open("./data/expl3/test_x.json", "w") as fw:
    json.dump(data, fw, indent=2)

# plot the results
# These are the cumulative stats
plt.clf()
plt.title(
    f'Total Cases Simulation, {sim_state[s.POPULATION]} population,\n '
    f'{phase_desc}')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
if 'start day' in phase.SIMULATION_PHASES['lock down']:
    start_day = phase.SIMULATION_PHASES['lock down']['start day']
    plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day],
                [sim_state[s.CUMULATIVE_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_ICU_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_RECOVERIES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_DEATHS_SERIES][start_day]],
                label='lock down')
if 'start day' in phase.SIMULATION_PHASES['reopen']:
    start_day = phase.SIMULATION_PHASES['reopen']['start day']
    plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day],
                [sim_state[s.CUMULATIVE_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_ICU_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_RECOVERIES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_DEATHS_SERIES][start_day]],
                label='reopen')
plt.plot(sim_state[s.CUMULATIVE_CASES_SERIES], label='cumulative cases')
plt.plot(sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES], label='cumulative confirmed cases')
plt.plot(sim_state[s.ACTIVE_CASES_SERIES], label='active cases')
plt.plot(sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES], label='active confirmed cases')
plt.plot(sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES], label='active hospitalization')
plt.plot(sim_state[s.ACTIVE_ICU_CASES_SERIES], label='active icu')
plt.plot(sim_state[s.CUMULATIVE_RECOVERIES_SERIES], label='recoveries')
plt.plot(sim_state[s.CUMULATIVE_DEATHS_SERIES], label='deaths')
plt.legend()
plt.show()
plt.pause(0.1)

# plot the results
# These are the cumulative stats
plt.clf()
plt.title(
    f'Active Cases Simulation, {sim_state[s.POPULATION]} population,\n '
    f'{phase_desc}')
plt.xlabel('days')
plt.ylabel('active count')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
if 'start day' in phase.SIMULATION_PHASES['lock down']:
    start_day = phase.SIMULATION_PHASES['lock down']['start day']
    plt.scatter([start_day, start_day, start_day, start_day],
                [sim_state[s.ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_ICU_CASES_SERIES][start_day]],
                label='lock down')
if 'start day' in phase.SIMULATION_PHASES['reopen']:
    start_day = phase.SIMULATION_PHASES['reopen']['start day']
    plt.scatter([start_day, start_day, start_day, start_day],
                [sim_state[s.ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_ICU_CASES_SERIES][start_day]],
                label='reopen')
plt.plot(sim_state[s.ACTIVE_CASES_SERIES], label='active cases')
plt.plot(sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES], label='active confirmed cases')
plt.plot(sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES], label='active hospitalization')
plt.plot(sim_state[s.ACTIVE_ICU_CASES_SERIES], label='active icu')
plt.legend()
plt.show()
plt.pause(0.1)

# These are the daily stats
plt.clf()
plt.title(
    f'Daily Cases Simulation, {sim_state[s.POPULATION]} population,\n '
    f'{phase_desc}')
plt.xlabel('days')
plt.ylabel('daily number')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
if 'start day' in phase.SIMULATION_PHASES['lock down']:
    start_day = phase.SIMULATION_PHASES['lock down']['start day']
    plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day],
                [sim_state[s.NEW_CASES_SERIES][start_day],
                 sim_state[s.NEW_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.NEW_ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.NEW_RECOVERIES_SERIES][start_day],
                 sim_state[s.NEW_DEATHS_SERIES][start_day]],
                label='lock down')
if 'start day' in phase.SIMULATION_PHASES['reopen']:
    start_day = phase.SIMULATION_PHASES['reopen']['start day']
    plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day],
                [sim_state[s.NEW_CASES_SERIES][start_day],
                 sim_state[s.NEW_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.NEW_ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.NEW_RECOVERIES_SERIES][start_day],
                 sim_state[s.NEW_DEATHS_SERIES][start_day]],
                label='reopen')
plt.plot(sim_state[s.NEW_CASES_SERIES], label='daily new cases')
plt.plot(sim_state[s.NEW_CONFIRMED_CASES_SERIES], label='daily new confirmed cases')
plt.plot(sim_state[s.NEW_ACTIVE_CASES_SERIES], label='daily active cases')
plt.plot(sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES], label='daily active confirmed cases')
plt.plot(sim_state[s.NEW_RECOVERIES_SERIES], label='daily recoveries')
plt.plot(sim_state[s.NEW_DEATHS_SERIES], label='daily deaths')
plt.legend()
plt.show()
plt.pause(0.1)
