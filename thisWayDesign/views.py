from django.shortcuts import render
from django.http import HttpResponse

from .models import Landmark, Directions #, Greeting
from .forms import landmarkForm, startForm
import requests

def getLandmarkURL(request):
	landmark = None
	landmarkURL = landmarkForm(request.POST or None)
	if landmarkURL.is_valid():
		landmarkURL = landmarkURL.cleaned_data['imageURL']
		landmark = Landmark.giveURL(landmarkURL)
		directions = getDirections(request, landmark)
		if landmark == "Nothing" or landmark == None or landmark == "UNKNOWN_LANDMARK":
			return render(request, 'landmark.html', {'landmark': "We couldn't find a landmark from that URL. Hit reset and try again with another."})
		else:
			return render(request, 'landmark.html', {'landmark': "LANDMARK SEEN: "+landmark, 'directions': directions})
	return render(request, 'landmark.html', {'landmark': "Error in the computer vision. Please reset and try again."})

def getDirections(request, endPoint):
	startPoint = startForm(request.POST or None)
	if startPoint.is_valid():
		startPoint = startPoint.cleaned_data['start']
		directions = Directions.giveDirections(startPoint, endPoint)
		return directions
	else:
		return "We couldn't gather anything from your entered start point."









def index(request):
	return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
