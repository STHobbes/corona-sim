"""These are the 'phases' the simulation goes through. Phases generally mean a change
in the conditions under which the simulation is running. Often these represent
mandated changes in behaviour of the population in effort to try to affect what
would be the normal path of the simulation."""
import simulate as s

SIMULATION_PHASES = {
    'normal': {'daily contacts': 50,
               'transmission probability': 0.015,
               'testing probability': 0.20,
               'next phase': 'lock down',
               'condition': {'type': 'cumulative confirmed cases exceeds',
                             'count': 200}},
    'lock down': {'daily contacts': 20,
                  'transmission probability': 0.01,
                  'testing probability': 0.30,
                  'next phase': 'reopen',
                  'condition': {'type': 'days after confirmed max active',
                                'days': 21}},
    'reopen': {'daily contacts': 25,
               'transmission probability': 0.012,
               'testing probability': 0.40}
}
"""
"""



def set_initial_phase(sim):
    """

    :param sim:
    :return:
    """
    set_simulation_phase(sim, 'normal', 0)


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
                  * sim[s.CURRENT_DAILY_CONTACTS]
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
