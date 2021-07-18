import re
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

from .models import User


def emailmobile_validator(value):
    email_pattern = re.compile("[^@]+@[^@]+\.[^@]+")
    mobile_number_pattern = re.compile("^[0-9]{1,15}$")
    if not (re.match(email_pattern, value) or re.match(mobile_number_pattern, value)):
        raise forms.ValidationError("휴대폰 번호 혹은 이메일 주소를 정확히 입력해주세요.")


class LoginForm(forms.Form):
    emailmobile = forms.CharField(error_messages={"required": "아이디를 입력해주세요."}, label="아이디")
    password = forms.CharField(
        widget=forms.PasswordInput(), error_messages={"required": "비밀번호를 입력해주세요."}, label="비밀번호"
    )

    def clean(self):
        cleaned_data = super().clean()
        emailmobile = cleaned_data.get("emailmobile")
        password = cleaned_data.get("password")
        if emailmobile and password:
            try:
                user = User.objects.get(Q(email=emailmobile) | Q(mobile_number=emailmobile))
            except User.DoesNotExist:
                self.add_error("emailmobile", "사용자가 존재하지 않습니다.")
                return
            if not check_password(password, user.password):
                self.add_error("password", "비밀번호가 틀렸습니다.")
                return


class SignUpForm(forms.Form):
    emailmobile = forms.CharField(
        max_length=100,
        label="휴대폰 번호 혹은 이메일 주소",
        validators=[emailmobile_validator],
        error_messages={"required": "휴대폰 번호 혹은 이메일 주소를 입력해주세요."},
    )
    full_name = forms.CharField(
        max_length=50, label="성명", error_messages={"required": "성명을 입력해주세요."}
    )
    username = forms.CharField(
        max_length=50, label="아이디", error_messages={"required": "아이디를 입력해주세요."}
    )
    password = forms.CharField(
        widget=forms.PasswordInput, label="비밀번호", error_messages={"required": "비밀번호를 입력해주세요."}
    )

    def clean_emailmobile(self):
        emailmobile = self.cleaned_data["emailmobile"]
        if User.objects.filter(Q(email=emailmobile) | Q(mobile_number=emailmobile)):
            raise forms.ValidationError("동일한 휴대폰 번호 혹은 이메일 주소가 있습니다.")
        return emailmobile

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(Q(username=username)):
            raise forms.ValidationError("동일한 아이디가 존재합니다.")
        return username

    def save(self):
        if self.is_valid():
            User.objects.create_user(
                emailmobile=self.cleaned_data["emailmobile"],
                full_name=self.cleaned_data["full_name"],
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
            )
            return User


def email_validator(value):
    email_pattern = re.compile("[^@]+@[^@]+\.[^@]+")
    if value == "None" or value == "":
        pass
    elif not re.match(email_pattern, value):
        raise forms.ValidationError("이메일 주소를 정확히 입력해주세요.")


def mobile_validator(value):
    mobile_number_pattern = re.compile("^[0-9]{1,15}$")
    if value == "None" or value == "":
        pass
    elif not re.match(mobile_number_pattern, value):
        raise forms.ValidationError("휴대폰 번호를 정확히 입력해주세요.")


# class ProfileUpdateForm(forms.Form):
#     email = forms.CharField(max_length=100, label="이메일주소", validators=[email_validator])
#     mobile_number = forms.CharField(max_length=20, label="휴대폰번호", validators=[mobile_validator])
#     full_name = forms.CharField(
#         max_length=50, label="성명", error_messages={"required": "성명을 입력해주세요."}
#     )
#     username = forms.CharField(
#         max_length=50, label="아이디", error_messages={"required": "아이디를 입력해주세요."}
#     )
#     introduction = forms.CharField(max_length=500)

#     def clean_email(self):
#         email = self.cleaned_data["email"]
#         if User.objects.filter(Q(email=email)):
#             raise forms.ValidationError("이메일 주소가 있습니다.")
#         return email

#     def clean_mobile(self):
#         mobile_number = self.cleaned_data["mobile_number"]
#         if self.email == None and mobile_number == None:
#             raise forms.ValidationError("이메일과 휴대폰번호 중 한개는 입력해야 합니다.")
#         if User.objects.filter(Q(mobile_number=mobile_number)):
#             raise forms.ValidationError("동일한 휴대폰 번호가 있습니다.")
#         return mobile_number

#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         if User.objects.filter(Q(username=username)):
#             raise forms.ValidationError("동일한 아이디가 존재합니다.")
#         return username
    
#     def save(self):
#         if self.is_valid():
#             User.objects.create_user(
#                 email=self.cleaned_data["email"],
#                 mobile_number=self.cleaned_data["mobile_number"],
#                 full_name=self.cleaned_data["full_name"],
#                 username=self.cleaned_data["username"],
#                 introduction=self.cleaned_data["introduction"]
#             )
#             return User


class ProfileUpdateForm(UserChangeForm):
    password = None
    email = forms.CharField(max_length=100, label="이메일주소", validators=[email_validator], required=False)
    mobile_number = forms.CharField(max_length=20, label="휴대폰번호", validators=[mobile_validator], required=False)
    full_name = forms.CharField(
        max_length=50, label="성명", error_messages={"required": "성명을 입력해주세요."}
    )
    username = forms.CharField(
        max_length=50, label="아이디", error_messages={"required": "아이디를 입력해주세요."}
    )
    introduction = forms.CharField(max_length=500)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email == "None":
            email = ""
        elif User.objects.filter(Q(email=email)):
            raise forms.ValidationError("이메일 주소가 있습니다.")
        return email

    def clean_mobile(self):
        email = self.cleaned_data["email"]
        if email == "None":
            email = ""
        mobile_number = self.cleaned_data["mobile_number"]
        if mobile_number == "None":
            mobile_number == ""
        if email == "" and mobile_number == "":
            raise forms.ValidationError("이메일과 휴대폰번호 중 한개는 입력해야 합니다.")
        elif User.objects.filter(Q(mobile_number=mobile_number)):
            raise forms.ValidationError("동일한 휴대폰 번호가 있습니다.")
        return mobile_number

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(Q(username=username)):
            raise forms.ValidationError("동일한 아이디가 존재합니다.")
        return username

    class Meta:
        model = User()
        fields = ['email', 'mobile_number', 'full_name', 'username', 'introduction']
