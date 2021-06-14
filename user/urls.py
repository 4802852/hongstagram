from django.urls import path

from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='home'),
    path('signup/', views.signup, name='signup')
]
