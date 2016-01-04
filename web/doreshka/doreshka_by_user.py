from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User, Language
from .models import UserResult

def lang_name_by_lang_id(id):
    return Language.objects.filter(id=id).get().name

def choose_form(a, form1, form2, form5):
    if a % 10 in {0, 5, 6, 7, 8, 9} or 11 <= a <= 19:
        return str(a) + ' ' + form5
    elif a % 10 == 1:
        return str(a) + ' ' + form1
    else:
        return str(a) + ' ' + form2

def doreshka_by_user_seconds(user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        ures = UserResult.objects.filter(user=user)[0]
    except IndexError:
        return None
    
    return ures.average_time

def rejected_by_user(user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        ures = UserResult.objects.filter(user=user)[0]
    except IndexError:
        return 0

    return ures.rj

def perfect_by_user(user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        ures = UserResult.objects.filter(user=user)[0]
    except IndexError:
        return 0

    return ures.pf

def lang_by_user(user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        ures = UserResult.objects.filter(user=user)[0]
    except IndexError:
        return 0

    return lang_name_by_lang_id(ures.lg)

def get_time_str(time):
    hr, mn = time // 3600, time // 60 % 60
    hr = choose_form(hr, 'час', 'часа', 'часов')
    mn = choose_form(mn, 'минута', 'минуты', 'минут')
    return hr + ' ' + mn

def doreshka_by_user_str(user_id):
    doreshka_time = doreshka_by_user_seconds(user_id)
    if doreshka_time is None:
        return None
    return get_time_str(doreshka_time)

def get_rating():
    results = UserResult.objects.all()
    rating = []
    for num, result in enumerate(results):
        rating.append((num + 1, result.user, get_time_str(result.average_time), result.rj, result.pf))
    return rating

