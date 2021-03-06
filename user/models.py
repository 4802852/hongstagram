from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from hongstagram import settings
import re


class UserManager(BaseUserManager):
    def create_user(self, emailmobile, full_name, username, password, **extra_fields):
        user = self.model(
            emailmobile=emailmobile, full_name=full_name, username=username, **extra_fields
        )
        email_pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        mobile_number_pattern = re.compile("^[0-9]{1,15}$")
        if re.match(email_pattern, emailmobile):
            user.email = emailmobile
        if re.match(mobile_number_pattern, emailmobile):
            user.mobile_number = emailmobile
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user("0123456789", "superuser", username, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    emailmobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    introduction = models.TextField(max_length=500, null=True, blank=True)

    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_following", blank=True)
    followed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_followed", blank=True)

    USERNAME_FIELD = "username"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def clean(self):
        if self.email == "":
            self.email = None
        if self.mobile_number == "":
            self.mobile_number = None

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("profile", args=[str(self.username)])

    class Meta:
        db_table = "users"
