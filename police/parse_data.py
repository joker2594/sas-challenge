import pandas as pd
from collections import defaultdict, Counter
from geopy.distance import vincenty, great_circle
from pandas import DataFrame, Series
import json


def create_grid(records):

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

    vertical_distance = great_circle(left_up_corner, right_up_corner).miles
    horizontal_distance = great_circle(left_up_corner, left_down_corner).miles

    horizontal_section = abs(max_lat - min_lat) / float(horizontal_distance)
    vertical_section = abs(max_long - min_long) / float(vertical_distance)

    return horizontal_section, vertical_section


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


related_events = {}
path = 'CityEvents.txt'
BAD_EVENTS = ['ROBBERY', 'MURDER', 'MUGGING', 'FRAUD']
excluded = []

records = pd.read_csv(path, names=['wday', 'month', 'day', 'time', 'tz', 'year', 'lat', 'long', 'type', 'affected'],
                      header=None, delim_whitespace=True)


# # types_count = frame['type'].value_counts()
# victims_count = frame.sort(columns='affected', ascending=False)
# vc_above15k = frame[frame['affected'] > 15000]
# # print len(vc_above15k)
# # print frame[:10]
# t = frame.loc[100]
# # print '>>>>', frame.loc[(frame['wday'] == 'Mon') & (frame['affected'] == 26)].values
#
# #events = search_near_events(frame, t)
# #print len(events)

frame = DataFrame(records)

i=0
for d in frame.iterrows():

    if d[1]['type'] in BAD_EVENTS:
        if d[0] not in excluded:
            near_events = search_near_events(frame, d)
            related_events[i] = near_events

        print i
    i += 1


with open('related_events.txt', 'w') as fp:
    json.dump(related_events, fp)


'''
for event in related_events:
    print event, ' --> ', len(related_events[event])
    print '-----------------------------------------------'
    print
'''




