from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User

def index(request):
    return HttpResponse("Sample text")

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'profile.html', {'user': user})
