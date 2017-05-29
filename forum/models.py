# python imports

# django imports
from django.db import models
from django.utils import timezone

# local imports
from authentication.models import User

# third party imports
from ckeditor_uploader.fields import RichTextUploadingField
#from ckeditor.fields import RichTextField

class Question(models.Model):
	ques_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	ques_title = models.CharField(verbose_name='Question Title',max_length=500)
	ques_description = RichTextUploadingField()
	#ques_description = models.CharField(verbose_name='Question',max_length=5000)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.ques_title


class Answer(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	ans_description = RichTextUploadingField()
	created_date = models.DateTimeField(default=timezone.now)
