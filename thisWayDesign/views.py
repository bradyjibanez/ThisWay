from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from google.cloud import storage
from google.oauth2 import service_account
from .models import Landmark, Directions
from .forms import submissionForm
import requests, json, os

landmarksref = []

#Used to process form data recieved from user
def processSubmission(request):
	landmark = None
	submission = submissionForm(request.POST or None)
	if submission.is_valid():

		#Google Cloud Vision to find landmark
		landmarkURL = submission.cleaned_data['imageURL']
		landmark = Landmark.giveURL(landmarkURL)

		#Google Cloud Storage to create reference for past searched landmarks by other users
		global landmarksref
		landmarksref.append(landmark)

		#Return error message if vision can't identify landmark
		if landmark == None or landmark == "UNKNOWN_LANDMARK":
			return render(request, 'landmark.html', {'landmark': "We couldn't find a landmark from that URL. Hit reset and try again with another."})

		#Google directions API to find directions 
		startPoint = submission.cleaned_data['start']
		directions = Directions.giveDirections(startPoint, landmark)

		#Google smtp request to send directions
		userAddy = [submission.cleaned_data['usermail']]

		#Return error message for invalid URL
		if (landmark == "Not a valid landmark image URL"):
			return render(request, 'landmark.html', {'landmark': landmark})
		#Return error message for invalid start point
		elif (directions == "Sorry, your start point wasn't recognized."):
			return render(request, 'landmark.html', {'landmark': directions})
		#Return values found and send directions to email if all good
		else:		
			send_mail('your thisWay! directions',
				'Your Directions to '+landmark+'!\n\n'+str(directions),
				'thiswayfollowup@gmail.com',
				userAddy,	
				fail_silently=False)
			return render(request, 'landmark.html', {'LANDMARKSEEN': "LANDMARK SEEN:", 'landmark': landmark, 'DIRECTION': "DIRECTIONS (sent to your given email):", 'directions': directions})

#Function allowing for Google Cloud Storage maintenance of recently searched landmarks
def updateStorage(landmark):

	#Open local file to hold all referenced landmarks
	with open("landmarksRequested.txt", "a+") as text_file:
		text_file.write(landmark+"\r\n")

	#Authenticate and access Google Cloud Storage 	
	credentials_raw = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
	service_account_info = json.loads(credentials_raw)
	storageCredentials = service_account.Credentials.from_service_account_info(service_account_info)

	#Reference Google Cloud Storage and update bucket
	client = storage.Client(credentials=storageCredentials)
	bucket = client.get_bucket('requested-landmarks')
	blob = bucket.blob('landmarksRequested.txt')
	blob.upload_from_filename('landmarksRequests.txt')

#Returns refreshed home page with previously rerenced landmarks by all users
def index(request):
	global landmarksref
	return render(request, "index.html", {'LPS': "LANDMARKS PREVIOUSLY SEARCHED:", 'landmarksref': landmarksref})
