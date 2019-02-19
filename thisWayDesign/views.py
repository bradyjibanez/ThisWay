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
		if landmark == "Nothing" or landmark == None or landmark == "UNKNOWN_LANDMARK":
			landmark = "We couldn't find a landmark from that URL. Hit reset and try again with another."
			landmark_dict = {
				'landmark': landmark
			}
			return render(request, 'landmark.html', landmark_dict)
		else:
			landmark_dict = {
				'landmark': landmark
			}
			return render(request, 'landmark.html', landmark_dict)
	return render(request, 'landmark.html', {'landmark': "Error in the computer vision. Please reset and try again."})

def index(request):
	return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
