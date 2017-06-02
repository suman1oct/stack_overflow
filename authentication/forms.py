# python imports
import datetime

# django imports
from django import forms
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget


#local imports
from authentication.models import User
from .validation import validateEmail


class SignUpForm(forms.ModelForm):	
	"""
	User Sign-Up form
	"""

	password = forms.CharField(widget=forms.PasswordInput)
	email = forms.CharField(widget = forms.EmailInput(attrs = {'placeholder': 'email id'}), validators = [validateEmail])

	def clean_email(self):
		"""
		check whether email address already exist or not if exist raise email already register error
		"""
		email = self.cleaned_data.get('email')
		
		if email and User.objects.filter(email=email).exists():
			raise forms.ValidationError(u'Email address already register.')
		
		return email

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name','address','date_of_birth','image', ]
		now = datetime.datetime.now()
		current_year = now.year
		# modify the widget of User model
		widgets = {
            'address': forms.Textarea(attrs={'rows':6, 'cols':40}),'password':forms.PasswordInput(attrs={'placeholder': 'Password'}), 'date_of_birth':SelectDateWidget(years=range(current_year - 70, current_year),
            empty_label=('Year', 'Month', 'Day'))
        }	



class SignInForm(forms.Form):
	"""
	User SignIn form
	"""

	username = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'placeholder': 'Username'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}))
	
	def clean(self):
		"""
		if username and password not valid raise not a valid username or password validation
		"""

		username = self.cleaned_data.get('username')
		password= self.cleaned_data.get('password')
		user=authenticate(username=username, password=password)
		
		if not user or not user.is_active:
			raise forms.ValidationError("Not a Valid Username Or Password")
		
		return self.cleaned_data


class ChangePasswordForm(forms.Form):		
	"""
	Change Password Form
	"""

	old_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'old Password'}))
	new_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
	confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

	def __init__(self, *args, **kwargs):
		"""
		get request from ChangePasswordView
		"""
		
		self.request = kwargs.pop('request', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		"""
		if old password is invalid raise inavalid old password error and new password and confirm password are not same raise New password and Confirm password are not matched error
		"""

		old_password=self.cleaned_data.get('old_password')
		
		if not self.request.user.check_password(old_password):
			raise forms.ValidationError('invalid old password')
		
		new_password=self.cleaned_data.get('new_password')
		confirm_password=self.cleaned_data.get('confirm_password')
		
		if new_password and new_password!=confirm_password:
			raise forms.ValidationError('New password and Confirm password are not matched')
		
		return self.cleaned_data


# class EditUserProfileForm(forms.Form):	
# 	"""
# 	Edit User Profile Form
# 	"""
# 	first_name =forms.CharField(max_length=100, widget=forms.TextInput())
# 	last_name =forms.CharField(max_length=100, widget=forms.TextInput())
# 	email = forms.CharField(widget = forms.EmailInput())
# 	address=forms.CharField(max_length=100, widget=forms.Textarea)

# 	def __init__(self, *args, **kwargs):
# 		"""
# 		get request from EditUserProfileView
# 		"""

# 		self.request = kwargs.pop('request', None)
# 		super(EditUserProfileForm, self).__init__(*args, **kwargs)

	# def clean_email_id(self):
	# 	"""
	# 	check whether email address already exist or not if exist raise email already register error
	# 	"""
	# 	email = self.cleaned_data.get('email_id')
		
	# 	if email and User.objects.filter(email=email).exclude(email=self.request.user.email).exists():
	# 		raise forms.ValidationError(u'Email address already register.')
		
	# 	return email



class EditUserProfileForm(forms.ModelForm):		# for edit the existing campaign of specific user

	def __init__(self, *args, **kwargs):
		"""
		get request from ChangePasswordView
		"""
		
		self.request = kwargs.pop('request', None)
		super(EditUserProfileForm, self).__init__(*args, **kwargs)

	def clean_email(self):
		"""
		check whether email address already exist or not if exist raise email already register error
		"""
		email = self.cleaned_data.get('email')
		
		if email and User.objects.filter(email=email).exclude(email=self.request.user.email).exists():
			raise forms.ValidationError(u'Email address already register.')
		
		return email


	class Meta:
		model = User
		fields=['first_name','last_name','email','address','date_of_birth','image' ]
		now = datetime.datetime.now()
		current_year = now.year
		widgets = {
            'address': forms.Textarea(attrs={'rows':4, 'cols':40}),'date_of_birth':SelectDateWidget(years=range(current_year - 70, current_year),empty_label=('Year', 'Month', 'Day'))
        }


