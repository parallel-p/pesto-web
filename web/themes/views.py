from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User
from .models import UserResult

def by_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    years = UserResult.objects.filter(user=user).values('year').distinct()
    years = [str(i['year']) for i in years]
    result = {}
    for year in years:
        year_res = UserResult.objects.filter(user=user).filter(year=year).order_by('solved')
        result[year] = []
        for theme_res in year_res[::-1]:
            result[year].append([theme_res.theme.name, theme_res.solved])
    return render(request, 'by_user.html', {'result':result})