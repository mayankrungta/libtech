from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    context = {'title': 'LibTech'}
    template = 'home.html'
    return render(request, template, context)

def about(request):
    context = {'title': 'About Us'}
    template = 'about.html'
    return render(request, template, context)

@login_required
def profile(request):
    user = request.user
    context = {'title': 'User: ' + user.username, 'user': user}
    template = 'profile.html'
    return render(request, template, context)
