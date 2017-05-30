# python imports

#django imports
from django.conf.urls import url

# locals import
from . import views
from .views import QuestionDetailView, ShowAllQuestion, QuestionDeleteView, EditQuestionView, AnswerView, AnswerDetailView, EditAnswerView, ShowAllAnswers


app_name = 'forum'

urlpatterns = [
	url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
	url(r'^$', views.HomepageView.as_view(), name='homepage'),
	url(r'^question/$', views.QuestionView.as_view(), name='question'),
	url(r'^show-all-own-question/$', views.ShowOwnAllQuestion.as_view(), name='show_all_own_question'),
	url(r'^question-detail/(?P<pk>\d+)/', QuestionDetailView.as_view(), name='question_detail'),
	url(r'^show-all-question/', ShowAllQuestion.as_view(), name='show_all_question'),
	url(r'^delete-question/(?P<pk>\d+)/', QuestionDeleteView.as_view(), name='question_delete'),
	url(r'^edit-question/(?P<pk>\d+)/', EditQuestionView.as_view(), name='edit_question'),
	url(r'^answer/(?P<pk>\d+)/', AnswerView.as_view(), name='answer'),
	url(r'^answer-detail/(?P<pk>\d+)/', AnswerDetailView.as_view(), name='answer_detail'),
	url(r'^edit-answer/(?P<pk>\d+)/', EditAnswerView.as_view(), name='edit_answer'),
	url(r'^show-all-answers/(?P<pk>\d+)/', ShowAllAnswers.as_view(), name='show_all_answers'),
]	
