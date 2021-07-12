from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name="home"),
    path('new-post/', views.post_new, name='post-new'),
    path('<int:pk>/', views.post_detail_view, name='post-detail'),
]
