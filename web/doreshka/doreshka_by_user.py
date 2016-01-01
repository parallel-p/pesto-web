from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User
from .models import UserResult

def choose_form(a, form1, form2, form5):
    if a % 10 in {0, 5, 6, 7, 8, 9} or 11 <= a <= 19:
        return str(a) + ' ' + form5
    elif a % 10 == 1:
        return str(a) + ' ' + form1
    else:
        return str(a) + ' ' + form2


def doreshka_by_user(user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        ures = UserResult.objects.filter(user=user)[0]
    except IndexError:
        return None
    
    hr, mn = ures.average_time // 3600, ures.average_time // 60 % 60
    
    hr = choose_form(hr, 'час', 'часа', 'часов')
    mn = choose_form(mn, 'минута', 'минуты', 'минут')
    
    return hr + ' ' + mn
