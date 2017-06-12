# python imports

# django imports
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views import View
from django.http import Http404
from django.http import HttpResponse

# local imports
from .serializers import UserSerializer, QuestionSerializer, AnswerSerializer, AnswerSerializer2, QuestionSerializer2

# inner app imports
from forum.models import Question, Answer

# third party imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class AllQuestionsList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(APIView):
	"""
	retrive question
	"""
	
	serializer_class = QuestionSerializer
	
	def get_object(self, pk):
		try:
			return Question.objects.get(pk=pk)
		except Question.DoesNotExist:
			raise Http404

	def get(self, *args, **kwargs):
		ques = self.get_object(kwargs['pk'])
		serializer = QuestionSerializer(ques)		
		return Response(serializer.data)


class QuestionCreate(generics.CreateAPIView):
	"""
	create question
	"""

	serializer_class = QuestionSerializer2

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serialized = serializer.save(user=self.request.user)
		self.perform_create(serializer)

		return Response(serializer.data, status=status.HTTP_201_CREATED)



class QuestionUpdate(generics.UpdateAPIView):
	"""
	update question
	"""

	serializer_class = QuestionSerializer2

	# def put(self, request, pk):
	# 	ques = Question.objects.get(pk = pk)
	# 	serializer = QuesionSerializer2(ques, data=request.data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



	def get_object(self):
		return Question.objects.get(pk= self.kwargs['pk'])

	# def update(self, request, *args, **kwargs):
	# 	partial = kwargs.pop('partial', False)
	# 	instance = self.get_object()
	# 	serializer = self.get_serializer(instance, data=request.data, partial=partial)
	# 	ques = Question.objects.get(pk = kwargs['pk'])
	# 	if serializer.is_valid():
	# 		serialized = serializer.save(user=self.request.user, question=ques)
		
	# 	return Response(serializer.data)



class AnswerList(generics.ListAPIView):
	"""
	list all question and answers
	"""

	serializer_class = AnswerSerializer
	#queryset = Answer.objects.()

	def get_queryset(self):
		return Answer.objects.filter(question__pk = self.kwargs['pk'])



	
class SelfQuestionsList(APIView):
	"""
	list all self questions
	"""
	
	serializer_class = QuestionSerializer
	
	def get(self, request):
		ques=Question.objects.filter(user__pk=self.request.user.pk)
		serializer = QuestionSerializer(ques, many=True)
		return Response(serializer.data)

	
class CreateAnswer(mixins.CreateModelMixin, generics.GenericAPIView):
	"""
	create answer
	"""

	serializer_class = AnswerSerializer2

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		ques = Question.objects.get(pk = kwargs['pk'])
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serialized = serializer.save(user=self.request.user, question=ques)
		self.perform_create(serializer)

		return Response(serializer.data, status=status.HTTP_201_CREATED)




class UpdateAnswer(generics.UpdateAPIView):
	"""
	update answer
	"""

	serializer_class = AnswerSerializer2

	def get_object(self):
		return Answer.objects.get(pk= self.kwargs['pk'])

	# def update(self, request, *args, **kwargs):
	# 	partial = kwargs.pop('partial', False)
	# 	instance = self.get_object()
	# 	serializer = self.get_serializer(instance, data=request.data, partial=partial)
	# 	ques = Question.objects.get(pk = kwargs['pk'])
	# 	if serializer.is_valid():
	# 		serialized = serializer.save(user=self.request.user, question=ques)
		
	# 	return Response(serializer.data)