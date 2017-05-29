# Django Import
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **kwargs):
        """
        Create the Normal User
        """

        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create the Super User
        """

        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')

        # return self._create_user(username, email, password, **extra_fields)

        user = self.model(username=username, email=email, is_staff=True, is_superuser=True, is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
