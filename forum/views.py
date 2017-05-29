# python imports

# django imports
from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# local imports
from .forms import EditQuestionForm
from .models import Question, Answer


from django.http import HttpResponse, HttpResponseForbidden,  HttpResponseRedirect

# inner app imports


class DashboardView(LoginRequiredMixin, generic.TemplateView):
	
	"""
	Homepage View
	"""

	template_name = 'forum/dashboard.html'


class HomepageView(generic.TemplateView):
	
	"""
	Homepage View
	"""

	template_name = 'forum/homepage.html'

	def get(self, *args, **kwargs):
		"""
		check if user is already loggedin then redirect to dashboard
		"""

		if self.request.user.is_authenticated():
			return redirect('forum:dashboard')
		return super(HomepageView, self).get(*args, **kwargs)


class QuestionView(LoginRequiredMixin, generic.CreateView):
	"""
	Create  question View
	"""
	model=Question
	template_name = 'forum/question.html'
	#form_class = QuestionForm
	fields = ['ques_title', 'ques_description']


	def form_valid(self,form):
		ques_title=form.cleaned_data.get('ques_title')
		ques_description =form.cleaned_data.get('ques_description')
		
		ques=Question(ques_title = ques_title, ques_description = ques_description)
		form.save(commit=False)
		ques.user=self.request.user
		ques.save()
		return redirect('forum:show_all_own_question')


class ShowOwnAllQuestion(LoginRequiredMixin, generic.ListView):
	"""
	display users own all question
	"""

	template_name = 'forum/show_all_own_question.html'

	def get_queryset(self):
		"""
		send object of UserProfile of authenticated user
		"""
		return Question.objects.filter(user=self.request.user)



class QuestionDetailView(generic.DetailView):
	"""
	Question Detail view this will display the detail of question
	"""
	template_name = 'forum/question_detail.html'
	model = Question


class ShowAllQuestion(LoginRequiredMixin, generic.ListView):
	"""
	display all users question
	"""

	template_name = 'forum/show_all_question.html'
	model = Question


class QuestionDeleteView(LoginRequiredMixin, generic.DeleteView):
	"""
	Delete  question view
	"""

	template_name = 'forum/question_delete.html'
	model = Question
	success_url = reverse_lazy('forum:show_all_own_question')
	success_message = 'Question Deleted Successfully'


class EditQuestionView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	"""
	Edit Question View
	"""

	model=Question
	#form_class = EditQuestionForm
	success_url=reverse_lazy('forum:show_all_own_question')
	template_name = 'forum/edit_question.html'
	success_message = 'Question Edited Successfully'
	fields=['ques_title','ques_description' ,]

	def get(self, *args, **kwargs):
		"""
		user can't edit the other users question
		"""

		if Question.objects.filter(pk=kwargs['pk']).exists():
			qu = Question.objects.get(pk=kwargs['pk'])
			if qu.user != self.request.user:
				return HttpResponseForbidden('Access Denied')
		else:
			return HttpResponseForbidden('Access Denied')

		return super(EditQuestionView, self).get(*args, **kwargs)


class AnswerView(LoginRequiredMixin, generic.CreateView):
	"""
	Create  question View
	"""
	model = Answer
	template_name = 'forum/answer.html'
	#form_class = QuestionForm
	fields = ['ans_description',]

	def form_valid(self,form):
		ans_description=form.cleaned_data.get('ans_description')
		
		ans=Answer(ans_description = ans_description)
		form.save(commit=False)
		ans.user=self.request.user
		qu=Question.objects.get(pk=self.kwargs.get('pk'))
		ans.question=qu
		ans.save()
		return redirect('forum:show_all_question')


class AnswerDetailView(generic.DetailView):
	"""
	Question Detail view this will display the detail of question
	"""
	template_name = 'forum/answer_detail.html'
	model = Answer


class EditAnswerView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	"""
	Edit Question View
	"""

	model=Answer
	success_url=reverse_lazy('forum:show_all_question' )
	template_name = 'forum/edit_answer.html'
	success_message = 'Answer Edited Successfully'
	fields=['ans_description' ,]

	def get(self, *args, **kwargs):
		"""
		user can't edit the other users answer
		"""

		if Answer.objects.filter(pk=kwargs['pk']).exists():
			ans = Answer.objects.get(pk=kwargs['pk'])
			if ans.user != self.request.user:
				return HttpResponseForbidden('Access Denied')
		else:
			return HttpResponseForbidden('Access Denied')

		return super(EditAnswerView, self).get(*args, **kwargs)


