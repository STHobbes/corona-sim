import json
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import simulate as s
import phase

'''These are the 'phases' the simulation goes through. Phases generally mean a change
in the conditions under which the simulation is running. Often these represent
mandated changes in behaviour of the population in effort to try to affect what
would be the normal path of the simulation.'''

HEALTH_STATES = {
    'well': {'days at state': -1,
             'can be infected': True,
             'next state': 'infected',
             'death rate': 0.0},
    'infected': {'days at state': 2,
                 'can be infected': False,
                 'next state': 'contagious',
                 'death rate': 0.0},
    'contagious': {'days at state': 4,
                   'can be infected': False,
                   'next state': 'recovering',
                   'death rate': 0.03},
    'recovering': {'days at state': 10,
                   'can be infected': False,
                   'next state': 'immune',
                   'death rate': 0.0},
    'immune': {'days at state': -1,
               'can be infected': False,
               'next state': 'well',
               'death rate': 0.0},
    'dead': {'days at state': -1,
             'can be infected': False}
}


sim_state = s.create_initial_state(
    HEALTH_STATES,
    phase.SIMULATION_PHASES, phase.daily_phase_evaluation,
    population=5000)
sim_state[s.CURRENT_DAILY_CONTACTS] = HEALTH_STATES['contagious']['days at state']
phase.set_initial_phase(sim_state)
# This line declares 4 key variables for our simulation:
# simulation_state = SIMULATION_STATES['normal']
# '''The current simulation state'''
# has_next_simulation_state = 'next phase' in simulation_state and \
#     'condition' in simulation_state
#
# daily_contacts = simulation_state['daily contacts']
# '''The number of people you come into contact with on a daily basis.'''
#
# transmission_probability = simulation_state['transmission probability']
# '''the likelihood a 'contagious' person will infect a 'well' person.'''

random.seed(42)
# Everything is setup, get the start time for the simulation
start = time.time()
# OK, let's setup and run the simulation for SIMULATION_DAYS days. The first thing
# we need is the population. For this initial model we will represent each person
# with a dictionary and we will keep their 'state' as one of the health states, and
# 'days' as the number of days they have been at that state. Create a healthy
# population:
for person_id in range(sim_state[s.POPULATION]):
    sim_state[s.PEOPLE].append({'id': person_id,
                                'state': 'well',
                                'days': 1})

# OK, now I've got a healthy population - let's infect the 'INITIAL_INFECTION',
# randomly - these may be people who came from an infected area to their second house,
# or went to a place that was infected to shop or work, and then came back into the
# population we are modeling.
for _ in range(sim_state[s.INITIAL_INFECTION]):
    sim_state[s.PEOPLE][random.randint(0, sim_state[s.POPULATION] - 1)]['state'] = 'contagious'

# OK, let's simulate. For each day every person will have DAILY_CONTACTS random
# contacts. If it is a contact between a person who can get infected and an
# infected person, then we will guess whether the person was infected based on
# the TRANSMISSION_POSSIBILITY
current_population = sim_state[s.POPULATION]

for day in range(sim_state[s.SIMULATION_DAYS]):
    # Does the simulation state change today based on the
    # numbers at the beginning of the day??
    sim_state[s.DAilY_PHASE_EVALUATION](sim_state, day)
    # initialize statistics for today
    new_cases = 0
    new_recoveries = 0
    new_deaths = 0
    for person in reversed(sim_state[s.PEOPLE]):
        # update the health state of every person
        health_state = HEALTH_STATES[person['state']]
        person['days'] += 1
        if 0 < health_state['days at state'] < person['days']:
            # The person is in a state that progresses after some number of days
            # and that number of days was reached - move to the next state and
            # reset this to the first day at that new state.
            if health_state['death rate'] > 0.0 and \
                    random.random() < health_state['death rate']:
                sim_state[s.PEOPLE].remove(person)
                new_deaths += 1
                current_population -= 1
            else:
                person['state'] = health_state['next state']
                person['days'] = 1
                if person['state'] == 'immune':
                    # This person was sick long enough to recover (they went
                    # from recovery to immune) record them as a recovery.
                    new_recoveries += 1

    for person in sim_state[s.PEOPLE]:
        # can this person infect, or be infected - if so, daily contacts
        # must be traced to see if there is an infection event
        if HEALTH_STATES[person['state']]['can be infected']:
            # look for contacts with infectious individuals
            for _ in range(int(sim_state[s.CURRENT_DAILY_CONTACTS] / 2)):
                contact = sim_state[s.PEOPLE][random.randint(0, current_population - 1)]
                if contact['state'] == 'contagious':
                    # Oh, this the contact between a healthy person who
                    # can be infected and a 'contagious' person.
                    if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                        # Bummer, this is an infection contact
                        person['state'] = 'infected'
                        person['days'] = 1
                        new_cases += 1
                        # and break because this person is now infected
                        # and can only be infected once
                        break

        elif person['state'] == 'contagious':
            # look for contacts with people who could be infected.
            for _ in range(int(sim_state[s.CURRENT_DAILY_CONTACTS] / 2)):
                contact = sim_state[s.PEOPLE][random.randint(0, current_population - 1)]
                if HEALTH_STATES[contact['state']]['can be infected']:
                    # Oh, this the contact between 'contagious' person
                    # and a healthy person who can be infected.
                    if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                        # Bummer, this is an infection contact
                        contact['state'] = 'infected'
                        contact['days'] = 1
                        new_cases += 1

    # append the today's statistics to the lists
    new_confirmed_cases = sim_state[s.CURRENT_TESTING_PROBABILITY] * new_cases
    new_confirmed_recoveries = sim_state[s.CURRENT_TESTING_PROBABILITY] * new_recoveries
    sim_state[s.CUMULATIVE_CASES_SERIES].append(sim_state[s.CUMULATIVE_CASES_SERIES][day] + new_cases)
    sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES].append(
        sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][day] + new_confirmed_cases)

    sim_state[s.ACTIVE_CASES_SERIES].append(
        sim_state[s.ACTIVE_CASES_SERIES][day] + new_cases - new_recoveries - new_deaths)
    if sim_state[s.ACTIVE_CASES_SERIES][day + 1] > sim_state[s.ACTIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]]:
        sim_state[s.MAX_ACTIVE_CASES] = day + 1
    sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES].append(
        sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][day] + new_confirmed_cases - new_confirmed_recoveries - new_deaths)
    if sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][day + 1] > \
            sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][sim_state[s.MAX_ACTIVE_CONFIRMED_CASES]]:
        sim_state[s.MAX_ACTIVE_CONFIRMED_CASES] = day + 1

    sim_state[s.CUMULATIVE_RECOVERIES_SERIES].append(sim_state[s.CUMULATIVE_RECOVERIES_SERIES][day] + new_recoveries)
    sim_state[s.CUMULATIVE_DEATHS_SERIES].append(sim_state[s.CUMULATIVE_DEATHS_SERIES][day] + new_deaths)

    sim_state[s.NEW_CASES_SERIES].append(new_cases)
    if sim_state[s.NEW_CASES_SERIES][day + 1] > sim_state[s.NEW_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]]:
        sim_state[s.MAX_NEW_DAILY_CASES] = day + 1
    sim_state[s.NEW_CONFIRMED_CASES_SERIES].append(new_confirmed_cases)
    if sim_state[s.NEW_CONFIRMED_CASES_SERIES][day + 1] > \
            sim_state[s.NEW_CONFIRMED_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CONFIRMED_CASES]]:
        sim_state[s.MAX_NEW_DAILY_CONFIRMED_CASES] = day + 1

    sim_state[s.NEW_ACTIVE_CASES_SERIES].append(new_cases - new_recoveries - new_deaths)
    sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES].append(new_confirmed_cases - new_confirmed_recoveries - new_deaths)
    sim_state[s.NEW_RECOVERIES_SERIES].append(new_recoveries)
    sim_state[s.NEW_DEATHS_SERIES].append(new_deaths)

# print the results of the simulation
print(f'Simulation Summary:')
print(f'  Setup:')
print(f'    Simulation Days:           {sim_state[s.SIMULATION_DAYS]:16,}')
print(f'    Population:                {sim_state[s.POPULATION]:16,}')
print(f'    Initial Infection:         {sim_state[s.INITIAL_INFECTION]:16,}')
print(f'    Days Contagious:           {HEALTH_STATES["contagious"]["days at state"]:16,}')
print(f'    Phases:')
for key, value in phase.SIMULATION_PHASES.items():
    if 'start day' in value:
        print(f'      {key}:')
        print(f'        start day:               {value["start day"]:14,}')
        print(f'        contacts per day:        {value["daily contacts"]:14,}')
        print(f'        transmission probability:{value["transmission probability"]:14.4f}')
        print(f'        Ro:                      {value["Ro"]:14.4f}')
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
print(f'  Cumulative:')
print(f'    Cumulative Cases:          {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Recoveries:     {sim_state[s.CUMULATIVE_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
print(f'    Cumulative Deaths:         {sim_state[s.CUMULATIVE_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
      f'({sim_state[s.CUMULATIVE_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')

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
        'days_contagious': HEALTH_STATES['contagious']['days at state'],
        'phases': phases_data,
        'max_new_daily_cases_day': sim_state[s.MAX_NEW_DAILY_CASES],
        'max_active_cases_day': sim_state[s.MAX_ACTIVE_CASES],
        'cumulative_cases': sim_state[s.CUMULATIVE_CASES_SERIES][-1],
        'cumulative_recoveries': sim_state[s.CUMULATIVE_RECOVERIES_SERIES][-1],
        'cumulative_deaths': sim_state[s.CUMULATIVE_DEATHS_SERIES][-1],
        'cumulative_cases_series': sim_state[s.CUMULATIVE_CASES_SERIES],
        'active_cases_series': sim_state[s.ACTIVE_CASES_SERIES],
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
    f'Total Cases Simulation\n {sim_state[s.POPULATION]} population, '
    f'{sim_state[s.CURRENT_DAILY_CONTACTS]} daily contacts @ {sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]}')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
if 'start day' in phase.SIMULATION_PHASES['lock down']:
    start_day = phase.SIMULATION_PHASES['lock down']['start day']
    plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day],
                [sim_state[s.CUMULATIVE_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_RECOVERIES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_DEATHS_SERIES][start_day]],
                label='lock down')
if 'start day' in phase.SIMULATION_PHASES['reopen']:
    start_day = phase.SIMULATION_PHASES['reopen']['start day']
    plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day],
                [sim_state[s.CUMULATIVE_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CASES_SERIES][start_day],
                 sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_RECOVERIES_SERIES][start_day],
                 sim_state[s.CUMULATIVE_DEATHS_SERIES][start_day]],
                label='reopen')
plt.plot(sim_state[s.CUMULATIVE_CASES_SERIES], label='cumulative cases')
plt.plot(sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES], label='cumulative confirmed cases')
plt.plot(sim_state[s.ACTIVE_CASES_SERIES], label='active cases')
plt.plot(sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES], label='active confirmed cases')
plt.plot(sim_state[s.CUMULATIVE_RECOVERIES_SERIES], label='recoveries')
plt.plot(sim_state[s.CUMULATIVE_DEATHS_SERIES], label='deaths')
plt.legend()
plt.show()
plt.pause(0.1)

# These are the daily stats
plt.clf()
plt.title(
    f'Daily Cases Simulation\n {sim_state[s.POPULATION]} population, '
    f'{sim_state[s.CURRENT_DAILY_CONTACTS]} daily contacts @ {sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]}')
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
plt.plot(sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES], label='new active confirmed cases')
plt.plot(sim_state[s.NEW_RECOVERIES_SERIES], label='daily recoveries')
plt.plot(sim_state[s.NEW_DEATHS_SERIES], label='daily deaths')
plt.legend()
plt.show()
plt.pause(0.1)
