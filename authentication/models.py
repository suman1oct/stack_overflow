# python imports
import uuid
import os

# django imports
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.contrib.auth.models import UserManager

# local imports
from .manager import UserManager

# third party imports

from rest_framework.authtoken.models import Token

def get_ProfileImage_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_images/', filename)


class User(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(verbose_name='UserName', max_length=200, unique=True)
	image = models.ImageField(verbose_name='profile image', upload_to=get_ProfileImage_path, blank=True, null=True)
	first_name = models.CharField(verbose_name='First Name', max_length=200)
	last_name = models.CharField(verbose_name='Last Name', max_length=200, blank=True, null=True)
	email = models.EmailField(max_length=200, blank=False, null=False)
	date_of_birth = models.DateField(null=True, blank=True)
	address = models.CharField(verbose_name='Address', max_length=1000)
	password = models.CharField(verbose_name='password',max_length=100)
	is_active = models.BooleanField(verbose_name='active',default=True)
	is_admin = models.BooleanField(verbose_name='admin status', default=False)
	is_staff = models.BooleanField(verbose_name='staff status',default=False)

	objects = UserManager()

	REQUIRED_FIELDS = ['email']
	USERNAME_FIELD = 'username'

	class Meta:
		verbose_name_plural = 'Users'

	def __str__(self):
		return self.username

	def get_full_name(self):
		"""
		Returns the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		#Returns the short name for the user
		return self.first_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

  