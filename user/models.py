from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.manager import BaseManager

class UserManager(BaseUserManager):
    def create_user(self, emailmobile, username, password, full_name, **extra_fields):
        user = self.model(
            emailmobile = emailmobile,
            full_name = full_name,
            username = username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, emailmobile, username, password, full_name=None):
        user = self.create_user('0123456789', username, password, 'superuser')
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    emailmobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True, null=True)
    mobile_number = models.CharField(max_length=20, unique=True, null=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'