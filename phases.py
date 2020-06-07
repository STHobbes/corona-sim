"""These are the 'phases' the simulation goes through. Phases generally mean a change
in the conditions under which the simulation is running. Often these represent
mandated changes in behaviour of the population in effort to try to affect what
would be the normal path of the simulation.

Phases are described in a dictionary where the key is the name of the phase, and
the value is a dictionary describing the values for the phase and the conditions
for moving to the next phase.
"""
import json
import simulate as s

SIMULATION_PHASES = {
    'normal': {'daily contacts': 50,
               'transmission probability': 0.015,
               'testing probability': 0.20
               }
}
INITIAL_PHASE = 'normal'
"""
The phases for the simulation. The default runs the simulation wit no phases
and is what would happen if no action is taken to combat the infectious disease,
people behave normally, and the disease runs its course.
"""


def read_from_file(file_name):
    """

    :param file_name:
    :return:
    """
    with open(file_name, "r") as data_file:
        global SIMULATION_PHASES
        global INITIAL_PHASE
        phases_config = json.load(data_file)
        SIMULATION_PHASES = phases_config['phases']
        INITIAL_PHASE = phases_config['initial phase']


def set_initial_phase(sim):
    """

    :param sim:
    :return:
    """
    set_simulation_phase(sim, INITIAL_PHASE, 0)


def set_simulation_phase(sim, phase_key, start_day):
    """

    :param sim:
    :param phase_key:
    :param start_day:
    :return:
    """
    phase = sim[s.CURRENT_PHASE] = SIMULATION_PHASES[phase_key]
    sim[s.HAS_NEXT_PHASE] = 'next phase' in phase and 'condition' in phase
    sim[s.CURRENT_DAILY_CONTACTS] = phase['daily contacts']
    sim[s.CURRENT_TRANSMISSION_PROBABILITY] = phase['transmission probability']
    sim[s.CURRENT_TESTING_PROBABILITY] = phase.get('testing probability', 1.0)
    phase['Ro'] = sim[s.CURRENT_DAILY_CONTACTS] * sim[s.CURRENT_TRANSMISSION_PROBABILITY] \
                  * sim[s.CURRENT_CONTAGIOUS_DAYS]
    phase['start day'] = start_day
    return


def daily_phase_evaluation(sim, day):
    """

    :param sim:
    :param day:
    :return:
    """
    if sim[s.HAS_NEXT_PHASE]:
        condition = sim[s.CURRENT_PHASE]['condition']
        advance = False
        if condition['type'] == 'cumulative cases exceeds':
            advance = sim[s.CUMULATIVE_CASES_SERIES][day] >= condition['count']
        elif condition['type'] == 'cumulative confirmed cases exceeds':
            advance = sim[s.CUMULATIVE_CONFIRMED_CASES_SERIES][day] >= condition['count']
        elif condition['type'] == 'days after max active':
            advance = day - sim[s.MAX_ACTIVE_CASES] > condition['days']
        elif condition['type'] == 'days after confirmed max active':
            advance = day - sim[s.MAX_ACTIVE_CONFIRMED_CASES] > condition['days']
        # Add new conditions here
        if advance:
            print(f' advance to {sim[s.CURRENT_PHASE]["next phase"]} on day {day}')
            set_simulation_phase(sim, sim[s.CURRENT_PHASE]['next phase'], day)
            return True
