from django import forms
from .models import Landmark, Directions

class landmarkForm(forms.ModelForm):
	imageURL = forms.CharField(max_length=1000)
	class Meta:
		model = Landmark
		fields = ('imageURL',)

class startForm(forms.ModelForm):
	start = forms.CharField(max_length=100)
	class Meta:
		model = Directions
		fields = ('start',)