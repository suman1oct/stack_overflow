# python imports

# django imports
from django import forms
 
# local imports
from .models import Question


class QuestionForm(forms.ModelForm):	
	"""
	Asking Question form
	"""
	
	class Meta:
		model = Question
		fields = ['title', 'text']
		

	



