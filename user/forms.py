import re
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models.expressions import Exists
from django.contrib.auth.hashers import check_password

from .models import User


def emailmobile_validator(value):
    email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
    mobile_number_pattern = re.compile('^[0-9]{1,15}$')
    if not (re.match(email_pattern, value) or re.match(mobile_number_pattern, value)):
        raise forms.ValidationError('X')


class LoginForm(forms.Form):
    emailmobile = forms.CharField(widget=forms.TextInput(), error_messages={
                                  'required': '아이디를 입력해주세요.'}, label='아이디')
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={
                               'required': '비밀번호를 입력해주세요.'}, label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        emailmobile = cleaned_data.get('emailmobile')
        password = cleaned_data.get('password')
        if emailmobile and password:
            try:
                user = User.objects.get(
                    Q(email=emailmobile) | Q(mobile_number=emailmobile))
            except User.DoesNotExist:
                self.add_error('emailmobile', '사용자가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')


class SignUpForm(forms.Form):
    emailmobile = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', }), validators=[emailmobile_validator])
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_emailmobile(self):
        emailmobile = self.cleaned_data['emailmobile']
        if User.objects.filter(
            Q(email=emailmobile) |
            Q(mobile_number=emailmobile)
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
