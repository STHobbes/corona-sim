import argparse
import json
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import simulate as s
import phases
import covid_state as state
import events


def run_simulation(args):
    # Setup the phases - there is a default no-phases implementation which can be overridden
    # by loading phases from a file
    if args.phases is not None:
        phases.read_from_file(args.phases)
    # Create the simulation state and initialize it to the initial state
    sim_state = s.create_initial_state(
        state.HEALTH_STATES, state.set_default_health_state,
        state.set_initial_infected_state, state.evaluate_health_for_day,
        state.evaluate_contacts, state.set_testing_for_phase,
        phases.SIMULATION_PHASES, phases.daily_phase_evaluation,
        events=events.EVENTS, daily_event_evaluation=events.evaluate_events,
        population=args.population)
    sim_state[s.CURRENT_CONTAGIOUS_DAYS] = state.get_mean_infectious_days()
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
            print(f'        start day:               {value["start day"]:14,}')
            print(f'        contacts per day:        {value["daily contacts"]:14,}')
            print(f'        transmission probability:{value["transmission probability"]:14.4f}')
            print(f'        Ro:                      {value["Ro"]:14.4f}')
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


def write_data(sim_state, file_name):
    # save the data from this simulation to a file
    phases_data = {}
    for key, value in phases.SIMULATION_PHASES.items():
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
    with open(file_name, "w") as fw:
        json.dump(data, fw, indent=2)


def plot_graphs(sim_state, phase_desc):
    # plot the results
    # These are the cumulative stats
    plt.clf()
    plt.title(
        f'Total Cases Simulation, {sim_state[s.POPULATION]} population,\n '
        f'{phase_desc}')
    plt.xlabel('days')
    plt.ylabel('cumulative number')
    plt.xticks(np.arange(0, 211, 14))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    for key, phase in phases.SIMULATION_PHASES.items():
        start_day = phase.get('start day', 0)
        if start_day > 1:
            plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day],
                        [sim_state[s.CUMULATIVE_CASES_SERIES][start_day],
                         sim_state[s.CUMULATIVE_CONFIRMED_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_ICU_CASES_SERIES][start_day],
                         sim_state[s.CUMULATIVE_RECOVERIES_SERIES][start_day],
                         sim_state[s.CUMULATIVE_DEATHS_SERIES][start_day]],
                        label=key)
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

    # plot the results
    # These are the cumulative stats
    plt.clf()
    plt.title(
        f'Active Cases Simulation, {sim_state[s.POPULATION]} population,\n '
        f'{phase_desc}')
    plt.xlabel('days')
    plt.ylabel('active count')
    plt.xticks(np.arange(0, 211, 14))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    for key, phase in phases.SIMULATION_PHASES.items():
        start_day = phase.get('start day', 0)
        if start_day > 1:
            plt.scatter([start_day, start_day, start_day, start_day],
                        [sim_state[s.ACTIVE_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES][start_day],
                         sim_state[s.ACTIVE_ICU_CASES_SERIES][start_day]],
                        label=key)
    plt.plot(sim_state[s.ACTIVE_CASES_SERIES], label='active cases')
    plt.plot(sim_state[s.ACTIVE_CONFIRMED_CASES_SERIES], label='active confirmed cases')
    plt.plot(sim_state[s.ACTIVE_HOSPITALIZED_CASES_SERIES], label='active hospitalization')
    plt.plot(sim_state[s.ACTIVE_ICU_CASES_SERIES], label='active icu')
    plt.legend()
    plt.show()
    plt.pause(0.1)

    # These are the daily stats
    plt.clf()
    plt.title(
        f'Daily Cases Simulation, {sim_state[s.POPULATION]} population,\n '
        f'{phase_desc}')
    plt.xlabel('days')
    plt.ylabel('daily number')
    plt.xticks(np.arange(0, 211, 14))
    plt.grid(b=True, which='major', color='#aaaaff', linestyle='-')
    for key, phase in phases.SIMULATION_PHASES.items():
        start_day = phase.get('start day', 0)
        if start_day > 1:
            plt.scatter([start_day, start_day, start_day, start_day, start_day, start_day],
                        [sim_state[s.NEW_CASES_SERIES][start_day],
                         sim_state[s.NEW_CONFIRMED_CASES_SERIES][start_day],
                         sim_state[s.NEW_ACTIVE_CASES_SERIES][start_day],
                         sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES][start_day],
                         sim_state[s.NEW_RECOVERIES_SERIES][start_day],
                         sim_state[s.NEW_DEATHS_SERIES][start_day]],
                        label=key)
    plt.plot(sim_state[s.NEW_CASES_SERIES], label='daily new cases')
    plt.plot(sim_state[s.NEW_CONFIRMED_CASES_SERIES], label='daily new confirmed cases')
    plt.plot(sim_state[s.NEW_ACTIVE_CASES_SERIES], label='daily active cases')
    plt.plot(sim_state[s.NEW_CONFIRMED_ACTIVE_CASES_SERIES], label='daily active confirmed cases')
    plt.plot(sim_state[s.NEW_RECOVERIES_SERIES], label='daily recoveries')
    plt.plot(sim_state[s.NEW_DEATHS_SERIES], label='daily deaths')
    plt.legend()
    plt.show()
    plt.pause(0.1)


parser = argparse.ArgumentParser(
    description='Run s simulation of in infectious disease spreading through a population.')
parser.add_argument('-ph', '--phases', dest='phases', type=str, default=None,
                    help='The json file containing the simulation phases description.')
parser.add_argument('-st', '--states', dest='states', type=str, default='./data/default_states.json',
                    help='The json file containing the health states data for the disease.')
parser.add_argument('-o', '--output', dest='base', type=str, default=None,
                    help='The base name of the .json file(s) to which the data from the simulation will be written.')
parser.add_argument("-p", "--population", dest='population', type=int, default=50000,
                    help='The population for the simulation.')
parser.add_argument("-g", "--graphs", dest='graphs', action="store_true",
                    help='Display the graphs for the simulation.')
parser.add_argument("-r", "--runs", dest='runs', type=int, default=0,
                    help='The number of runs for the set, 1 seeded run is always included')
args = parser.parse_args()

print(f'phases file:          {args.phases}')
print(f'health states file:   {args.states}')
print(f'output file(s) base:  {args.base}')
print(f'population:           {args.population}')
print(f'display graphs:       {args.graphs}')
print(f'random runs:          {args.runs}')

# The seeded run
random.seed(42)
print('-------------------------------------------------------------------------------')
print('---   Seeded Run                                                            ---')
print('-------------------------------------------------------------------------------')
sim, sub_title = run_simulation(args)
if args.base is not None:
    write_data(sim, f'{args.base}.json')
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
        write_data(sim, f'{args.base}_{run_id}.json')
