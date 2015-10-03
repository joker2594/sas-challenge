from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import geocoder
import analyse_data as ad
import json
import ast

def index(request):
    context_dict = ""
    return render(request, 'index.html', context_dict)

def deploy(request):
    data_json = ad.get_most_important_events_json()
    data = json.loads(ad.get_most_important_events_json())
    locations = []
    for location in data:
        locations.append(location[location.keys()[0]])
    assignOfficers(locations)
    addPostCodes(locations)
    context_dict = {'data_json': data_json, 'locations': locations}
    return render(request, 'deploy.html', context_dict)

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
