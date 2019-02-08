from django import forms
from .models import Landmark

class landmarkForm(forms.ModelForm):
	class Meta:
		model = Landmark
		fields = [
			'imageURL'
		]