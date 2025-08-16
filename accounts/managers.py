from django.contrib.auth.models import UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user