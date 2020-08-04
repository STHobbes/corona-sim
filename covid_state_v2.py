"""

"""
import json
import math
import random
import numpy as np
import simulate_v2 as s

HEALTH_STATES = None
# {
#     'well': {
#         'name': 'well',
#         'days at state': -1,
#         'can be infected': True,
#         'infectious': False,
#         'hospitalize': False,
#         'icu': False,
#         'activity level': 1.0,
#         'next state': [(1.0, 'infected')]
#     },
#     'infected': {
#         'name': 'infected',
#         'days at state': 4.6,
#         'standard_deviation': 2.5,
#         'can be infected': False,
#         'infectious': False,
#         'hospitalize': False,
#         'icu': False,
#         'activity level': 1.0,
#         'next state': [(0.4, 'asymptomatic'),
#                        (1.0, 'presymptomatic')]
#     },
#     'asymptomatic': {
#         'name': 'asymptomatic',
#         'days at state': 8.0,
#         'standard_deviation': 2.5,
#         'can be infected': False,
#         'infectious': True,
#         'hospitalize': False,
#         'icu': False,
#         'activity level': 1.0,
#         'next state': [(1.0, 'immune')]
#     },
#     'presymptomatic': {
#         'name': 'presymptomatic',
#         'days at state': 1.0,
#         'standard_deviation': 2.5,
#         'can be infected': False,
#         'infectious': True,
#         'hospitalize': False,
#         'icu': False,
#         'activity level': 1.0,
#         'next state': [(0.57, 'mild'),
#                        (0.86, 'severe'),
#                        (1.0, 'critical')]
#     },
#     'mild': {
#         'name': 'mild',
#         'days at state': 8.0,
#         'standard_deviation': 2.0,
#         'can be infected': False,
#         'infectious': True,
#         'hospitalize': False,
#         'icu': False,
#         'activity level': 0.75,
#         'next state': [(1.0, 'immune')]
#     },
#     'severe': {
#         'name': 'severe',
#         'days at state': 14.0,
#         'standard_deviation': 2.4,
#         'can be infected': False,
#         'infectious': True,
#         'hospitalize': True,
#         'icu': False,
#         'activity level': 0.00,
#         'next state': [(1.0, 'immune')]
#     },
#     'critical': {
#         'name': 'critical',
#         'days at state': 14.0,
#         'standard_deviation': 2.4,
#         'can be infected': False,
#         'infectious': True,
#         'hospitalize': True,
#         'icu': True,
#         'activity level': 0.00,
#         'next state': [(0.8, 'immune'),
#                        (1.0, 'dead')]
#     },
#     'immune': {
#         'name': 'immune',
#         'days at state': -1,
#         'can be infected': False,
#         'infectious': False,
#         'hospitalize': False,
#         'icu': False,
#         'next state': [(1.0, 'well')],
#         'death rate': 0.0
#     },
#     'dead': {
#         'name': 'dead',
#         'days at state': -1,
#         'can be infected': False,
#         'infectious': False
#     }
# }
DEFAULT_HEALTH_STATE = None
# HEALTH_STATES['well']
STATE_MODS = None


def read_from_file(file_name):
    """
    Read the states data from a file. The default if no state data is read is
    50 daily contacts with a transmission probability of 0.015, and a
    testing probability of 0.20

    :param file_name: (str, required) The name of the JSON disease description file.
    :return: None
    """
    with open(file_name, "r") as data_file:
        global HEALTH_STATES
        global DEFAULT_HEALTH_STATE
        global STATE_MODS
        disease_config = json.load(data_file)
        HEALTH_STATES = disease_config['health states']
        DEFAULT_HEALTH_STATE = HEALTH_STATES[disease_config['initial state']]
        STATE_MODS = disease_config.get('state mods', None)


def daily_update_state(sim, day):
    if STATE_MODS is not None:
        for state_mod in STATE_MODS:
            condition = state_mod['condition']
            if s.test_condition(sim,condition,day):
                # this condition was met, reset the health state state description value as specified
                path = 'HEALTH_STATES'
                last_base = HEALTH_STATES
                next_base = HEALTH_STATES
                last_key = None
                for key in state_mod['path']:
                    path += '[' + (str(key) if type(key) != str else ("'" + key + "'")) + ']'
                    last_key = key
                    last_base = next_base
                    next_base = last_base[last_key]
                print(f' on day {day} reset state value: {path} = {state_mod["value"]}                               ')
                last_base[last_key] = state_mod["value"]
    return

def get_mean_infectious_days():
    """


    :return:
    """
    # First question - why do we want this? Because the infectious days is part of the Ro
    # calculation: Ro = contacts x transmission probability x infectious days
    #
    # OK, this is really difficult because it is not the case that everybody who is contagious is
    # walking around infecting people, let us examine this a bit. In a
    # disease like COVID-19 we have a number of states that are infectious, and we can assign an activity
    # level that corresponds to the effective number of days they are circulating, for example:
    # - presymptomatic - don't know they have it, don't change behaviour, activity level 1.0
    # - asymptomatic - don't know they have it, don't change behaviour, activity level 1.0
    # - mild - guess that the average activity level is 0.5 (they don't qualify for testing unless
    #     there is known contact, if symptoms are mild it is like a cold or similar illness - which
    #     really doesn't slow us down that much).
    # - severe & critical - require hospitalization, we might guess there is a little time they had
    #     some activity, and then it became apparent there was a problem, they stayed in a bit,
    #     and then when to the hospital where they were effectively quarantined - for the sake
    #     of not over-complicating the model, let's assume anymore who is severe or critical is
    #     instantly hospitalized
    #
    # So, the average number of days a contagious person is infecting other people is a summation of:
    #   the probability of reaching that state x days at state x activity level
    mean_infectious_days = 0.0
    next_state_list = DEFAULT_HEALTH_STATE['next state']
    last_state = None
    for next_state in next_state_list:
        probability = next_state[0] - (0.0 if last_state is None else last_state[0])
        mean_infectious_days += probability * _get_mean_day_for_next_states(HEALTH_STATES[next_state[1]])
        last_state = next_state
    return mean_infectious_days


def _get_mean_day_for_next_states(this_state):
    """

    :param this_state:
    :return:
    """
    if this_state['days at state'] == -1:
        # this is a terminal state in the state tree
        return 0.0
    mean_infectious_days = int(this_state['days at state'] * this_state['activity level']) \
        if this_state['infectious'] else 0
    # break this down - the next state has a probability - so
    next_state_list = this_state['next state']
    last_state = None
    for next_state in next_state_list:
        probability = next_state[0] - (0.0 if last_state is None else last_state[0])
        mean_infectious_days += probability * _get_mean_day_for_next_states(HEALTH_STATES[next_state[1]])
        last_state = next_state
    return int(mean_infectious_days)


def set_default_health_state(person, local):
    """

    :param person:
    :param local
    :return:
    """
    person['state'] = DEFAULT_HEALTH_STATE
    person['tested'] = False
    person['days at state'] = 1
    person['state length'] = -1
    person['local'] = local
    return


def set_initial_infected_state(sim_state, person):
    """

    :param sim_state:
    :param person:
    :return:
    """
    current_state = person['state']
    if current_state is DEFAULT_HEALTH_STATE:
        # this person can be infected.
        advance_health_state(sim_state, person, current_state)
        if random.random() < .15:
            # move on from inspected to the next
            advance_health_state(sim_state, person, person['state'])
            current_state = person['state']
            if current_state['name'] == 'presymptomatic':
                advance_health_state(sim_state, person, current_state)
                if current_state['hospitalize']:
                    person['state length'] = int(random.random() * person['state length'])
        else:
            # anyone infected immediately becomes contagious
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

            if person['local']:
                if health_state['name'] == 'infected':
                    sim_state[s.DAILY_CASES] += 1
                elif health_state['name'] == 'dead':
                    # this person has died (only icu people die)
                    sim_state[s.DAILY_DEATHS] += 1
                    sim_state[s.HOSPITALIZED_PEOPLE].remove(person)
                    sim_state[s.DAILY_HOSPITALIZATIONS] -= 1
                    sim_state[s.DAILY_ICU] -= 1
                    if person['tested']:
                        sim_state[s.DAILY_CONFIRMED_DEATHS] += 1
                    return
                elif health_state['name'] == 'immune':
                    # This is someone who has recovered
                    if old_health_state['hospitalize']:
                        # This is someone that was previously hospitalized
                        sim_state[s.HOSPITALIZED_PEOPLE].remove(person)
                        sim_state[s.DAILY_HOSPITALIZATIONS] -= 1
                        sim_state[s.PEOPLE].append(person)
                        sim_state[s.DAILY_POPULATION] += 1
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
    if p_state['infectious']:
        # look for contacts with people who could be infected.
        for _ in range(int(sim_state[s.CURRENT_DAILY_CONTACTS] * p_state['activity level'])):
            contact = population[random.randint(0, population_ct - 1)]
            if contact['state']['can be infected']:
                # Oh, this the contact between 'contagious' person
                # and a healthy person who can be infected.
                if random.random() < sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]:
                    # Bummer, this is an infection contact
                    advance_health_state(sim_state, contact, contact['state'])
    return
