from django.db import models
from .findLandmark import getLandmark
from .getDirections import findDirections

# Used to build landmark obj from Google Computer Vision API and return name, lat, lon
class Landmark(models.Model):
	image = models.CharField(max_length=1000)
	def giveURL(image):	
		landmark = getLandmark(image)
		return landmark

#Used to build directions object from Google Maps Direction API
class Directions(models.Model):
	startPoint = models.CharField(max_length=100)
	def giveDirections(startPoint, endPoint):
		directions = findDirections(startPoint, endPoint)
		return directions

#Used for overall form submission referencing and passing to Views
class Submission (models.Model):
	image = models.CharField(max_length=1000)
	startPoint = models.CharField(max_length=100)
	userAddy = models.CharField(max_length=100)