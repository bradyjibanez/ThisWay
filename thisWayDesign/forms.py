from django import forms
from .models import Landmark

class landmarkForm(forms.ModelForm):
	imageURL = forms.CharField(max_length=1000)
	class Meta:
		model = Landmark
		fields = ('imageURL',)