from django.urls import path

from . import views

urlpatterns = [
    # path('', views.LoginView.as_view(), name='home'),
    path("", views.login_view, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile-update/", views.profile_update_view, name="profile-update"),
]
