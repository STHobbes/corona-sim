import argparse
import random
import time
import simulate as s
import phases
import covid_state as state
import events


def run_simulation(args):
    # Setup the phases - there is a default no-phases implementation which
    # can be overridden by loading phases from a file
    if args.phases is not None:
        phases.read_from_file(args.phases)
    # Setup the events - there is a default no-events implementation and
    # events can be loaded by event files
    if args.events is not None:
        events.read_from_file(*[file_name.strip() for file_name in args.events.split(',')])
    # Create the simulation state and initialize it to the initial state
    sim_state = s.create_initial_state(
        state.HEALTH_STATES, state.set_default_health_state,
        state.set_initial_infected_state, state.evaluate_health_for_day,
        state.evaluate_contacts, state.set_testing_for_phase,
        phases.SIMULATION_PHASES, phases.daily_phase_evaluation,
        events=events.EVENTS, daily_event_evaluation=events.evaluate_events,
        population=args.population, simulation_days=args.sim_days,
        initial_infection=args.infection
    )
    sim_state[s.CURRENT_CONTAGIOUS_DAYS] = state.get_mean_infectious_days()
    print(f' Contagious days for this disease: {sim_state[s.CURRENT_CONTAGIOUS_DAYS]:.2f}')
    phases.set_initial_phase(sim_state)
    state.set_testing_for_phase(sim_state[s.CURRENT_TESTING_PROBABILITY])

    # Everything is setup, get the start time for the simulation
    start = time.time()
    s.run_simulation(sim_state)

    # print the results of the simulation
    phase_desc = ''
    print(f'Simulation Summary:')
    print(f'  Setup:')
    print(f'    Simulation Days:           {sim_state[s.SIMULATION_DAYS]:16,}')
    print(f'    Population:                {sim_state[s.POPULATION]:16,}')
    print(f'    Initial Infection:         {sim_state[s.INITIAL_INFECTION]:16,}')
    # print(f'    Days Contagious:           {HEALTH_STATES["contagious"]["days at state"]:16,}')
    print(f'    Phases:')
    for key, value in phases.SIMULATION_PHASES.items():
        if 'start day' in value:
            print(f'      {key}:')
            print(f'        start day:               {value["start day"]:16,}')
            print(f'        contacts per day:        {value["daily contacts"]:16,}')
            print(f'        transmission probability:{value["transmission probability"]:16.4f}')
            print(f'        Ro:                      {value["Ro"]:16.4f}')
            print(f'        daily new cases:         {sim_state[s.NEW_CASES_SERIES][value["start day"]]:16,}')
            print(f'        cumulative cases:        {sim_state[s.CUMULATIVE_CASES_SERIES][value["start day"]]:16,}')
            print(f'        deaths:                  '
                  f'{sim_state[s.CUMULATIVE_CONFIRMED_DEATHS_SERIES][value["start day"]]:16,}')
            if phase_desc != '':
                phase_desc += ', '
            phase_desc += f'{key} Ro={value["Ro"]:.2f}'
    print(f'  Daily:')
    print(f'    Max Daily New Cases:')
    print(f'      On Day:                        {sim_state[s.MAX_NEW_DAILY_CASES]:16,}')
    print(f'      Number of New Cases:           {sim_state[s.NEW_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]]:16,}')
    print(
        f'      Cumulative Cases:              {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]]:16,}'
        f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_NEW_DAILY_CASES]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(f'    Maximum Active Cases:')
    print(f'      On Day:                        {sim_state[s.MAX_ACTIVE_CASES]:16,}')
    print(f'      Number of Active Cases:        {sim_state[s.ACTIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]]:16,}')
    print(
        f'      Cumulative Cases:              {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]]:16,}'
        f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.MAX_ACTIVE_CASES]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(f'    Maximum Hospitalized Cases:')
    print(f'      On Day:                        {sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS]:16,}')
    print(f'      Max Hospitalized Cases:        '
          f'{sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][sim_state[s.MAX_ACTIVE_HOSPITALIZATIONS]]:16,}')
    print(f'    Maximum ICU Beds:')
    print(f'      On Day:                        {sim_state[s.MAX_ACTIVE_ICU]:16,}')
    print(f'      Number of ICU Beds:            '
          f'{sim_state[s.ACTIVE_ICU_CASES_SERIES][sim_state[s.MAX_ACTIVE_ICU]]:16,}')
    print(f'  Cumulative:')
    print(
        f'    Cumulative Cases:                {sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
        f'({sim_state[s.CUMULATIVE_CASES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(
        f'    Cumulative Recoveries:           {sim_state[s.CUMULATIVE_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
        f'({sim_state[s.CUMULATIVE_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(
        f'    Cumulative Deaths:               {sim_state[s.CUMULATIVE_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
        f'({sim_state[s.CUMULATIVE_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(
        f'    Cumulative Confirmed Cases:      {sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
        f'({sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(
        f'    Cumulative Confirmed Recoveries: {sim_state[s.CUMULATIVE_CONFIRMED_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
        f'({sim_state[s.CUMULATIVE_CONFIRMED_RECOVERIES_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')
    print(
        f'    Cumulative Confirmed Deaths:     {sim_state[s.CUMULATIVE_CONFIRMED_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]]:16,}'
        f'({sim_state[s.CUMULATIVE_CONFIRMED_DEATHS_SERIES][sim_state[s.SIMULATION_DAYS]] * 100.0 / sim_state[s.POPULATION]:5.2f}%)')

    print(f'\nSimulation time: {time.time() - start:.4f}sec\n')
    return sim_state, phase_desc


def plot_graphs(sim_state, phase_desc):
    s.graph_simulation(
        sim_state, f'Total Cases Simulation, {sim_state[s.POPULATION]} population,\n {phase_desc}',
        [s.CUMULATIVE_CASES_SERIES, s.CUMULATIVE_CONFIRMED_CASES_SERIES, s.ACTIVE_CASES_SERIES,
         s.ACTIVE_CONFIRMED_CASES_SERIES, s.ACTIVE_HOSPITALIZED_CASES_SERIES, s.ACTIVE_ICU_CASES_SERIES,
         s.CUMULATIVE_RECOVERIES_SERIES, s.CUMULATIVE_DEATHS_SERIES])

    s.graph_simulation(
        sim_state, f'Active Cases Simulation, {sim_state[s.POPULATION]} population,\n {phase_desc}',
        [s.ACTIVE_CASES_SERIES, s.ACTIVE_CONFIRMED_CASES_SERIES,
         s.ACTIVE_HOSPITALIZED_CASES_SERIES, s.ACTIVE_ICU_CASES_SERIES])

    s.graph_simulation(
        sim_state, f'Daily Cases Simulation, {sim_state[s.POPULATION]} population,\n {phase_desc}',
        [s.NEW_CASES_SERIES, s.NEW_CONFIRMED_CASES_SERIES, s.NEW_ACTIVE_CASES_SERIES,
         s.NEW_CONFIRMED_ACTIVE_CASES_SERIES, s.NEW_RECOVERIES_SERIES, s.NEW_DEATHS_SERIES])


# ----------------------------------------------------------------------------------------------------------------------
# Lets run some simulations -
# - Start by parsing the arguments that configure this simulation run
# ----------------------------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='Run s simulation of in infectious disease spreading through a population.')
parser.add_argument(
    '-ph', '--phases', dest='phases', type=str, default=None,
    help='The JSON file containing the simulation phases description.')
parser.add_argument(
    '-st', '--states', dest='states', type=str, default='./data/default_states.json',
    help='The JSON file containing the health states data for the disease.')
parser.add_argument(
    '-e', '--events', dest='events', type=str, default=None,
    help='The JSON files containing the events descriptions, comma separated.')
parser.add_argument(
    '-o', '--output', dest='base', type=str, default=None,
    help='The base name of the .json file(s) to which the data from the simulation will be written.')
parser.add_argument(
    '-p', '--population', dest='population', type=int, default=s.DEFAULT_POPULATION,
    help='The population for the simulation.')
parser.add_argument(
    '-d', '--days', dest='sim_days', type=int, default=s.DEFAULT_SIMULATION_DAYS,
    help='The length of the simulation in days.')
parser.add_argument(
    '-i', '--infection', dest='infection', type=int, default=s.DEFAULT_INITIAL_INFECTION,
    help='The default infection (not tested).')
parser.add_argument(
    '-g', '--graphs', dest='graphs', action='store_true',
    help='Display the graphs for the simulation.')
parser.add_argument(
    '-r', '--runs', dest='runs', type=int, default=0,
    help='The number of runs for the set, 1 seeded run is always included')
args = parser.parse_args()

print('---------------------------------------------------------')
print('---    INFECTIOUS DISEASE SIMULATION CONFIGURATION    ---')
print('---------------------------------------------------------')
print(f'population:               {args.population}')
print(f'simulation length (days): {args.sim_days}')
print(f'initial infection:        {args.infection}')
print(f'phases file:              {args.phases}')
print(f'health states file:       {args.states}')
print(f'output file(s) base:      {args.base}')
print(f'events:                   {args.events}')
print(f'display graphs:           {args.graphs}')
print(f'random runs:              {args.runs}')
print('---------------------------------------------------------')

# The seeded run
random.seed(42)
print('-------------------------------------------------------------------------------')
print('---   Seeded Run                                                            ---')
print('-------------------------------------------------------------------------------')
sim, sub_title = run_simulation(args)
if args.base is not None:
    s.write_data(sim, f'{args.base}.json')
if args.graphs:
    plot_graphs(sim, sub_title)

# random runs

if args.runs > 0 and args.base is not None:
    for run_id in range(args.runs):
        print('-------------------------------------------------------------------------------')
        print(f'---   Random Run {run_id:2d}                                                         ---')
        print('-------------------------------------------------------------------------------')
        random.seed(int(time.time()))
        sim, sub_title = run_simulation(args)
        s.write_data(sim, f'{args.base}_{run_id}.json')
