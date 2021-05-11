import re
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models.expressions import Exists

from .models import User


def emailmobile_validator(value):
    email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
    mobile_number_pattern = re.compile('^[0-9]{1,15}$')
    if not (re.match(email_pattern, value) or re.match(mobile_number_pattern, value)):
        raise forms.ValidationError('X')

class SignUpForm(forms.Form):
    emailmobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}), validators=[emailmobile_validator])
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_emailmobile(self):
        emailmobile = self.cleaned_data['emailmobile']
        if User.objects.filter(
            Q(email = emailmobile) |
            Q(mobile_number = emailmobile)
        ).Exists():
            raise forms.ValidationError('ALREADY EXISTS!')
        return emailmobile
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.object.filter(
            Q(username=username)
        ).Exists():
            raise forms.ValidationError('ALREADY EXISTS!')
        return username

    def save(self):
        if self.is_valid():
            User.objects.create_user(
                emailmobile=self.cleaned_data['emailmobile'],
                full_name=self.cleaned_data['full_name'],
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
            )
            return User

