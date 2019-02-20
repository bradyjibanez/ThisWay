from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import Landmark, Directions
from .forms import submissionForm
import requests

def processSubmission(request):
	landmark = None
	submission = submissionForm(request.POST or None)
	if submission.is_valid():

		#Google Cloud Vision to find landmark
		landmarkURL = submission.cleaned_data['imageURL']
		landmark = Landmark.giveURL(landmarkURL)
		if landmark == "Nothing" or landmark == None or landmark == "UNKNOWN_LANDMARK":
			return render(request, 'landmark.html', {'landmark': "We couldn't find a landmark from that URL. Hit reset and try again with another."})


		#Google directions API to find directions 
		startPoint = submission.cleaned_data['start']
		directions = Directions.giveDirections(startPoint, landmark)

		#Google smtp request to send directions
		userAddy = [submission.cleaned_data['usermail']]
		#directions = '\n'.join(directions)
		send_mail('your thisWay! directions',
				'Your Directions to '+landmark+'!\n\n'+str(directions),
				'thiswayfollowup@gmail.com',
				userAddy,	
				fail_silently=False)

		return render(request, 'landmark.html', {'LANDMARKSEEN': "LANDMARK SEEN:", 'landmark': landmark, 'DIRECTION': "DIRECTIONS (sent to your given email):", 'directions': directions})
	return render(request, 'landmark.html', {'landmark': "Error in your inputted data. Please reset and try again."})

def index(request):
	return render(request, "index.html")