# python imports

# django imports
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden,  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View, generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# local imports
#from .forms import EditQuestionForm
from .models import Question, Answer

# inner app imports


class DashboardView(LoginRequiredMixin, generic.TemplateView):
	
	"""
	Homepage View
	"""

	template_name = 'forum/DASHBOARD.html'


class HomepageView(generic.TemplateView):
	
	"""
	Homepage View
	"""

	template_name = 'forum/index.html'

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
	template_name = 'forum/CREATE_QUESTION.html'
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

	template_name = 'forum/SELF_QUESTION.html'

	def get_queryset(self):
		"""
		send object of UserProfile of authenticated user
		"""
		return Question.objects.filter(user=self.request.user)


class QuestionDetailView(generic.CreateView):
	"""
	Question Detail view this will display the detail of question their ans and form for your answer
	"""
	template_name = 'forum/ques_detail.html'
	model = Answer
	fields = ['ans_description',]

	def form_valid(self,form):
		ans_description=form.cleaned_data.get('ans_description')
		
		ans=Answer(ans_description = ans_description)
		form.save(commit=False)
		ans.user=self.request.user
		qu=Question.objects.get(pk=self.kwargs.get('pk'))
		ans.question=qu
		ans.save()
		return redirect('forum:question_detail', pk=qu.pk)

	def get_context_data(self, *args, **kwargs):
		context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
		context['answers'] = Answer.objects.filter(question__pk = self.kwargs['pk'])
		context['question'] = Question.objects.get(pk = self.kwargs['pk'])
		return context




class ShowAllQuestion(LoginRequiredMixin, generic.ListView):
	"""
	display all users question
	"""

	template_name = 'forum/ALL_QUESTION.html'
	model = Question

	def get_queryset(self):
		"""
		send all questions
		"""
		ques = Question.objects.all().order_by('updated_date')
		return ques


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
	template_name = 'forum/EDIT_QUESTION.html'
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

	def form_valid(self, form):
		"""
		Edit the update date of question
		"""
		instance = form.save(commit=False)
		instance.updated_date = timezone.now()
		super(EditQuestionView, self).form_valid(form)
		return redirect(self.success_url)



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
		return redirect('forum:question_detail', pk=qu.pk)

	def get_context_data(self, *args, **kwargs):
		context = super(AnswerView, self).get_context_data(*args, **kwargs)
		context['answers'] = Answer.objects.filter(question__pk = self.kwargs['pk'])
		context['question'] = Question.objects.filter(pk = self.kwargs['pk'])
		return context
		return redirect('forum:answer', pk=self.kwargs['pk'])



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

	def form_valid(self, form):
		"""
		Edit the Updated date of answer
		"""
		instance = form.save(commit=False)
		instance.updated_date = timezone.now()
		super(EditAnswerView, self).form_valid(form)
		#return redirect(self.success_url)
		q=Question.objects.get(pk=instance.question.pk)
		return redirect('forum:question_detail', pk=q.pk)


class ShowAllAnswers(LoginRequiredMixin, generic.ListView):
	"""
	display all answers for a question
	"""

	template_name = 'forum/show_all_answers.html'
	model = Answer

	def get_queryset(self):
		"""
		send object of all answer of a particular question
		"""
		ques=Question.objects.get(pk = self.kwargs.get('pk'))
		ans=ques.answer_set.all()
		return ans


class ShowSelfAnswers(LoginRequiredMixin, generic.ListView):
	"""
	display own answer with question
	"""
	model = Answer
	template_name= 'forum/SELF_ANSWER.html'
 
	def get_queryset(self):
		"""
		send all self answer with question
		"""
		answers = Answer.objects.filter(user = self.request.user)
		return answers