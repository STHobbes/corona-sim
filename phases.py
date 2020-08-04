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
    'normal': {'daily contacts': 24,
               'transmission probability': 0.031,
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
    Read the phases data from a file. The default if no phase data is read is
    50 daily contacts with a transmission probability of 0.015, and a
    testing probability of 0.20

    :param file_name: (str, required) The name of the JSON phases description file.
    :return: None
    """
    with open(file_name, "r") as data_file:
        global SIMULATION_PHASES
        global INITIAL_PHASE
        phases_config = json.load(data_file)
        SIMULATION_PHASES = phases_config['phases']
        INITIAL_PHASE = phases_config['initial phase']


def set_initial_phase(sim):
    """
    Set the initial phase for the simulation.

    :param sim: (dict, required) The simulation state.
    :return: None
    """
    _set_simulation_phase(sim, INITIAL_PHASE, 0)
    sim[s.NORMAL_DAILY_CONTACTS] = sim[s.CURRENT_DAILY_CONTACTS]
    sim[s.NORMAL_TRANSMISSION_PROBABILITY] = sim[s.CURRENT_TRANSMISSION_PROBABILITY]


def _set_simulation_phase(sim, phase_key, start_day):
    """
    Set a simulation phase (this is a local method).

    :param sim: (dict, required) The simulation state.
    :param phase_key: (str, required) The name of the phase to be started
    :param start_day: (int, required) The day that this phase is starting.
    :return: None
    """
    phase = sim[s.CURRENT_PHASE] = SIMULATION_PHASES[phase_key]
    sim[s.HAS_NEXT_PHASE] = 'next phase' in phase and 'condition' in phase
    sim[s.CURRENT_DAILY_CONTACTS] = phase['daily contacts']
    sim[s.CURRENT_TRANSMISSION_PROBABILITY] = phase['transmission probability']
    sim[s.CURRENT_TESTING_PROBABILITY] = phase.get('testing probability', 1.0)
    phase['Ro'] = sim[s.CURRENT_DAILY_CONTACTS] * sim[s.CURRENT_TRANSMISSION_PROBABILITY] \
                  * sim[s.CURRENT_CONTAGIOUS_DAYS]
    phase['start day'] = start_day
    print(f' advance to {phase["name"]} on day {start_day},'
          f' Ro={phase["Ro"]}                                                             ')
    return


def daily_phase_evaluation(sim, day):
    """
    Examine the data for this day

    :param sim: (dict, required) The simulation state.
    :param day: (int, required) The day of the simulation for which the phase
    is being evaluated.
    :return: (bool) True if the state has advanced, False otherwise
    """
    advance = False
    if sim[s.HAS_NEXT_PHASE]:
        condition = sim[s.CURRENT_PHASE]['condition']
        # if condition['type'] == 'cumulative cases exceeds':
        #     advance = sim[s.CUMULATIVE_CASES_SERIES][day] >= condition['count']
        # elif condition['type'] == 'daily new confirmed above':
        #     advance = sim[s.NEW_CONFIRMED_CASES_SERIES][day] >= condition['count']
        # elif condition['type'] == 'daily new confirmed below':
        #     advance = sim[s.NEW_CONFIRMED_CASES_SERIES][day] <= condition['count']
        # elif condition['type'] == 'cumulative confirmed cases exceeds':
        #     advance = sim[s.CUMULATIVE_CONFIRMED_CASES_SERIES][day] >= condition['count']
        # elif condition['type'] == 'days after max active':
        #     advance = day - sim[s.MAX_ACTIVE_CASES] > condition['days']
        # elif condition['type'] == 'days after confirmed max active':
        #     advance = day - sim[s.MAX_ACTIVE_CONFIRMED_CASES] > condition['days']
        # elif condition['type'] == 'days in phase':
        #     advance = day - sim[s.CURRENT_PHASE]['start day'] > condition['days']
        # elif condition['type'] == 'day in simulation':
        #     advance = day == condition['day']
        # else:
        #     print(f'Unrecognized phase advancement condition: "{condition["type"]}"')

        advance = s.test_condition(sim, condition, day)
        if advance:
            _set_simulation_phase(sim, sim[s.CURRENT_PHASE]['next phase'], day)

    return advance
