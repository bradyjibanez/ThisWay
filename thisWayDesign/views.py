from django.shortcuts import render
from django.http import HttpResponse

from .models import Landmark #, Greeting
from .forms import landmarkForm
import requests

def getLandmarkURL(request):
	landmark = None
	landmarkURL = landmarkForm(request.POST or None)
	if landmarkURL.is_valid():
		landmarkURL = landmarkURL.cleaned_data['imageURL']
		landmark = Landmark.giveURL(landmarkURL)
		if landmark == "Nothing" or landmark == None:
			landmark = "We couldn't find a landmark from that URL. Hit reset and try again with another."
			landmark_dict = {
				'landmark': landmark
			}
		else:
			landmark_dict = {
				'landmark': landmark
			}
	return render(request, 'landmark.html', landmark_dict)

def index(request):
	return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
