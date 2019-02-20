from django import forms
from .models import Submission #Landmark, Directions, UserAddy, Submission

class submissionForm(forms.ModelForm):
	imageURL = forms.CharField(max_length=1000)
	start = forms.CharField(max_length=100)
	usermail = forms.CharField(max_length=100)
	class Meta:
		model = Submission
		fields = ('imageURL', 'start', 'usermail',)