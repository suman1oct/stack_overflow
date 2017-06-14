# python imports

# django imports
from django.contrib.auth.models import Group
from django.db import models
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
		fields = ('user_id', 'username','image','first_name','last_name', 'email', 'date_of_birth',)

		extra_kwargs = {"password": {"write_only": True},}	

	# def create(self, validated_data):
	# 	user = super().create(validated_data)
	# 	user.set_password(validated_data['password'])
	# 	user.save()
	# 	return user

	# def create(self, validated_data, format=None):
	# 	user = super().create(validated_data)
	# 	user.set_password(validated_data['password'])
	# 	user.save()
	# 	return user

class QuestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields=('ques_id', 'user', 'ques_title', 'ques_description',)


class QuestionSerializer2(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields=('ques_title', 'ques_description',)


class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields=('user', 'question', 'ans_description',)


class AnswerSerializer2(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ('ans_description',)

class SignUpSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = User
		fields = ('username', 'image','first_name', 'last_name', 'email', 'date_of_birth', 'address', 'password', )


class SignInSerializer(models.Model):
	
	username = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
