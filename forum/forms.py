# python imports

# django imports
from django import forms
 
# local imports
from .models import Question

# third party imports
from ckeditor_uploader.fields import RichTextUploadingField



# class QuestionForm(forms.ModelForm):	
# 	"""
# 	Asking Question form
# 	"""
	
# 	class Meta:
# 		model = Question
# 		fields = ['title', 'text']
		

# class EditQuestionForm(forms.ModelForm):	
# 	"""
# 	Asking Question form
# 	"""
	
# 	ques_description = RichTextUploadingField()

# 	class Meta:
# 		model = Question
# 		fields = ['ques_title',]
			



