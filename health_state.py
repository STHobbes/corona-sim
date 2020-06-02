import random
import simulate as s

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


def get_mean_infectious_days():
    return HEALTH_STATES['contagious']['days at state']


def set_default_health_state(person):
    person['state'] = 'well'
    person['days'] = 1
    person['tested'] = False
    return


def set_initial_infected_state(person):
    person['state'] = 'contagious'
    return


def evaluate_health_for_day(sim_state, person):
    old_health_state = HEALTH_STATES[person['state']]
    person['days'] += 1
    if 0 < old_health_state['days at state'] < person['days']:
        # The person is in a state that progresses after some number of days
        # and that number of days was reached - move to the next state and
        # reset this to the first day at that new state.
        advance_health_state(sim_state, person, old_health_state)

    return


def advance_health_state(sim_state, person, old_health_state):
    # The person is in a state that progresses after some number of days
    # and that number of days was reached - move to the next state and
    # reset this to the first day at that new state.
    if old_health_state['death rate'] > 0.0 and \
            random.random() < old_health_state['death rate']:
        sim_state[s.PEOPLE].remove(person)
        sim_state[s.DAILY_DEATHS] += 1
        sim_state[s.DAILY_POPULATION] -= 1
        if person['tested']:
            sim_state[s.DAILY_CONFIRMED_DEATHS] += 1
    else:
        person['state'] = old_health_state['next state']
        person['days'] = 1
        if person['state'] == 'immune':
            # This person was sick long enough to recover (they went
            # from recovery to immune) record them as a recovery.
            sim_state[s.DAILY_RECOVERIES] += 1
            if person['tested']:
                sim_state[s.DAILY_CONFIRMED_RECOVERIES] += 1
        elif person['state'] == 'infected':
            sim_state[s.DAILY_CASES] += 1
        elif person['state'] == 'contagious':
            # so this is near where you might show symptoms and be tested
            if HEALTH_STATES['contagious']['testing'] > random.random():
                person['tested'] = True
                sim_state[s.DAILY_CONFIRMED_CASES] += 1


def set_testing_for_phase(testing_probability):
    HEALTH_STATES['contagious']['testing'] = testing_probability


def evaluate_contacts(sim_state, person, population):
    population_ct = len(population)
    if HEALTH_STATES[person['state']]['can be infected']:
        # look for contacts with infectious individuals
        for _ in range(int(sim_state[s.CURRENT_DAILY_CONTACTS] / 2)):
            contact = population[random.randint(0, sim_state[s.DAILY_POPULATION] - 1)]
            if contact['state'] == 'contagious':
                # Oh, this the contact between a healthy person who
                # can be infected and a 'contagious' person.
                if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                    # Bummer, this is an infection contact
                    advance_health_state(sim_state, person, HEALTH_STATES[person['state']])
                    # and break because this person is now infected
                    # and can only be infected once
                    break

    elif person['state'] == 'contagious':
        # look for contacts with people who could be infected.
        for _ in range(int(sim_state[s.CURRENT_DAILY_CONTACTS] / 2)):
            contact = population[random.randint(0, sim_state[s.DAILY_POPULATION] - 1)]
            if HEALTH_STATES[contact['state']]['can be infected']:
                # Oh, this the contact between 'contagious' person
                # and a healthy person who can be infected.
                if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                    # Bummer, this is an infection contact
                    advance_health_state(sim_state, contact, HEALTH_STATES[contact['state']])
