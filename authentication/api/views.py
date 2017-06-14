# python imports

# django imports
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views import View
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout

# local imports
from .serializers import UserSerializer, QuestionSerializer, AnswerSerializer,SignInSerializer , AnswerSerializer2, ChangePasswordSerializer, QuestionSerializer2, SignUpSerializer

# inner app imports
from forum.models import Question, Answer
from .permission import IsOwnerOrReadOnly

# third party imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions	


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)


class AllQuestionsList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)



class QuestionDetail(APIView):
	"""
	retrive question
	"""
	authentication_classes = (SessionAuthentication, BasicAuthentication)
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
	authentication_classes = (SessionAuthentication, BasicAuthentication)
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
	# authentication_classes = (SessionAuthentication, BasicAuthentication)
	serializer_class = QuestionSerializer2
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

	def get_object(self):
		try:
			Question.objects.get(pk=self.kwargs['pk'])
		except Question.DoesNotExist:
			raise Http404()
		obj = Question.objects.get(pk=self.kwargs['pk'])
		self.check_object_permissions(self.request, obj)
		return obj


class AnswerList(generics.ListAPIView):
	"""
	list all question and answers
	"""
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	serializer_class = AnswerSerializer
	#queryset = Answer.objects.()

	def get_queryset(self):
		return Answer.objects.filter(question__pk = self.kwargs['pk'])



	
class SelfQuestionsList(APIView):
	"""
	list all self questions
	"""
	authentication_classes = (SessionAuthentication, BasicAuthentication)
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
	authentication_classes = (SessionAuthentication, BasicAuthentication)

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
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

	def get_object(self):
		try:
			Answer.objects.get(pk=self.kwargs['pk'])
		except Answer.DoesNotExist:
			raise Http404()
		obj = Answer.objects.get(pk= self.kwargs['pk'])
		self.check_object_permissions(self.request, obj)
		return obj


class SignUpView(generics.CreateAPIView):
	"""
	create question
	"""

	serializer_class = SignUpSerializer
	authentication_classes=[]
	permission_classes = []

	def create(self, request, format=None):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			s_user=serializer.save()
			s_user.set_password(request.data['password'])
			s_user.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	# def post(self, request, format=None):
	# 	serializer = self.get_serializer(data=request.data)
	# 	if serializer.is_valid():
	# 		s_user=serializer.save()
	# 		s_user.set_password(request.data['password'])
	# 		s_user.save()
	# 		return Response(serializer.data, status=status.HTTP_201_CREATED)
	# 	else:
	# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# class LoginView(APIView):
	
# 	serializer_class = SignInSerializer
# 	authentication_classes=[]
# 	permission_classes = []

# 	def post(self, request, *args, **kwargs):
# 		serializer = self.get_serializer(data=request.data)
# 		# if not valid raise exception
# 		serializer.is_valid(raise_exception=True)
# 		username = serializer.validated_data.get('username')
# 		password = serializer.validated_data.get('password')
# 		user = authenticate(username = username, password = password)
# 		if user and user.is_active:
# 			serialized_user = SignUpSerializer(user).data
# 			serialized_user.update({'token':user.get_auth_token()})
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
	serializer_class = SignInSerializer
	authentication_classes=[]
	permission_classes = []

	def post(self, request, format=None):
		data = request.data

		username = data.get('username', None)
		password = data.get('password', None)
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.UpdateAPIView):
	"""
	Change Password
	"""
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	serializer_class = ChangePasswordSerializer

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
			# set_password also hashes the password that the user will get

			new_password = serializer.data.get("new_password")
			confirm_password = serializer.data.get("confirm_password")
			if not new_password == confirm_password:
				return Response({"message": "new password  and confirm password not matched"}, status=status.HTTP_400_BAD_REQUEST)
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response("Success.", status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
