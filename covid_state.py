import math
import random
import numpy as np
import simulate as s

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


def get_mean_infectious_days():
    return HEALTH_STATES['presymptomatic']['days at state'] + HEALTH_STATES['mild']['days at state']


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

    testing_probability -= severe_possibility
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
        # there may be multiple next states with different probabilities
        # of advancement
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
                if person['tested']:
                    sim_state[s.DAILY_CONFIRMED_DEATHS] += 1
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
                    sim_state[s.DAILY_CONFIRMED_RECOVERIES] += 1
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
    """

    :param sim_state:
    :param person:
    :param population:
    :return:
    """
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
