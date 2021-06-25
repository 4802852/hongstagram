from django.shortcuts import render

def home(request):
    username = request.session["username"]
    context = {"username": username}
    return render(request, 'post/home.html', context)