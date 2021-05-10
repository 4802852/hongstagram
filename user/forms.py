import re
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


def emailmobile_validator(value):
    email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
    mobile_number_pattern = re.compile('^[0-9]{1,15}$')
    if not (re.match(email_pattern, value) or re.match(mobile_number_pattern, value)):
        raise forms.ValidationError('X')

class SignUpFrom(UserCreationForm):
    emailmobile = forms.CharField(validators=[emailmobile_validator])

    def __init__(self, *args, **kwargs):
        super(SignUpFrom, self).__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ['emailmobile', 'full_name', 'username', 'password']
    
    def save(self, commit=True):
        user = super(SignUpFrom, self).save(commit=False)
        user.save()
        return user
