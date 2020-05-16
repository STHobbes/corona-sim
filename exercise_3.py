import json
import random
import time
import numpy as np
import matplotlib.pyplot as plt

POPULATION = 50000
'''The size of the initial population.'''

INITIAL_INFECTION = 20
'''The initial infection is the number of initially infected individuals in the population.'''

SIMULATION_DAYS = 211
'''The number of days to run the simulation.'''

SIMULATION_PHASES = {
    'normal': {'daily contacts': 50,
               'transmission probability': 0.0085,
               'next phase': 'lock down',
               'condition': {'type': 'cumulative cases exceeds',
                             'count': 200}},
    'lock down': {'daily contacts': 28,
                  'transmission probability': 0.0076,
                  'next phase': 'reopen',
                  'condition': {'type': 'days after max active',
                                'days': 21}},
    'reopen': {'daily contacts': 35,
               'transmission probability': 0.0079}}
'''These are the 'phases' the simulation goes through. Phases generally mean a change
in the conditions under which the simulation is running. Often these represent
mandated changes in behaviour of the population in effort to try to affect what
would be the normal path of the simulation.'''

HEALTH_STATES = {'well': {'days at state': -1,
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
                          'can be infected': False}}


def set_simulation_phase(phase_key, start_day):
    phase = SIMULATION_PHASES[phase_key]
    has_next = 'next phase' in phase and 'condition' in phase
    contacts = phase['daily contacts']
    transmissivity = phase['transmission probability']
    phase['Ro'] = contacts * transmissivity \
                  * HEALTH_STATES['contagious']['days at state']
    phase['start day'] = start_day
    return phase, has_next, contacts, transmissivity


# random.seed(42)
# Everything is setup, get the start time for the simulation
start = time.time()
# OK, let's setup and run the simulation for SIMULATION_DAYS days. The first thing
# we need is the population. For this initial model we will represent each person
# with a dictionary and we will keep their 'state' as one of the health states, and
# 'days' as the number of days they have been at that state. Create a healthy
# population:
people = []
for person_id in range(POPULATION):
    people.append({'id': person_id,
                   'state': 'well',
                   'days': 1})

# OK, now I've got a healthy population - let's infect the 'INITIAL_INFECTION',
# randomly - these may be people who came from an infected area to their second house,
# or went to a place that was infected to shop or work, and then came back into the
# population we are modeling.
for _ in range(INITIAL_INFECTION):
    people[random.randint(0, POPULATION - 1)]['state'] = 'contagious'

# OK our population is ready to go. We need some tracking arrays so we can record
# and graph what happens in our simulation. The important things for us are:
#  cumulative_cases - number of cases since this started
#  active_cases - number of people who are still sick
#  cumulative_recoveries - number of people who have recovered and are now immune
#  cumulative_deaths - the number of deaths since this started
#  daily_new_cases - how many new cases are there today
#  daily_new_active_cases - the change in the number of active cases, which is the
#    (daily_new_cases - daily recovery), so if the whole population is recovering,
#    this will be negative because more people are recovering than getting sick.
#  daily_new_recoveries - how many new recoveries are there today
#  daily_new_deaths - how many deaths are there today.
cumulative_cases = [INITIAL_INFECTION]
active_cases = [INITIAL_INFECTION]
cumulative_recoveries = [0]
cumulative_deaths = [0]
daily_new_cases = [0]
daily_new_active_cases = [0]
daily_new_recoveries = [0]
daily_new_deaths = [0]
maximum_active_cases = 0
maximum_active_cases_day = 0
maximum_daily_new_cases = 0
maximum_new_cases_day = 0
maximum_new_cases_cumulative = 0
phase_days = []
phase_cumulative = []
phase_daily = []

simulation_phase, has_next_simulation_phase, daily_contacts, \
    transmission_probability = set_simulation_phase('normal', 0)
# This line declares 4 key variables for our simulation:
# simulation_phase = SIMULATION_STATES['normal']
#   this is phase data for the current phase specification of the
#   simulation (as opposed to the name of the phase)
# has_next_simulation_state = True if there is a next phase in the
#   simulation, False otherwise
# daily_contacts = simulation_phase['daily contacts']
#   the average number of daily contacts for a person.
# transmission_probability = simulation_phase['transmission probability']
#   the likelihood a 'contagious' person will infect a 'well' person.

# OK, let's simulate. For each day every person will have DAILY_CONTACTS random
# contacts. If it is a contact between a person who can get infected and an
# infected person, then we will guess whether the person was infected based on
# the TRANSMISSION_POSSIBILITY
current_population = POPULATION
for day in range(SIMULATION_DAYS):
    # initialize statistics for today
    new_cases = 0
    new_recoveries = 0
    new_deaths = 0
    for person in reversed(people):
        # update the health state of every person
        health_state = HEALTH_STATES[person['state']]
        person['days'] += 1
        if 0 < health_state['days at state'] < person['days']:
            # The person is in a state that progresses after some number of days
            # and that number of days was reached - move to the next state and
            # reset this to the first day at that new state.
            if health_state['death rate'] > 0.0 and \
                    random.random() < health_state['death rate']:
                people.remove(person)
                new_deaths += 1
                current_population -= 1
            else:
                person['state'] = health_state['next state']
                person['days'] = 1
                if person['state'] == 'immune':
                    # This person was sick long enough to recover (they went
                    # from recovery to immune) record them as a recovery.
                    new_recoveries += 1

    for person in people:
        # can this person infect, or be infected - if so, daily contacts
        # must be traced to see if there is an infection event
        if HEALTH_STATES[person['state']]['can be infected']:
            # look for contacts with infectious individuals
            for _ in range(int(daily_contacts / 2)):
                contact = people[random.randint(0, current_population - 1)]
                if contact['state'] == 'contagious':
                    # Oh, this the contact between a healthy person who
                    # can be infected and a 'contagious' person.
                    if random.random() < transmission_probability:
                        # Bummer, this is an infection contact
                        person['state'] = 'infected'
                        person['days'] = 1
                        new_cases += 1
                        # and break because this person is now infected
                        # and can only be infected once
                        break

        elif person['state'] == 'contagious':
            # look for contacts with people who could be infected.
            for _ in range(int(daily_contacts / 2)):
                contact = people[random.randint(0, current_population - 1)]
                if HEALTH_STATES[contact['state']]['can be infected']:
                    # Oh, this the contact between 'contagious' person
                    # and a healthy person who can be infected.
                    if random.random() < transmission_probability:
                        # Bummer, this is an infection contact
                        contact['state'] = 'infected'
                        contact['days'] = 1
                        new_cases += 1

    # append the today's statistics to the lists
    cumulative_cases.append(cumulative_cases[day] + new_cases)
    active_cases.append(active_cases[day] + new_cases - new_recoveries - new_deaths)
    if active_cases[day + 1] > maximum_active_cases:
        maximum_active_cases = active_cases[day + 1]
        maximum_active_cases_day = day
    cumulative_recoveries.append(cumulative_recoveries[day] + new_recoveries)
    cumulative_deaths.append(cumulative_deaths[day] + new_deaths)
    if maximum_daily_new_cases < new_cases:
        maximum_daily_new_cases = new_cases
        maximum_new_cases_day = day
        maximum_new_cases_cumulative = cumulative_cases[day + 1]
    daily_new_cases.append(new_cases)
    daily_new_active_cases.append(new_cases - new_recoveries - new_deaths)
    daily_new_recoveries.append(new_recoveries)
    daily_new_deaths.append(new_deaths)

    # Does the simulation state change?
    if has_next_simulation_phase:
        condition = simulation_phase['condition']
        move_to_next_phase = False
        if condition['type'] == 'cumulative cases exceeds':
            if cumulative_cases[day + 1] >= condition['count']:
                move_to_next_phase = True
        elif condition['type'] == 'days after max active':
            if day - maximum_active_cases_day >= condition['days']:
                move_to_next_phase = True

        if move_to_next_phase:
            print(f' advance to {simulation_phase["next phase"]} on day {day}')
            simulation_phase, has_next_simulation_phase, daily_contacts, \
                transmission_probability = \
                set_simulation_phase(simulation_phase['next phase'], day)
            phase_days += [day + 1, day + 1, day + 1, day + 1]
            phase_cumulative += [cumulative_cases[day + 1], active_cases[day + 1],
                                 cumulative_recoveries[day + 1], cumulative_deaths[day + 1]]
            phase_daily += [daily_new_cases[day + 1], daily_new_active_cases[day + 1],
                            daily_new_recoveries[day + 1], daily_new_deaths[day + 1]]

# print the results of the simulation
print(f'Simulation Summary:')
print(f'  Setup:')
print(f'    Simulation Days:           {SIMULATION_DAYS:16,}')
print(f'    Population:                {POPULATION:16,}')
print(f'    Initial Infection:         {INITIAL_INFECTION:16,}')
print(f'    Days Contagious:           {HEALTH_STATES["contagious"]["days at state"]:16,}')
print(f'    Phases:')
for key, value in SIMULATION_PHASES.items():
    if 'start day' in value:
        print(f'      {key}:')
        print(f'        start day:               {value["start day"]:14,}')
        print(f'        contacts per day:        {value["daily contacts"]:14,}')
        print(f'        transmission probability:{value["transmission probability"]:14.4f}')
        print(f'        Ro:                      {value["Ro"]:14.4f}')
print(f'  Daily:')
print(f'    Max Daily New Cases:')
print(f'      Number of Cases:         {maximum_daily_new_cases:16,}')
print(f'      On Day:                  {maximum_new_cases_day:16,}')
print(f'      Cumulative Cases:        {maximum_new_cases_cumulative:16,}'
      f'({maximum_new_cases_cumulative * 100.0 / POPULATION:5.2f}%)')
print(f'    Maximum Active Cases:      {maximum_active_cases:16,}')
print(f'    Maximum Active Cases Day:  {maximum_active_cases_day:16,}')
print(f'  Cumulative:')
print(f'    Cumulative Cases:          {cumulative_cases[SIMULATION_DAYS]:16,}'
      f'({cumulative_cases[SIMULATION_DAYS] * 100.0 / POPULATION:5.2f}%)')
print(f'    Cumulative Recoveries:     {cumulative_recoveries[SIMULATION_DAYS]:16,}'
      f'({cumulative_recoveries[SIMULATION_DAYS] * 100.0 / POPULATION:5.2f}%)')
print(f'    Cumulative Deaths:         {cumulative_deaths[SIMULATION_DAYS]:16,}'
      f'({cumulative_deaths[SIMULATION_DAYS] * 100.0 / POPULATION:5.2f}%)')

print(f'\nSimulation time: {time.time() - start:.4f}sec\n')

# save the data from this simulation to a file
phases_data = {}
for key, value in SIMULATION_PHASES.items():
    if 'start day' in value:
        phases_data[key] = {
            'start_day': value['start day'],
            'daily_contacts': value['daily contacts'],
            'transmission_probability': value['transmission probability'],
            'Ro': value["Ro"]
        }

data = {'simulation_days': SIMULATION_DAYS,
        'population': POPULATION,
        'initial_infection': INITIAL_INFECTION,
        'days_contagious': HEALTH_STATES['contagious']['days at state'],
        'phases': phases_data,
        'max_new_daily_cases_ct': maximum_daily_new_cases,
        'max_new_daily_cases_day': maximum_new_cases_day,
        'max_new_daily_cases_cum': maximum_new_cases_cumulative,
        'max_active_cases_ct': maximum_active_cases,
        'max_active_cases_day': maximum_active_cases_day,
        'cumulative_cases': cumulative_cases[-1],
        'cumulative_recoveries': cumulative_recoveries[-1],
        'cumulative_deaths': cumulative_deaths[-1],
        'cumulative_cases_series': cumulative_cases,
        'active_cases_series': active_cases,
        'cumulative_recoveries_series': cumulative_recoveries,
        'cumulative_deaths_series': cumulative_deaths,
        'daily_new_cases_series': daily_new_cases,
        'daily_new_active_cases_series': daily_new_active_cases,
        'daily_new_recoveries_series': daily_new_recoveries,
        'daily_new_deaths_series': daily_new_deaths}
with open("./data/expl2/report_200_lock_0_85_9.json", "w") as fw:
    json.dump(data, fw, indent=2)

# plot the results
# These are the cumulative stats
plt.clf()
plt.title(
    f'Total Cases Simulation, population: {POPULATION}\n'
    f'"normal" @ Ro={SIMULATION_PHASES["normal"]["Ro"]:.3f};'
    f' "lock down" @ Ro={SIMULATION_PHASES["lock down"]["Ro"]:.3f};'
    f' "reopen" @ Ro={SIMULATION_PHASES["reopen"]["Ro"]:.3f}')
plt.xlabel('days')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.ylabel('cumulative number')
plt.plot(cumulative_cases, label='cumulative cases')
plt.plot(active_cases, label='active cases')
plt.plot(cumulative_recoveries, label='recoveries')
plt.plot(cumulative_deaths, label='deaths')
plt.scatter(phase_days, phase_cumulative)
plt.legend()
plt.show()
plt.pause(0.1)

# These are the daily stats
plt.clf()
plt.title(
    f'Daily Cases Simulation, population: {POPULATION}\n'
    f'"normal" @ Ro={SIMULATION_PHASES["normal"]["Ro"]:.3f};'
    f' "lock down" @ Ro={SIMULATION_PHASES["lock down"]["Ro"]:.3f};'
    f' "reopen" @ Ro={SIMULATION_PHASES["reopen"]["Ro"]:.3f}')
plt.xlabel('days')
plt.xticks(np.arange(0, 211, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.ylabel('daily number')
plt.plot(daily_new_cases, label='daily new cases')
plt.plot(daily_new_active_cases, label='daily active cases')
plt.plot(daily_new_recoveries, label='daily recoveries')
plt.plot(daily_new_deaths, label='daily deaths')
plt.scatter(phase_days, phase_daily)
plt.legend()
plt.show()
plt.pause(0.1)
