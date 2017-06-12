# python imports

# django imports
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

#local imports

# inner app imports
from forum.models import Question, Answer

# third party imports
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('user_id', 'username','image','first_name','last_name', 'email', 'date_of_birth', 'password')


class QuestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields=('ques_id', 'user', 'ques_title', 'ques_description',)


class QuestionSerializer2(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields=('ques_id', 'ques_title', 'ques_description',)


class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields=('user', 'question', 'ans_description',)


class AnswerSerializer2(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ('ans_description',)