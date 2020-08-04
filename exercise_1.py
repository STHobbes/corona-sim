import random
import numpy as np
import matplotlib.pyplot as plt

POPULATION = 32800
'''The size of the initial population.'''

INITIAL_INFECTION = 20
'''The initial infection is the number of initially infected individuals in the population.'''

SIMULATION_DAYS = 211
'''The number of days to run the simulation.'''

DAILY_CONTACTS = 10
'''The number of people you come into contact with on a daily basis.'''

TRANSMISSION_PROBABILITY = 0.075
'''the likelihood a 'contagious' person will infect a 'well' person.'''

HEALTH_STATES = {'well': {'days at state': -1,
                          'can be infected': True,
                          'next state': 'infected',
                          'death rate': 0.0},
                 'infected': {'days at state': 4,
                              'can be infected': False,
                              'next state': 'contagious',
                              'death rate': 0.0},
                 'contagious': {'days at state': 8,
                                'can be infected': False,
                                'next state': 'recovering',
                                'death rate': 0.048},
                 'recovering': {'days at state': 1,
                                'can be infected': False,
                                'next state': 'immune',
                                'death rate': 0.0},
                 'immune': {'days at state': -1,
                            'can be infected': False,
                            'next state': 'well',
                            'death rate': 0.0},
                 'dead': {'days at state': -1,
                          'can be infected': False}}

# OK, let's setup and run the simulation for 500 days. The first thing we need is the
# population. For this initial model we will represent each person with a dictionary
# and we will keep their 'state' as one of the health states, and 'days' as the number
# of days they have been at that state. Create a healthy population:
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
    people[random.randint(0, POPULATION - 1)]['state'] = 'infected'

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
maximum_active_cases_day = 0
maximum_new_cases_day = 0
for day in range(SIMULATION_DAYS):
    # initialize statistics for today
    new_cases = 0
    new_recoveries = 0
    new_deaths = 0
    for person in people:
        # update the health state of every person
        health_state = HEALTH_STATES[person['state']]
        person['days'] += 1
        if 0 < health_state['days at state'] < person['days']:
            # The person is in a state that progresses after some number of days
            # and that number of days was reached - move to the next state and
            # reset this to the first day at that new state.
            if health_state['death rate'] > 0.0 and\
                    random.random() < health_state['death rate']:
                person['state'] = 'dead'
                person['days'] = 1
                new_deaths += 1
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
            for _ in range(int(DAILY_CONTACTS / 2)):
                contact = people[random.randint(0, POPULATION - 1)]
                if contact['state'] == 'contagious':
                    # Oh, this the contact between a healthy person who
                    # can be infected and a 'contagious' person.
                    if random.random() < TRANSMISSION_PROBABILITY:
                        # Bummer, this is an infection contact
                        person['state'] = 'infected'
                        person['days'] = 1
                        new_cases += 1
                        # and break because this person is now infected
                        # and can only be infected once
                        break

        elif person['state'] == 'contagious':
            # look for contacts with people who could be infected.
            for _ in range(int(DAILY_CONTACTS / 2)):
                contact = people[random.randint(0, POPULATION - 1)]
                if HEALTH_STATES[contact['state']]['can be infected']:
                    # Oh, this the contact between 'contagious' person
                    # and a healthy person who can be infected.
                    if random.random() < TRANSMISSION_PROBABILITY:
                        # Bummer, this is an infection contact
                        contact['state'] = 'infected'
                        contact['days'] = 1
                        new_cases += 1

    # append the today's statistics to the lists
    cumulative_cases.append(cumulative_cases[day] + new_cases)
    active_cases.append(active_cases[day] + new_cases - new_recoveries - new_deaths)
    if active_cases[day+1] > active_cases[maximum_active_cases_day]:
        maximum_active_cases_day = day + 1
    cumulative_recoveries.append(cumulative_recoveries[day] + new_recoveries)
    cumulative_deaths.append(cumulative_deaths[day] + new_deaths)
    daily_new_cases.append(new_cases)
    if daily_new_cases[day+1] > daily_new_cases[maximum_new_cases_day]:
        maximum_new_cases_day = day + 1
    daily_new_active_cases.append(new_cases - new_recoveries - new_deaths)
    daily_new_recoveries.append(new_recoveries)
    daily_new_deaths.append(new_deaths)

# print the results of the simulation
print('Simulation Summary:')
print(f'  Cumulative Cases:         {cumulative_cases[SIMULATION_DAYS]:16,}')
print(f'  Cumulative Recoveries:    {cumulative_recoveries[SIMULATION_DAYS]:16,}')
print(f'  Cumulative Deaths:        {cumulative_deaths[SIMULATION_DAYS]:16,}')
print(f'  Maximum Active Cases:     {active_cases[maximum_active_cases_day]:16,}: day {maximum_active_cases_day}')
print(f'  Maximum New Daily Cases:  {daily_new_cases[maximum_new_cases_day]:16,}: day {maximum_new_cases_day}')

# plot the results
# These are the cumulative stats
Ro = DAILY_CONTACTS * TRANSMISSION_PROBABILITY * HEALTH_STATES['contagious']['days at state']
plt.clf()
plt.title(
    f'Total Cases Simulation\n population={POPULATION}, Ro={Ro}')
plt.xlabel('days')
plt.ylabel('cumulative number')
plt.xticks(np.arange(0, SIMULATION_DAYS, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.plot(cumulative_cases, label='cumulative cases')
plt.plot(active_cases, label='active cases')
plt.plot(cumulative_recoveries, label='recoveries')
plt.plot(cumulative_deaths, label='deaths')
plt.legend()
plt.show()
plt.pause(0.1)

#These are the daily stats
plt.clf()
plt.title(
    f'Daily Cases Simulation\npopulation={POPULATION}, Ro={Ro}')
plt.xlabel('days')
plt.ylabel('daily number')
plt.xticks(np.arange(0, SIMULATION_DAYS, 14))
plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
plt.plot(daily_new_cases, label='daily new cases')
plt.plot(daily_new_active_cases, label='daily active cases')
plt.plot(daily_new_recoveries, label='daily recoveries')
plt.plot(daily_new_deaths, label='daily deaths')
plt.legend()
plt.show()
plt.pause(0.1)
