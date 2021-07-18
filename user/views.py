from django.db.models import Q
from .models import User
from .forms import LoginForm, ProfileUpdateForm, SignUpForm
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
import re


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            emailmobile = login_form.cleaned_data.get("emailmobile")
            user = User.objects.get(Q(email=emailmobile) | Q(mobile_number=emailmobile))
            request.session["username"] = user.username
            login(request, user)
            return redirect("/post")
    else:
        login_form = LoginForm()
    return render(request, "login.html", {"form": login_form})


def logout_view(request):
    logout(request)
    return redirect("/")


def signup_view(request):
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect("/")
    else:
        signup_form = SignUpForm()

    context = {
        "form": signup_form,
    }
    return render(request, "user/signup.html", context)


def profile_update_view(request):
    user = request.user
    if request.method == "POST":
        profile_update_form = ProfileUpdateForm(request.POST, instance=user)
        if profile_update_form.is_valid():
            profile_update_form.save()
            return redirect("profile", user.username)
    else:
        profile_update_form = ProfileUpdateForm(instance=user)
    
    context = {
        "form": profile_update_form,
    }
    return render(request, "post/profile_update.html", context)