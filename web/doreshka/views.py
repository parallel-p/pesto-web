from django.shortcuts import render
from .doreshka_by_user import get_rating

def doreshka_rating(request):
    return render(request, 'doreshka_rating.html', {'rating': get_rating()})
