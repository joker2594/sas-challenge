from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import geocoder
import analyse_data as ad
import json

def index(request):
    context_dict = ""
    return render(request, 'index.html', context_dict)

def deploy(request):
    data_json = ad.get_most_important_events_json()
    data = json.loads(ad.get_most_important_events_json())

    context_dict = {'data_json': data_json}
    return render(request, 'deploy.html', context_dict)
