# python imports

# django imports
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.http import HttpResponse, HttpResponseForbidden,  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# local imports
from .forms import SignUpForm, SignInForm, ChangePasswordForm, EditUserProfileForm
from authentication.models import User
from .mixins import ValidUserProfileMixin


class SignUpView(generic.CreateView):
	"""
	User Sign-Up View
	"""

	model=User
	form_class = SignUpForm
	#fields=['first_name','last_name','email','address']
	success_url=reverse_lazy('forum:dashboard')
	template_name = 'authentication/sign_up.html'
	success_message = 'User Registered Successfully'

	def get(self, *args, **kwargs):
		"""
		check if user is already loggedin then redirect to dashboard
		"""

		if self.request.user.is_authenticated():
			return redirect('forum:dashboard')
		return super(SignUpView, self).get(*args, **kwargs)

	def form_valid(self,form):
		username=form.cleaned_data.get('username')
		first_name =form.cleaned_data.get('first_name')
		last_name=form.cleaned_data.get('last_name')
		password=form.cleaned_data.get('password')
		email=form.cleaned_data.get('email')
		address=form.cleaned_data.get('address')
		date_of_birth=form.cleaned_data.get('date_of_birth')

		user=User(username=username, first_name=first_name, last_name=last_name, email=email, address=address, date_of_birth=date_of_birth)
		
		if User.objects.filter(username=user.username).exists():
			#check whether user is not already exist
			messages.error(self.request,'Username already exist')
			return redirect('forum:sign-up')

		user.set_password(password)
		user.save()
		messages.success(self.request, 'User Register Successfully')
		return redirect(self.success_url)


class SignInView(generic.FormView):
	"""
	user sign-In view
	"""

	template_name='authentication/sign_in.html'
	form_class=SignInForm
	success_url=reverse_lazy('forum:dashboard')

	def get(self, *args, **kwargs):
		"""
		check if user is already loggedin then redirect to dashboard
		"""

		if self.request.user.is_authenticated():
			return redirect('forum:dashboard')
		return super(SignInView, self).get(*args, **kwargs)

	def form_valid(self,form):
		"""
		check if username and password is valid then login the user
		"""
		username =form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username,password=password)
		
		# if user is authenticate then login the user		
		if user.is_active:
			login(self.request, user)
			return redirect(self.success_url)


class LogoutView(LoginRequiredMixin, generic.View):
	"""
	User logout View
	"""

	def get(self,request):
		"""
		logout the request
		"""
		logout(request)
		
		return redirect('authentication:sign_in')


class EditProfileView(SuccessMessageMixin,ValidUserProfileMixin, LoginRequiredMixin, UpdateView):
	model=User
	form_class = EditUserProfileForm
	success_url=reverse_lazy('authentication:show_profile')
	template_name = 'authentication/edit_profile.html'
	success_message = 'Profile Edited Successfully Successfully'

	# def get(self, *args, **kwargs):
	# 	u = User.objects.get(pk=kwargs['pk'])
	# 	if u.pk != self.request.user.pk:
	# 		return HttpResponseForbidden('Access Denied')
	# 	return super(EditProfileView, self).get(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(EditProfileView, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs


class UserProfileView(LoginRequiredMixin, generic.ListView):
	template_name ='authentication/show_profile.html'

	def get_queryset(self):
		"""
		send object of UserProfile of authenticated user
		"""
		return User.objects.filter(pk=self.request.user.pk)


class ChangePasswordView(LoginRequiredMixin, generic.FormView):
	"""
	Change password view
	"""
	form_class = ChangePasswordForm
	template_name='authentication/change_password.html'
	success_url = reverse_lazy('forum:dashboard')
	success_message = 'password changed successfully'
	
	def form_valid(self,form):
		"""
		check if old password if valid then change the password
		"""
		
		old_password=form.cleaned_data.get('old_password')
		new_password=form.cleaned_data.get('new_password')
		
		if self.request.user.check_password(old_password):
			self.request.user.set_password(new_password)
			self.request.user.save()

		return super(ChangePasswordView, self).form_valid(form)

	def get_form_kwargs(self):
		"""
		pass request to EditUserProfileForm
		"""
		kwargs = super(ChangePasswordView, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs


class DeleteUserAccountView(LoginRequiredMixin, ValidUserProfileMixin, SuccessMessageMixin,generic. DeleteView):
	"""
	Delete User Account View
	"""

	model = User
	template_name = 'authentication/delete_account.html'
	success_url = reverse_lazy('authentication:sign_up')
	success_message = 'User Account Deleted Successfully'

	# def get(self, *args, **kwargs):
	# 	u = User.objects.get(pk=kwargs['pk'])
	# 	if u.pk != self.request.user.pk:
	# 		return HttpResponseForbidden('Access Denied')
	# 	return super(DeleteUserAccountView, self).get(*args, **kwargs)


class SettingView(LoginRequiredMixin, generic.TemplateView):
	
	"""
	Setting View
	"""

	template_name = 'authentication/setting.html'

	