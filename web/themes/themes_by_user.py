from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from stats.models import User
from .models import UserResult

def themes_by_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    years = UserResult.objects.filter(user=user).values('year').distinct()
    years = [str(i['year']) for i in years]
    result = []
    for year in years:
        year_res = UserResult.objects.filter(user=user).filter(year=year).order_by('solved')
        result.append([year, []])
        for theme_res in year_res[::-1]:
            result[-1][1].append([theme_res.theme.name, theme_res.solved])
    template = loader.get_template('by_user.html')
    return template.render({'result': result}, request)
