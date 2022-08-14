import os

from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from hongstagram import settings
from .forms import NewCommentForm, NewPostForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.db.models import Q
from urllib.parse import urlparse

from .models import Photo, Post, Comment
from user.models import User


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = "post/home.html"
    context_object_name = "post_list"

    def get_queryset(self):
        post_list = Post.objects.order_by("-id")
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context["paginator"]
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get("page")
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context["page_range"] = page_range
        return context


def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.order_by("-id").all()
    if request.user == post.writer:
        post_auth = True
    else:
        post_auth = False
    context = {"post": post, "post_auth": post_auth, "comments": comments}
    return render(request, "post/post_detail.html", context)


def post_new(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            post.hashtag_save()
            for img in request.FILES.getlist("imgs"):
                photo = Photo()
                photo.post = post
                photo.image = img
                photo.save()
            return redirect("post-detail", post.id)
    else:
        form = NewPostForm()
    return render(request, "post/post_new.html", {"form": form})


def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    if post.writer == request.user or request.user.is_superuser == True:
        photos = Photo.objects.filter(post=post)
        for photo in photos:
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.image.path))
            photo.delete()
        post.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect("home")
    else:
        messages.error(request, "본인의 게시글만 삭제할 수 있습니다.")
    return redirect("post-detail", pk)


def post_update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        if post.writer == request.user:
            if request.FILES:
                photos = Photo.objects.filter(post=post)
                for photo in photos:
                    os.remove(os.path.join(settings.MEDIA_ROOT, photo.image.path))
                    photo.delete()
            form = NewPostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.writer = request.user
                post.save()
                post.hashtag_save()
                for img in request.FILES.getlist("imgs"):
                    photo = Photo()
                    photo.post = post
                    photo.image = img
                    photo.save()
                messages.success(request, "수정되었습니다.")
                return redirect("post-detail", post.id)
    else:
        if post.writer == request.user:
            form = NewPostForm(instance=post)
            context = {
                "form": form,
                "update": True,
            }
            return render(request, "post/post_new.html", context)
        else:
            messages.error(request, "본인 게시글만 수정할 수 있습니다.")
            return redirect("post-detail", pk)


def search(request):
    b = request.GET.get("b", "")
    if b:
        username_search = User.objects.get(username=b)
        if username_search:
            return redirect("profile", username_search.username)
        search_result = Post.objects.all()
        search_result = search_result.filter(Q(hashtags__name__icontains=b)).order_by("-id")
        return render(request, "post/home.html", {"b": b, "post_list": search_result})
    else:
        messages.error(request, "검색어를 입력해주세요.")
        return redirect("home")


def profile_page(request, username):
    user = User.objects.get(username=username)
    if user == request.user:
        mypage = True
    else:
        mypage = False
    post_list = Post.objects.filter(writer=user)
    context = {
        "profile_user": user,
        "mypage": mypage,
        "post_list": post_list,
    }
    return render(request, "post/profile.html", context)


class PostLike(generic.base.View):
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            post_id = kwargs["pk"]
            post = Post.objects.get(id=post_id)
            user = request.user
            if user in post.like.all():
                post.like.remove(user)
            else:
                post.like.add(user)
            referer_url = request.META.get("HTTP_REFERER")
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        else:
            return HttpResponseForbidden()


def comment_create(request, pk):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.writer = request.user
            comment.save()
            return redirect("post-detail", pk)
    # else:
    #     form = NewCommentForm()


def comment_delete(request, pk, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if comment.writer == request.user or request.user.is_superuser == True:
        comment.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect("post-detail", pk)
    else:
        messages.error(request, "본인의 게시글만 삭제할 수 있습니다.")
    return redirect("post-detail", pk)
