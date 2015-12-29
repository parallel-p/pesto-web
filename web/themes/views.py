from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User
from .models import UserResult

def by_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    years = UserResult.objects.filter(user=user).values('year').distinct()
    years = [i['year'] for i in years]
    result = ['<style>td{border:1px solid gray;padding:2px;}</style>']
    for year in years:
        year_res = UserResult.objects.filter(user=user).filter(year=year).order_by('solved')
        result.append('<div style="float:left;margin-left:10px;"><b>{}:</b> <table style="border-collapse:collapse">'.format(year))
        for theme_res in year_res[::-1]:
            result.append('<tr><td>{}</td><td>{}</td></tr>'.format(theme_res.theme.name, theme_res.solved))
        result.append('</table></div>')
    return HttpResponse('\n'.join(result))