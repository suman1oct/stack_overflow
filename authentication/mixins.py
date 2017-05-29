# django imports
from .models import User
from django.http import HttpResponse, HttpResponseForbidden

class ValidUserProfileMixin(object):
	"""
	View Mixin which validate and authenticate the user acccess
	"""

	def dispatch(self, request, *args, **kwargs):
		if User.objects.filter(pk=kwargs['pk']).exists():
			u = User.objects.get(pk=kwargs['pk'])
			if u.pk != self.request.user.pk:
				return HttpResponseForbidden('Access Denied')
		else:
			return HttpResponseForbidden('Access Denied')

		return super(ValidUserProfileMixin, self).dispatch(request, *args, **kwargs)



		# u = User.objects.get(pk=kwargs['pk'])
		# if u.pk != self.request.user.pk:
		# 	return HttpResponseForbidden('Access Denied')
		# return super(DeleteUserAccountView, self).get(*args, **kwargs)