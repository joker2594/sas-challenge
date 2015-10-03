import pandas as pd
from collections import defaultdict, Counter
from geopy.distance import vincenty, great_circle
from pandas import DataFrame, Series
import json



def get_counts(sequence):
    counts = defaultdict(int)  # values will initialize to 0
    for x in sequence:
        counts[x] += 1
    return counts


def create_grid(records):
    grid_points = {'horizontal': [], 'vertical': []}
    grid = []

    latitudes = records['lat']
    longitudes = records['long']

    min_lat = latitudes.min()
    max_lat = latitudes.max()

    min_long = longitudes.min()
    max_long = longitudes.max()

    left_up_corner = (max_lat, min_long)
    left_down_corner = (min_lat, min_long)
    right_up_corner = (max_lat, max_long)
    right_down_corner = (min_lat, max_long)

    corners = [left_up_corner, right_up_corner, right_down_corner, left_down_corner]

    vertical_distance = great_circle(left_up_corner, right_up_corner).miles
    horizontal_distance = great_circle(left_up_corner, left_down_corner).miles

    horizontal_section = abs(max_lat - min_lat) / float(horizontal_distance)
    vertical_section = abs(max_long - min_long) / float(vertical_distance)

    return horizontal_section, vertical_section

    '''

    # calculate vertical points
    current_long = min_long
    while current_long < max_long:
        grid_points['vertical'].append(current_long)
        current_long += horizontal_section

    # calculate horizontal points
    current_lat = min_lat
    while current_lat < max_lat:
        grid_points['horizontal'].append(current_lat)
        current_lat += vertical_section

    # make sections
    for i in range(len(grid_points['vertical']) - 1):
        for j in range(len(grid_points['horizontal']) - 1):

            grid.append([(grid_points['vertical'][i], grid_points['horizontal'][j]),
                         (grid_points['vertical'][i+1]), grid_points['horizontal'][j+1]])

    '''


def search_near_events(df, event):
    events = []
    fe = event[1]
    fe_point = (fe['lat'], fe['long'])

    for d in df.iterrows():
        se = d[1]
        se_point = (se['lat'], se['long'])

        if great_circle(fe_point, se_point).miles <= 1:
            events.append(int(d[0]))
            if se['type'] in BAD_EVENTS:
                excluded.append(d[0])

    return events

    '''
    hsection = 0.0144691017081
    vsection = 0.0258757383572
    '''

    # return df.loc[(df['lat'] >= (e['lat'] + hsection)) | (df['lat'])]


related_events = {}
path = 'CityEvents.txt'
BAD_EVENTS = ['ROBBERY', 'MURDER', 'MUGGING', 'FRAUD']
excluded = []

records = pd.read_csv(path, names=['wday', 'month', 'day', 'time', 'tz', 'year', 'lat', 'long', 'type', 'affected'],
                      header=None, delim_whitespace=True)

frame = DataFrame(records)
# types_count = frame['type'].value_counts()
victims_count = frame.sort(columns='affected', ascending=False)
vc_above15k = frame[frame['affected'] > 15000]
# print len(vc_above15k)
# print frame[:10]
t = frame.loc[100]
# print '>>>>', frame.loc[(frame['wday'] == 'Mon') & (frame['affected'] == 26)].values

#events = search_near_events(frame, t)
#print len(events)

i=0
for d in frame.iterrows():

    if d[1]['type'] in BAD_EVENTS:
        if d[0] not in excluded:
            near_events = search_near_events(frame, d)
            related_events[i] = near_events

        print i
    i += 1

#print len(related_events)
#print related_events
with open('related_events.txt', 'w') as fp:
    json.dump(related_events, fp)


'''
for event in related_events:
    print event, ' --> ', len(related_events[event])
    print '-----------------------------------------------'
    print
'''




