from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("new-post/", views.post_new, name="post-new"),
    path("<int:pk>/", views.post_detail_view, name="post-detail"),
    path("<int:pk>/delete", views.post_delete, name="post-delete"),
    path("<int:pk>/update", views.post_update, name="post-update"),
    path("<int:pk>/like", views.PostLike.as_view(), name="post-like"),
    path("search/", views.search, name="search"),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    # Comment
    path("<int:pk>/comment", views.comment_create, name="comment_create"),
    path(
        "<int:pk>/comment/<int:comment_id>/delete",
        views.comment_delete,
        name="comment_delete",
    ),
]
