from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import geocoder

def index(request):
    context_dict = ""
    return render(request, 'index.html', context_dict)

def deploy(request):
    areas = [
        {'postcode':'G3 6JX', 'morning': 4, 'afternoon': 2, 'night': 4, 'percentage':'63%', 'crimes': 70, 'people':5645},
        {'postcode':'G1 8QF', 'morning': 8, 'afternoon': 4, 'night': 8, 'percentage':'54%', 'crimes': 13, 'people':544},
        {'postcode':'G7 9JK', 'morning': 8, 'afternoon': 6, 'night': 10, 'percentage':'57%', 'crimes': 89, 'people':1454},
        {'postcode':'G4 9JK', 'morning': 8, 'afternoon': 8, 'night': 4, 'percentage':'78%', 'crimes': 14, 'people':21334},
        {'postcode':'G7 9JK', 'morning': 10, 'afternoon': 10, 'night': 12, 'percentage':'80%', 'crimes': 16, 'people':15544534},
        {'postcode':'G9 9JK', 'morning': 6, 'afternoon': 6, 'night': 4, 'percentage':'33%', 'crimes': 40, 'people':454},
        {'postcode':'G2 9JK', 'morning': 8, 'afternoon': 8, 'night': 10, 'percentage':'24%', 'crimes': 7, 'people':78},
        {'postcode':'G4 9JK', 'morning': 4, 'afternoon': 6, 'night': 4, 'percentage':'78%', 'crimes': 46, 'people':6546},
        {'postcode':'G5 9JK', 'morning': 2, 'afternoon': 6, 'night': 6, 'percentage':'13%', 'crimes': 3, 'people':4},
    ]
    coords = []
    for area in areas:
        g = geocoder.google(area['postcode'])
        coords.append(g.latlng)
    context_dict = {'areas': areas, 'coords': coords}
    return render(request, 'deploy.html', context_dict)
