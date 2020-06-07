import expl_tools as tools

data_dir = './data/expl3/'
test_set = tools.read_run_set(data_dir, 'cov_50000')
event_set = tools.read_run_set(data_dir, 'cov_50000_e70')

ave_active_cases = tools.plot_run_set(test_set, 'active_cases_series',
             f'Active Cases Simulation, pop - 50,000\nlock down at 200 confirmed',
             ylabel='active cases')

ave_active_confirmed_cases = tools.plot_run_set(test_set, 'active_confirmed_cases_series',
             f'Active Confirmed Cases Simulation, pop - 50,000\nlock down at 200 confirmed',
             ylabel='active confirmed cases')

ave_deaths = tools.plot_run_set(test_set, 'cumulative_deaths_series',
             f'Active Confirmed Cases Simulation, pop - 50,000\nlock down at 200 confirmed',
             ylabel='active confirmed cases')

ave_active_cases_event = tools.plot_run_set(event_set, 'active_cases_series',
             f'Active Cases Simulation, pop - 50,000\nlock down at 200 confirmed, event at day 70',
             ylabel='active cases')

ave_active_confirmed_cases_event = tools.plot_run_set(event_set, 'active_confirmed_cases_series',
             f'Active Confirmed Cases Simulation, pop - 50,000\n for various lock down timing, event at day 70',
             ylabel='active confirmed cases')

ave_deaths_event = tools.plot_run_set(event_set, 'cumulative_deaths_series',
             f'Active Confirmed Cases Simulation, pop - 50,000\n for various lock down timing, event at day 70',
             ylabel='active confirmed cases')

phased_events_comp = {
    'active confirmed': ave_active_confirmed_cases,
    'active confirmed with event': ave_active_confirmed_cases_event,
    'cumulative deaths': ave_deaths,
    'cumulative deaths with event': ave_deaths_event
}

tools.plot_curves(phased_events_comp, 'comparison when events occur')
