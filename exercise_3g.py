import json
import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import simulate as s
import phase

HEALTH_STATES = {
    'well': {
        'name': 'well',
        'days at state': -1,
        'can be infected': True,
        'infectious': False,
        'hospitalize': False,
        'icu': False,
        'activity level': 1.0,
        'next state': [(1.0, 'infected')]
    },
    'infected': {
        'name': 'infected',
        'days at state': 4.6,
        'standard_deviation': 2.5,
        'can be infected': False,
        'infectious': False,
        'hospitalize': False,
        'icu': False,
        'activity level': 1.0,
        'next state': [(0.3, 'asymptomatic'),
                       (1.0, 'presymptomatic')]
    },
    'asymptomatic': {
        'name': 'asymptomatic',
        'days at state': 8.0,
        'standard_deviation': 2.5,
        'can be infected': False,
        'infectious': True,
        'hospitalize': False,
        'icu': False,
        'activity level': 1.0,
        'next state': [(1.0, 'immune')]
    },
    'presymptomatic': {
        'name': 'presymptomatic',
        'days at state': 1.0,
        'standard_deviation': 2.5,
        'can be infected': False,
        'infectious': True,
        'hospitalize': False,
        'icu': False,
        'activity level': 1.0,
        'next state': [(0.57, 'mild'),
                       (0.86, 'severe'),
                       (1.0, 'critical')]
    },
    'mild': {
        'name': 'mild',
        'days at state': 8.0,
        'standard_deviation': 2.0,
        'can be infected': False,
        'infectious': True,
        'hospitalize': False,
        'icu': False,
        'activity level': 0.5,
        'next state': [(1.0, 'immune')]
    },
    'severe': {
        'name': 'severe',
        'days at state': 14.0,
        'standard_deviation': 2.4,
        'can be infected': False,
        'infectious': True,
        'hospitalize': True,
        'icu': False,
        'activity level': 0.0,
        'next state': [(1.0, 'immune')]
    },
    'critical': {
        'name': 'critical',
        'days at state': 14.0,
        'standard_deviation': 2.4,
        'can be infected': False,
        'infectious': True,
        'hospitalize': True,
        'icu': True,
        'activity level': 0.0,
        'next state': [(0.8, 'immune'),
                       (1.0, 'dead')]
    },
    'immune': {
        'name': 'immune',
        'days at state': -1,
        'can be infected': False,
        'infectious': False,
        'hospitalize': False,
        'icu': False,
        'next state': 'well',
        'death rate': 0.0
    },
    'dead': {
        'name': 'dead',
        'days at state': -1,
        'can be infected': False
    }
}
DEFAULT_HEALTH_STATE = HEALTH_STATES['well']


def set_default_health_state(person):
    """

    :param person:
    :return:
    """
    person['state'] = DEFAULT_HEALTH_STATE
    person['tested'] = False
    person['days at state'] = 1
    person['state length'] = -1
    return


def set_initial_infected_state(person):
    """

    :param person:
    :return:
    """
    person['state'] = HEALTH_STATES['infected']
    person['tested'] = False
    # set the state so that the person will immediately become infectious
    person['days at state'] = 1
    person['state length'] = 0
    return


def evaluate_health_for_day(sim_state, person):
    """

    :param sim_state:
    :param person:
    :return:
    """
    old_health_state = person['state']
    person['days at state'] += 1
    if 0 <= person['state length'] < person['days at state']:
        # The person is in a state that progresses after some number of days
        # and that number of days was reached - move to the next state and
        # reset this to the first day at that new state.
        advance_health_state(sim_state, person, old_health_state)

    return


def set_testing_for_phase(testing_probability):
    """

    :param testing_probability:
    :return:
    """
    symptomatic_probability = HEALTH_STATES['infected']['next state'][1][0] - \
                              HEALTH_STATES['infected']['next state'][0][0]
    mild_probability = HEALTH_STATES['presymptomatic']['next state'][0][0] * \
                       symptomatic_probability
    severe_possibility = (HEALTH_STATES['presymptomatic']['next state'][1][0] -
                          HEALTH_STATES['presymptomatic']['next state'][0][0]) * \
                         symptomatic_probability
    critical_probability = (HEALTH_STATES['presymptomatic']['next state'][2][0] -
                            HEALTH_STATES['presymptomatic']['next state'][1][0]) * \
                           symptomatic_probability
    if critical_probability > testing_probability:
        HEALTH_STATES['critical']['testing'] = testing_probability / critical_probability
        HEALTH_STATES['severe']['testing'] = 0.0
        HEALTH_STATES['mild']['testing'] = 0.0
        return

    testing_probability -= critical_probability
    HEALTH_STATES['critical']['testing'] = 1.0
    if severe_possibility > testing_probability:
        HEALTH_STATES['severe']['testing'] = testing_probability / severe_possibility
        HEALTH_STATES['mild']['testing'] = 0.0
        return

    testing_probability -= mild_probability
    HEALTH_STATES['severe']['testing'] = 1.0
    if mild_probability > testing_probability:
        HEALTH_STATES['mild']['testing'] = testing_probability / mild_probability

    return


def advance_health_state(sim_state, person, old_health_state):
    """

    :param sim_state:
    :param person:
    :param old_health_state: (dict, not None) The current state for the person.
    :return:
    """
    next_states = old_health_state['next state']
    state_probability = random.random()
    for next_state in next_states:
        if state_probability <= next_state[0]:
            # Move to the next state
            person['state'] = health_state = HEALTH_STATES[next_state[1]]
            person['days at state'] = 1
            mean = health_state['days at state']
            std_dev = health_state.get('standard_deviation', None)
            if mean == -1:
                person['state length'] = -1
            elif std_dev is None:
                person['state length'] = mean
            else:
                person['state length'] = \
                    int(np.random.lognormal(np.log(mean), np.log(math.sqrt(2.0))))

            if health_state['name'] == 'infected':
                sim_state[s.DAILY_CASES] += 1
            elif health_state['name'] == 'dead':
                # this person has died
                sim_state[s.HOSPITALIZED_PEOPLE].remove(person)
                sim_state[s.DAILY_DEATHS] += 1
                sim_state[s.DAILY_HOSPITALIZATIONS] -= 1
                sim_state[s.DAILY_ICU] -= 1
                return
            elif health_state['name'] == 'immune':
                # This is someone who has recovered
                if old_health_state['hospitalize']:
                    sim_state[s.DAILY_HOSPITALIZATIONS] -= 1
                    sim_state[s.PEOPLE].append(person)
                    sim_state[s.DAILY_POPULATION] += 1
                    sim_state[s.HOSPITALIZED_PEOPLE].remove(person)
                    if old_health_state['icu']:
                        sim_state[s.DAILY_ICU] -= 1
                if person['tested']:
                    sim_state[s.DAILY_CONFORMED_RECOVERIES] += 1
                sim_state[s.DAILY_RECOVERIES] += 1

            testing = health_state.get('testing', 0.0)
            if testing > 0.0 and health_state['infectious'] and random.random() < testing:
                person['tested'] = True
                sim_state[s.DAILY_CONFIRMED_CASES] += 1

            if health_state['hospitalize']:
                # this person has moved into a state requiring hospitalization
                sim_state[s.PEOPLE].remove(person)
                sim_state[s.DAILY_POPULATION] -= 1
                sim_state[s.HOSPITALIZED_PEOPLE].append(person)
                sim_state[s.DAILY_HOSPITALIZATIONS] += 1
                if health_state['icu']:
                    # this is a person who has moved into a state requiring
                    # a ventilator (an ICU bed)
                    sim_state[s.DAILY_ICU] += 1
            if 0 <= person['state length'] < person['days at state']:
                # This can happen because some states can be less than a day in length
                return advance_health_state(sim_state, person, health_state)

            break
    return


def evaluate_contacts(sim_state, person, population):
    # can this person infect, or be infected - if so, daily contacts
    # must be traced to see if there is an infection event
    population_ct = len(population)
    p_state = person['state']
    if p_state['can be infected']:
        # look for contacts with infectious individuals
        for _ in range(int((sim_state[s.CURRENT_DAILY_CONTACTS] * p_state['activity level']) / 2)):
            contact = population[random.randint(0, population_ct - 1)]
            if contact['state']['infectious']:
                # Oh, this the contact between a healthy person who
                # can be infected and a 'contagious' person.
                if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                    # Bummer, this is an infection contact
                    advance_health_state(sim_state, person, p_state)
                    # This person is now infected, I don't think we need to
                    # worry about any other contacts.
                    break

    elif p_state['infectious']:
        # look for contacts with people who could be infected.
        for _ in range(int((sim_state[s.CURRENT_DAILY_CONTACTS] * p_state['activity level']) / 2)):
            contact = population[random.randint(0, population_ct - 1)]
            if contact['state']['can be infected']:
                # Oh, this the contact between 'contagious' person
                # and a healthy person who can be infected.
                if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                    # Bummer, this is an infection contact
                    advance_health_state(sim_state, contact, contact['state'])
    return


# Create the simulation state and initialize it to the initial state
sim_state = s.create_initial_state(
    HEALTH_STATES,
    phase.SIMULATION_PHASES, phase.daily_phase_evaluation,
    population=5000
)
sim_state[s.CURRENT_DAILY_CONTACTS] = 9
phase.set_initial_phase(sim_state)
set_testing_for_phase(sim_state[s.CURRENT_TESTING_PROBABILITY])
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
    person = {'id': person_id}
    set_default_health_state(person)
    sim_state[s.PEOPLE].append(person)

# OK, now I've got a healthy population - let's infect the 'INITIAL_INFECTION',
# randomly - these may be people who came from an infected area to their second house,
# or went to a place that was infected to shop or work, and then came back into the
# population we are modeling.
for _ in range(sim_state[s.INITIAL_INFECTION]):
    set_initial_infected_state(
        sim_state[s.PEOPLE][random.randint(0, sim_state[s.POPULATION] - 1)])

# OK, let's simulate. For each day every person will have DAILY_CONTACTS random
# contacts. If it is a contact between a person who can get infected and an
# infected person, then we will guess whether the person was infected based on
# the TRANSMISSION_POSSIBILITY
sim_state[s.DAILY_POPULATION] = sim_state[s.POPULATION]

for day in range(sim_state[s.SIMULATION_DAYS]):
    # Does the simulation state change today based on the
    # numbers at the beginning of the day??
    if sim_state[s.DAilY_PHASE_EVALUATION](sim_state, day):
        set_testing_for_phase(sim_state[s.CURRENT_TESTING_PROBABILITY])

    # initialize statistics for today
    sim_state[s.DAILY_CASES] = 0
    sim_state[s.DAILY_CONFIRMED_CASES] = 0
    sim_state[s.DAILY_RECOVERIES] = 0
    sim_state[s.DAILY_CONFORMED_RECOVERIES] = 0
    sim_state[s.DAILY_DEATHS] = 0
    sim_state[s.DAILY_HOSPITALIZATIONS] = 0
    sim_state[s.DAILY_ICU] = 0
    # update the health state of every person
    for person in reversed(sim_state[s.HOSPITALIZED_PEOPLE]):
        evaluate_health_for_day(sim_state, person)
    for person in reversed(sim_state[s.PEOPLE]):
        evaluate_health_for_day(sim_state, person)

    for person in sim_state[s.PEOPLE]:
        # can this person infect, or be infected - if so, daily contacts
        # must be traced to see if there is an infection event
        evaluate_contacts(sim_state, person, sim_state[s.PEOPLE])

    # append the today's statistics to the lists
    # new_confirmed_cases = sim_state[s.CURRENT_TESTING_PROBABILITY] * sim_state[s.DAILY_CASES]
    # new_confirmed_recoveries = sim_state[s.CURRENT_TESTING_PROBABILITY] * sim_state[s.DAILY_RECOVERIES]
    sim_state[s.CUMULATIVE_CASES_SERIES].append(
        sim_state[s.CUMULATIVE_CASES_SERIES][day] + sim_state[s.DAILY_CASES])
    sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES].append(
        sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][day] + sim_state[s.DAILY_CONFIRMED_CASES])

    sim_state[s.ACTIVE_CASES_SERIES].append(
        sim_state[s.ACTIVE_CASES_SERIES][day] + sim_state[s.DAILY_CASES]
        - sim_state[s.DAILY_RECOVERIES] - sim_state[s.DAILY_DEATHS])
    if sim_state[s.ACTIVE_CASES_SERIES][day + 1] > sim_state[s.ACTIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]]:
        sim_state[s.MAX_ACTIVE_CASES] = day + 1
    sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES].append(
        sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][day] + sim_state[s.DAILY_CONFIRMED_CASES]
        - sim_state[s.DAILY_CONFORMED_RECOVERIES] - sim_state[s.DAILY_DEATHS])
    if sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][day + 1] > \
            sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][sim_state[s.MAX_ACTIVE_CONFIRMED_CASES]]:
        sim_state[s.MAX_ACTIVE_CONFIRMED_CASES] = day + 1
    sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES].append(
        sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][day] + sim_state[s.DAILY_HOSPITALIZATIONS])
    if sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][day + 1] > \
            sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS]]:
        sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS] = day + 1
    sim_state[s.ACTIVE_ICU_CASES_SERIES].append(
        sim_state[s.ACTIVE_ICU_CASES_SERIES][day] + sim_state[s.DAILY_ICU])
    if sim_state[s.ACTIVE_ICU_CASES_SERIES][day + 1] > \
            sim_state[s.ACTIVE_ICU_CASES_SERIES][sim_state[s.MAX_ACTIVE_ICU]]:
        sim_state[s.MAX_ACTIVE_ICU] = day + 1

    sim_state[s.CUMULATIVE_RECOVERIES_SERIES].append(
        sim_state[s.CUMULATIVE_RECOVERIES_SERIES][day] + sim_state[s.DAILY_RECOVERIES])
    sim_state[s.CUMULATIVE_DEATHS_SERIES].append(
        sim_state[s.CUMULATIVE_DEATHS_SERIES][day] + sim_state[s.DAILY_DEATHS])

    sim_state[s.NEW_CASES_SERIES].append(sim_state[s.DAILY_CASES])
    if sim_state[s.NEW_CASES_SERIES][day + 1] > sim_state[s.NEW_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]]:
        sim_state[s.MAX_NEW_DAILY_CASES] = day + 1
    sim_state[s.NEW_CONFIRMED_CASES_SERIES].append(sim_state[s.DAILY_CONFIRMED_CASES])
    if sim_state[s.NEW_CONFIRMED_CASES_SERIES][day + 1] > \
            sim_state[s.NEW_CONFIRMED_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CONFIRMED_CASES]]:
        sim_state[s.MAX_NEW_DAILY_CONFIRMED_CASES] = day + 1

    sim_state[s.NEW_ACTIVE_CASES_SERIES].append(
        sim_state[s.DAILY_CASES] - sim_state[s.DAILY_RECOVERIES] - sim_state[s.DAILY_DEATHS])
    sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES].append(
        sim_state[s.DAILY_CONFIRMED_CASES] - sim_state[s.DAILY_CONFORMED_RECOVERIES] - sim_state[s.DAILY_DEATHS])
    sim_state[s.NEW_RECOVERIES_SERIES].append(sim_state[s.DAILY_RECOVERIES])
    sim_state[s.NEW_DEATHS_SERIES].append(sim_state[s.DAILY_DEATHS])

# print the results of the simulation
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
    f'Total Cases Simulation\n {sim_state[s.POPULATION]} population, '
    f'{sim_state[s.CURRENT_DAILY_CONTACTS]} daily contacts @ {sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]}')
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
plt.plot(sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES], label='daily active confirmed cases')
plt.plot(sim_state[s.NEW_RECOVERIES_SERIES], label='daily recoveries')
plt.plot(sim_state[s.NEW_DEATHS_SERIES], label='daily deaths')
plt.legend()
plt.show()
plt.pause(0.1)
