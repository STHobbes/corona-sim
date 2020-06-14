import json
import random
import simulate as s

EVENTS = []


# day - the day of the simulation for the event
# duration - the duration of the event, hours
# participants - the number of people participating in the event
# visiting participants - the number of participants from outside the local population
# infected visiting - the fraction of the visiting population that is infectious (we know
#   our local population infections.
# site - 'inside', 'outside', 'mixed'
# seating -
#   'fixed' - as in an auditorium or theatre,
#   'standing' - as in an outdoor event,
#   'separated tables' - as in an awards dinner,
#   'booths' - as in a trade show
# masked - true or false
# full duration contacts - # of people within 6 ft for the duration of the event
# casual contacts - # of people casually contacted (brief passing conversation)

def read_from_file(*file_names):
    global EVENTS
    events = []
    for file_name in file_names:
        with open(file_name, "r") as data_file:
            events.append(json.load(data_file))
    EVENTS = events


def evaluate_events(sim_state, day):
    for event in EVENTS:
        if event.get('day', -1) == day or \
                (event.get('start day', -1) <= day <= event.get('end day', -1)):
            # OK, this event happens or starts today
            print(f'{event["description"]} on day {day}')
            # What is the probability of infection for the event?
            # full duration contacts - use 3 x normal transmission possibility CURRENT_TRANSMISSION_PROBABILITY
            #    * number of hours * .5 for masked * (1.5 if inside, 1.0 otherwise)
            # casual contacts are at the CURRENT_TRANSMISSION_PROBABILITY
            full_duration_probability = \
                3.0 * (sim_state[s.CURRENT_TRANSMISSION_PROBABILITY] if
                       event['distanced'] else sim_state[s.NORMAL_TRANSMISSION_PROBABILITY]) * \
                event['duration']
            if event['masked']:
                full_duration_probability *= 0.5
            if event['site'] == 'inside':
                full_duration_probability *= 1.5

            casual_probability = 3.0 * (sim_state[s.CURRENT_TRANSMISSION_PROBABILITY] if
                                        event['distanced'] else sim_state[s.NORMAL_TRANSMISSION_PROBABILITY])
            if event['site'] == 'inside':
                casual_probability *= 1.5

            # create the event population - take a random sample
            event_people = event.get('people', None)
            if event_people is None:
                event_people = event['people'] = []
                for _ in range(event['participants'] - event['visiting participants']):
                    event_people.append(sim_state[s.PEOPLE][random.randint(0, sim_state[s.DAILY_POPULATION] - 1)])

                for person_id in range(event['participants'] - event['visiting participants']):
                    person = {'id': -(person_id + 1)}
                    sim_state[s.SET_DEFAULT_HEALTH](person, False)
                    if random.random() < event['infected visiting']:
                        sim_state[s.SET_INFECTED](person)
                        sim_state[s.DAILY_HEALTH_EVALUATION](sim_state, person)

                    event_people.append(person)
            else:
                # the local population has already been updated, update the visiting population
                for person in event_people:
                    if person['local']:
                        state = person['state']
                        if state['name'] == 'dead' or state['hospitalize']:
                            # this person is out of the pool, replace them
                            event_people.remove(person)
                            event_people.append(
                                sim_state[s.PEOPLE][random.randint(0, sim_state[s.DAILY_POPULATION] - 1)])
                    else:
                        sim_state[s.DAILY_HEALTH_EVALUATION](sim_state, person)

            phase_daily_contacts = sim_state[s.CURRENT_DAILY_CONTACTS]
            phase_transmission_probability = sim_state[s.CURRENT_TRANSMISSION_PROBABILITY]
            # now do the full duration contacts
            sim_state[s.CURRENT_DAILY_CONTACTS] = event['full duration contacts']
            sim_state[s.CURRENT_TRANSMISSION_PROBABILITY] = full_duration_probability
            for person in event_people:
                # can this person infect, or be infected - if so, daily contacts
                # must be traced to see if there is an infection event
                sim_state[s.DAILY_EVALUATE_CONTACTS](sim_state, person, event_people)

            # now do the casual contacts
            sim_state[s.CURRENT_DAILY_CONTACTS] = event['casual contacts']
            sim_state[s.CURRENT_TRANSMISSION_PROBABILITY] = casual_probability
            for person in event_people:
                # can this person infect, or be infected - if so, daily contacts
                # must be traced to see if there is an infection event
                sim_state[s.DAILY_EVALUATE_CONTACTS](sim_state, person, event_people)

            # and reset the phase parameters
            sim_state[s.CURRENT_DAILY_CONTACTS] = phase_daily_contacts
            sim_state[s.CURRENT_TRANSMISSION_PROBABILITY] = phase_transmission_probability

            if event.get('end day', -1) == day:
                del event['people']

    return
