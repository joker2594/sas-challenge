from django.shortcuts import render
from django.http import HttpResponse
import geocoder
import analyse_data as ad
import json


def index(request):
    context_dict = ""
    return render(request, 'index.html', context_dict)


def deploy(request):
    data = json.loads(ad.get_most_important_events_json())
    locations = []
    for location in data:
        locations.append(location[location.keys()[0]])

    #groups = 2
    #officers = 100
    if request.method == 'GET':
        groups = int(request.GET.get('groups'))
        officers = int(request.GET.get('officers'))

    length = len(locations)

    locations = assignOfficers(locations, officers, groups)
    officers_assigned = []
    for loc in locations:
        officers_assigned.append(str(loc['officers']))

    if length > len(officers_assigned):
        for i in range(length - len(officers_assigned)):
            officers_assigned.append('0')

    locations_json = json.dumps(locations)


    context_dict = {'locations_json': locations_json, 'locations': locations, 'officers_numbers': json.dumps(officers_assigned), 'groups': groups, 'officers': officers}


    return render(request, 'deploy.html', context_dict)


def get_locations(request):
    if request.method == 'GET':
        data = json.loads(ad.get_most_important_events_json())

        locations = []
        for location in data:
            for l in location:
                locations.append((float(location[l]['lat']), float(location[l]['long']), 10,
                                  str(location[l]['most_common']), str(location[l]['affected'])))

        locations_json = json.dumps(locations)

        return HttpResponse(locations_json)


def assignOfficers(locations, officers, groupsOf):
    total = 0
    j = 0
    min = 1
    for location in locations:
        total += location['percentage']
    min = round(total / officers)
    while locations[-1]['percentage'] * officers / total < 3 * groupsOf:
        total -= locations[-1]['percentage']
        del locations[-1]
    for location in locations:
        officerNo = round(3 * groupsOf * (location['percentage'] / locations[-1]['percentage']))
        officers -= officerNo
        location['officers'] = int(officerNo);
    index = 0
    while officers > 0:
        for location in locations:
            location['officers'] += 1
            officers -= 1
    for location in locations:
        location['morning'] = int(round(location['officers'] / 3))
        location['afternoon'] = int(round(location['officers'] / 3))
        if location['officers'] % 3 == 1:
            location['afternoon'] = int(round(location['officers'] / 3) + 1)
        if location['officers'] % 3 == 2:
            location['afternoon'] = int(round(location['officers'] / 3) + 2)
        location['night'] = int(round(location['officers'] / 3))

    return locations
