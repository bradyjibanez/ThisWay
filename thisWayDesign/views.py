from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from google.cloud import storage
from google.oauth2 import service_account
from .models import Landmark, Directions
from .forms import submissionForm
import requests, json, os

def processSubmission(request):
	landmark = None
	submission = submissionForm(request.POST or None)
	if submission.is_valid():

		#Google Cloud Vision to find landmark
		landmarkURL = submission.cleaned_data['imageURL']
		landmark = Landmark.giveURL(landmarkURL)

		#Google Cloud Storage to create reference for past searched landmarks by other users
		updateStorage(landmark)

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

	'''	
	service_account_info = {
	  "type": "service_account",
	  "project_id": "landmarkdetection",
	  "private_key_id": "099fca800613aa77adfac4ccf23e3b96c3e6f0b5",
	  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCzTMIK9DRiRZnb\ndTxlhfY2XghT80Sjz0rwAurRKEOznrVuP/Hsl89TH9FwHPYw75NU/inh4XjTkL9R\nAnbyi8WHKNDVj+KIzyOWlksajRHWppQnR5SFKV9/fx6X0kENN5AySbUFEN+QrjG6\nh+XqH/mdMzRfUI3f1zDVkpqeqrWd5tcRscpeA5G3foSNw0+0/h+GiuYdjFc/zr1c\nRqZYgIS24j7IldFn5c9A/GV0faRWjc5z5bp+8CkfCY6KzewfyhboQ8eCEi36jpvq\nEszarU7xpsBbXtr+GK09uN/yZlK1FItW+eJoyV56gxOwPvzoQhoGYTanft3oIdvi\nN3InsgW5AgMBAAECggEAAkVNZCoWQRrazLyMTXYP6YbROxNf3EDfeYeif+tvLQ/6\nAf4z7nKKqqW1B1VLa9COWI7fHPOhLhYGk6xelc7QK2Y6zh8ESAYXZwWfSFZRIm2g\nrOG+x10pQSaxkxT4LQrxcG8HWtdED48HMxdAeJrJK14Ljfv3fErbZjOZloRdQ7Vr\nBUgKWnKmkpkr3GKugCd6cUoUNU4ao+moBfHRZmm+oXC9EDi2uqmBXQCTSGrAEiy4\n/DZmSlOCqL+7H3kVqXnJz2DsGqdPxtjUV4ZZZPDHSLQQoDmELeS1ZKVsvFb799bY\n84U/Ur7aBsfh/fCHXT6AI1wKwnLtNOFJKTNYanQEAQKBgQDqy5kHpytdXYLsM5wC\ny3hys1ptihKiuZCtme2y0b4ieBSqrhIV2VU0q1/Mqbv/+Yu35hWrdCjmj2iHVcOp\nYv6fVh9Z6GQ3Oed2OjaBuPxRpkYeW6tUAphkdvsgjowMQgowC/+y3/eZZyGSbLcO\n+iX9RJtFBihW5wFTYZuenjX8AQKBgQDDfh7SXwaj9pFVXrp70Xb+jPq/f4BPNou4\nXL+y5cC8BYGsaqVHnE5nChxmyHGjdgzLrv00siFS1uP+ZG0igNzOSOYOkPbtDzIC\nH6IcgDPdN3xQG1Fifj4pgOACiZXT38i09/TiwGOu0O3PjWKRywLn9pDLeBIcO8he\nAgZn+FLpuQKBgBvkDYycLgmMNyYpx0mJtAgkCATlFuufkXEdzN+mDKj5jLLttJZF\n19pG1T1xmDSDBzbULRTN2qHwvSD+bhyr9sUkrNq4QVdSGI2xwpHMUKS+VKv8hbCY\nElQ00gX/COHX4m/srPYpprbhSlqjcWdlDag1QyCC573S+RRXju3bq1wBAoGAdwNf\nDD+hsUw4qjpjWWHqCYoWVWLv4EmawgBlDCpnLZBEo4zBVllIOd6j78bzt8n0fEPq\nDpyrQN1mK8dD0Y+V3VfwBsomKafoj/ZmIOfDq1dOLQ6Ue1vTyDyXI7RTLIu+ir2x\nriHmDdVQEd1HNu7atBEdkWFl1R5oGyMsdztsbrECgYBVizlHc2EGrUncsklJm87m\nD9HDfVlfTLgPUiNxnutdE0yv2AXca3JVOwhbvyPmpmK1X9KGU8w7Tcp//Yt6lZDl\njWavxHj348nf45L9FGKGi8uZCQOrjNkl1SYIuDhz2DTiMAQtjc6U4VHtxwFbxsqv\nMNgL3tZxRYZu80wWrDtsfw==\n-----END PRIVATE KEY-----\n",
	  "client_email": "storage-service-account@landmarkdetection.iam.gserviceaccount.com",
	  "client_id": "105550972891814099970",
	  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
	  "token_uri": "https://oauth2.googleapis.com/token",
	  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/storage-service-account%40landmarkdetection.iam.gserviceaccount.com"
	}'''

	credentials_raw = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
	service_account_info = json.loads(credentials_raw)
	storageCredentials = service_account.Credentials.from_service_account_info(service_account_info)

	client = storage.Client(credentials=storageCredentials)
	bucket = client.get_bucket('requested-landmarks')
	blob = bucket.blob('landmarksRequested.txt')
	blob.upload_from_filename('landmarksRequests.txt')

	#blob.download_to_filename('landmarksRequested.txt')

def index(request):
	return render(request, "index.html")