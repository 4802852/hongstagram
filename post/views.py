from .forms import NewPostForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import Photo, Post
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
    if request.user == post.writer:
        post_auth = True
    else:
        post_auth = False

    context = {"post": post, "post_auth": post_auth}
    return render(request, "post/post_detail.html", context)


def post_new(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        username = request.session["username"]
        user = User.objects.get(username=username)

        if form.is_valid():
            post = form.save(commit=False)
            post.writer = user
            post.save()
            for img in request.FILES.getlist("imgs"):
                photo = Photo()
                photo.post = post
                photo.image = img
                photo.save()
            return redirect("post-detail", post.id)

    else:
        form = NewPostForm()
    return render(request, "post/post_new.html", {"form": form})
