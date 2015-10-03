import pandas as pd
from collections import defaultdict, Counter
from geopy.distance import vincenty, great_circle


def get_counts(sequence):
    counts = defaultdict(int) # values will initialize to 0
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

    return grid

path = 'CityEvents.txt'
records = pd.read_csv(path, names=['wday', 'month', 'day', 'time', 'tz', 'year', 'lat', 'long', 'type', 'affected'],
                      header=None, delim_whitespace=True)

victims = records['affected']
count_victims = get_counts(victims)

'''
types = records['type']
type_count = get_counts(types)
counts = Counter(type_count)
print latitudes.min()
print latitudes.max()
print
print longitudes.min()
print longitudes.max()
'''

