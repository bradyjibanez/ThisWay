from django.db import models
from .findLandmark import getLandmark

# Used to build landmark obj and return name, lat, lon
class Landmark(models.Model):
	image = models.CharField(max_length=1000)
	def giveURL(image):	
		landmark = getLandmark(image)
		return landmark
	def __str__(self):
		return self.landmark

#class Greeting(models.Model):
#    when = models.DateTimeField("date created", auto_now_add=True)
