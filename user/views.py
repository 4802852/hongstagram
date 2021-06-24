from .models import User
from .forms import LoginForm, SignUpForm
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
import re


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/post'

    def form_valid(self, form):
        emailmobile = form.cleaned_data.get('emailmobile')
        password = form.cleaned_data.get('password')
        email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
        mobile_number_pattern = re.compile('^[0-9]{1,15}$')
        if re.match(email_pattern, emailmobile):
            user = authenticate(
                self.request, email=emailmobile, password=password)
        elif re.match(mobile_number_pattern, emailmobile):
            user = authenticate(
                self.request, mobile_number=emailmobile, password=password)
        if user:
            self.request.session['emailmobile'] = emailmobile
            login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    if request.method == SignUpForm(request.POST):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('/')
    else:
        signup_form = SignUpForm()

    context = {
        'form': signup_form,
    }
    return render(request, 'user/signup.html', context)

# class SignUpView(generic.CreateView):
#     model = User
#     template_name = 'signup.html'
#     form_class = SignUpForm

#     def get_success_url(self):
#         return redirect('/')

#     def form_valid(self, form):
#         self.object = form.save()
#         return redirect(self.get_success_url())


# PASSWORD_MINIMUM_LENGTH = 8

# class SignUpView(View):
#     def post(self, request):
#         try:
#             data = json.loads(request.body)

#             email = data.get('email', None)
#             mobile_number = data.get('mobile_number', None)
#             full_name = data.get('full_name', None)
#             username = data.get('username', None)
#             password = data.get('password', None)

#             email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
#             mobile_number_pattern = re.compile('^[0-9]{1,15}$')
#             username_pattern = re.compile('^(?=.*[a-z])[a-z0-9_.]+$')

#             if not (
#                 (email or mobile_number)
#                 and full_name
#                 and username
#                 and password
#             ):
#                 return JsonResponse({'message': 'KEY_ERROR'}, status=400)

#             if email:
#                 if not re.match(email_pattern, email):
#                     return JsonResponse({'message': 'EMAIL_VALIDATION_ERROR'}, status=400)

#             if mobile_number:
#                 if not re.match(mobile_number_pattern, mobile_number):
#                     return JsonResponse({'message':'MOBILE_NUMBER_VALIDATION_ERROR'}, status=400)

#             if not re.match(username_pattern, username):
#                 return JsonResponse({'message':'USERNAME_VALIDATION_ERROR'}, status=400)

#             if len(data['password']) < PASSWORD_MINIMUM_LENGTH:
#                 return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)

#             if User.objects.filter(
#                 Q(email = data.get('email', 1)) |
#                 Q(mobile_number = data.get('mobile_number', 1)) |
#                 Q(username = data.get['username'])
#             ).exists():
#                 return JsonResponse({'message': 'ALREADY_EXISTS'}, status=409)

#             User.objects.create(
#                 email = email,
#                 mobile_number = mobile_number,
#                 full_name = full_name,
#                 username = username,
#                 password = password
#             )
#             return JsonResponse({'message': 'SUCCESS'}, status=201)

#         except JSONDecodeError:
#             return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
