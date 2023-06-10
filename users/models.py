import uuid
from enum import IntEnum
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserStatus(IntEnum):
    UNVERIFIED = 1
    VERIFIED = 2
    UNSUBSCRIBED = 3
    BLOCKLISTED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', UserStatus.VERIFIED)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    status = models.IntegerField(choices=UserStatus.choices(), default=UserStatus.UNVERIFIED)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserLoginEmailType(IntEnum):
    LOGIN = 1
    VERIFICATION = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

def _get_expiration_time():
    return datetime.datetime.now() + datetime.timedelta(minutes=15)

class UserLoginEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fulfilled = models.BooleanField(default=False)
    expires_at = models.DateField(default=_get_expiration_time)
    email_type = models.IntegerField(choices=UserLoginEmailType.choices(), default=UserLoginEmailType.LOGIN)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='user_active_login_email', condition=models.Q(fulfilled=False))
        ]

    def is_expired(self) -> bool:
        return datetime.datetime.now() > self.expires_at

    def is_fulfilled(self) -> bool:
        return self.fulfilled
