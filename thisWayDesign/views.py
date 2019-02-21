from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from google.cloud import storage
from google.oauth2 import service_account
from .models import Landmark, Directions
from .forms import submissionForm
import requests, json, os

landmarksref = []

def processSubmission(request):
	landmark = None
	submission = submissionForm(request.POST or None)
	if submission.is_valid():

		#Google Cloud Vision to find landmark
		landmarkURL = submission.cleaned_data['imageURL']
		landmark = Landmark.giveURL(landmarkURL)

		#Google Cloud Storage to create reference for past searched landmarks by other users
		#updateStorage(landmark)
		global landmarksref
		landmarksref.append(landmark)

		#Return error message if vision can't identify landmark
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

def updateStorage(landmark):

	with open("landmarksRequested.txt", "a+") as text_file:
		text_file.write(landmark+"\r\n")

	credentials_raw = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
	service_account_info = json.loads(credentials_raw)
	storageCredentials = service_account.Credentials.from_service_account_info(service_account_info)

	client = storage.Client(credentials=storageCredentials)
	bucket = client.get_bucket('requested-landmarks')
	blob = bucket.blob('landmarksRequested.txt')
	blob.upload_from_filename('landmarksRequests.txt')

def index(request):
	global landmarksref
	return render(request, "index.html", {'LPS': "LANDMARKS PREVIOUSLY SEARCHED:", 'landmarksref': landmarksref})