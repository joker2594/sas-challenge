from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import geocoder
import analyse_data as ad
import json
from django.core import serializers
import ast


def index(request):
    context_dict = ""
    return render(request, 'index.html', context_dict)


def deploy(request):
    data = json.loads(ad.get_most_important_events_json())
    locations = []
    for location in data:
        locations.append(location[location.keys()[0]])

    groups = 0
    officers = 0
    if request.method == 'GET':
        groups = int(request.GET('groups'))
        officers = int(request.GET('officers'))

    assignOfficers(locations)
    addPostCodes(locations)

    locations_json = json.dumps(locations)

    context_dict = {'locations_json': locations_json, 'locations': locations}
    return render(request, 'deploy.html', context_dict)


def get_locations(request):
    if request.method == 'GET':
        data = json.loads(ad.get_most_important_events_json())

        locations = []
        for location in data:
            for l in location:
                locations.append((float(location[l]['lat']), float(location[l]['long']), 10))

        locations_json = json.dumps(locations)

        return HttpResponse(locations_json)


def addPostCodes(locations):
    for location in locations:
        lat = location['lat']
        long = location['long']
        postcode = geocoder.google([lat, long], method='reverse')
        #if postcode.postal == None:
            #print lat, long
        location['postcode'] = postcode.postal


def assignOfficers(locations, officers=100, groupsOf=2):
    total = 0
    min = 1
    for location in locations:
            total += location['percentage']
    min = round(total / officers)
    print (min)
    while min < groupsOf:
        del locations[-1]
        for location in locations:
            total += location['percentage']
            min = round(total / officers)
            #print (min)
    if min % 2 != 0:
        min = min + 1
    for location in locations:
        officerNo = round(min * (location['percentage'] / locations[-1]['percentage']))
        officers -= officerNo
        location['officers'] = officerNo
    index = 0
    while officers > 0 and officers - groupsOf >= 0:
        locations[index]['officers'] += groupsOf
        officers -= groupsOf
        index = (index + 1) % len(locations)


##data_json = ad.get_most_important_events_json()
##data = json.loads(ad.get_most_important_events_json())
##locations = []
##for location in data:
##    locations.append(location[location.keys()[0]])
##assignOfficers(locations)
##addPostCodes(locations)
