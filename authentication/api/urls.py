# python imports

# django imports
from django.conf.urls import url
from rest_framework.authtoken import views

# local imports

# inner app imports
from authentication.api import urls
from authentication.api.views import UserList, UserDetail, AllQuestionsList ,SelfQuestionsList, LoginView, QuestionDetail, AnswerList, QuestionCreate, QuestionUpdate, CreateAnswer,UpdateAnswer, SignUpView, LogoutView, ChangePasswordView

# third party imports



urlpatterns = [
    url(r'^users/$', UserList.as_view()),
	url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
	url(r'^all-questions-list/$', AllQuestionsList.as_view()),
	url(r'^self-questions-list/$', SelfQuestionsList.as_view()),
	url(r'^question/detail/(?P<pk>[0-9]+)/$', QuestionDetail.as_view()),
	url(r'^question/add/$', QuestionCreate.as_view()),
	url(r'^question/update/(?P<pk>[0-9]+)/$', QuestionUpdate.as_view()),
	url(r'^answers/(?P<pk>[0-9]+)/$', AnswerList.as_view()),
	url(r'^update-answer/(?P<pk>[0-9]+)/$', UpdateAnswer.as_view()),
	url(r'^create-answer/(?P<pk>[0-9]+)/$', CreateAnswer.as_view()),
	url(r'^user-sign-up/$', SignUpView.as_view()),
	url(r'^api-token-auth/', views.obtain_auth_token),
	url(r'^api/logout/', LogoutView.as_view()),
	url(r'^login/$', LoginView.as_view()),
	url(r'^change/user/password', ChangePasswordView.as_view()),



]