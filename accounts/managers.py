from django.contrib.auth.models import UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    def create_user(self, username, email, role, password=None):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have an email address')
        if not role:
            raise ValueError('User must have a role')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, role="Administrator", password=None):
        user = self.create_user(
            username=username,
            email=email,
            role=role,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
