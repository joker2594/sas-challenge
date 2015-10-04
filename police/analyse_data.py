import json
import pandas as pd
from pandas import DataFrame
import os
import operator


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
related_events_path = os.path.join(BASE_DIR, 'police/related_events.txt')
city_event_path = os.path.join(BASE_DIR, 'police/CityEvents.txt')

related_events = json.load(open(related_events_path))

records = pd.read_csv(city_event_path, names=['wday', 'month', 'day', 'time', 'tz', 'year', 'lat', 'long', 'type', 'affected'],
                      header=None, delim_whitespace=True)

frame = DataFrame(records)
events = {}
important_events = {}
BAD_EVENTS = ['ROBBERY', 'MURDER', 'MUGGING', 'FRAUD']
IMPORTANCE = {'MURDER': 10, 'ROBBERY': 9, 'MUGGING': 8, 'FRAUD': 7, 'RACE': 2, 'SPEECH': 3, 'RIVER': 1, 'FOOTBALL': 2,
              'DEMONSTRATION': 2, 'CONCERT': 1, 'ATHLETICS': 1, 'CHARITY': 2, 'MARCH': 2, 'PICKET': 3}


# compute the number of crimes in each area
def set_crimes_number():
    for event in related_events:
        events[event] = {'near_events': related_events[event], 'crimes': 0}
        for e in events[event]['near_events']:
            ev = frame.loc[e]

            if ev['type'] in BAD_EVENTS:
                events[event]['crimes'] += 1


# get the areas with more than <value> crimes
def set_important_events(value=10):
    for event in events:
        if events[event]['crimes'] > value:
            important_events[event] = events[event]


def get_most_common(events):
    types = {'MURDER': 0, 'ROBBERY': 0, 'MUGGING': 0, 'FRAUD': 0, 'RACE': 0, 'SPEECH': 0, 'RIVER': 0, 'FOOTBALL': 0,
              'DEMONSTRATION': 0, 'CONCERT': 0, 'ATHLETICS': 0, 'CHARITY': 0, 'MARCH': 0, 'PICKET': 0}
    for event in events:
        e = frame.loc[event]
        if e['type'] in types.keys():
            types[e['type']] += 1

    sorted_types = sorted(types.items(), key=operator.itemgetter(1))

    return sorted_types[::-1][0]


# update the most important events with the rest of the fields
def build():
    for e in important_events:
        important_events[e]['importance'] = 0
        important_events[e]['affected'] = 0
        important_events[e]['most_common'] = get_most_common(important_events[e]['near_events'])

        for event in important_events[e]['near_events']:
            nested_event = frame.loc[event]
            important_events[e]['lat'] = nested_event['lat']
            important_events[e]['long'] = nested_event['long']
            important_events[e]['importance'] += IMPORTANCE[nested_event['type']] * nested_event['affected']
            important_events[e]['affected'] += nested_event['affected']




# get event with most importance
def get_highest_threat():
    highest_threat = 0
    for e in important_events:
        if highest_threat < important_events[e]['importance']:
            highest_threat = important_events[e]['importance']

    return highest_threat


# convert importance to percentage
def set_percentages():
    for e in important_events:
        important_events[e]['priority_percentage'] = float(important_events[e]['importance']*100/get_highest_threat())


# get a dictionary of important events
def get_most_important_events():
    set_crimes_number()
    set_important_events()
    build()
    set_percentages()

    return important_events


# get a json of most important events
def get_most_important_events_json():
    data = get_most_important_events()
    data_to_json_dict = {}
    data_list = []

    for event in data:
        data_to_json_dict[event] = {'lat': data[event]['lat'], 'long': data[event]['long'],
                                    'percentage': data[event]['priority_percentage']}

    for s in sorted(data_to_json_dict.iteritems(), key=lambda (x, y): y['percentage']):
        data_list.append({s[0]: s[1]})

    data_list_to_json = data_list[::-1]
    data_json = json.dumps(data_list_to_json)

    return data_json







