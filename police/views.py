from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    context_dict = ""
    return render(request, 'index.html', context_dict)
