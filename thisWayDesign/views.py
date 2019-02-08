from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Landmark
from .forms import landmarkForm
import requests

def getLandmark(request):
	landmarkURL = landmarkForm(request.POST or None)
	if landmarkURL.is_valid():
		landmarkURL = landmarkURL.cleaned_data['imageURL']
		landmark = Landmark(landmarkURL)
		return render(request, 'thisWayDesign/index.html', landmark)


'''def index(request):
	return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})'''
