from django.db import models
from .findLandmark import getLandmark
from .getDirections import findDirections

# Used to build landmark obj and return name, lat, lon
class Landmark(models.Model):
	image = models.CharField(max_length=1000)
	def giveURL(image):	
		landmark = getLandmark(image)
		return landmark

class Directions(models.Model):
	startPoint = models.CharField(max_length=100)
	def giveDirections(startPoint, endPoint):
		directions = findDirections(startPoint, endPoint)
		return directions

class Submission (models.Model):
	image = models.CharField(max_length=1000)
	startPoint = models.CharField(max_length=100)
	userAddy = models.CharField(max_length=100)