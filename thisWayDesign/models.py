from django.db import models
from findLandmark import getLandmark

# Create your models here.
class Landmark(models.Model):
	image = models.CharField(max_length=1000)
	landmark, lat, lon = landmark(image)
	def __str__(self):
		return self.landmark

#class Greeting(models.Model):
#    when = models.DateTimeField("date created", auto_now_add=True)
