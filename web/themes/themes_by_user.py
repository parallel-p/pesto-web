from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User, Participation
from .models import UserResult

class PartResult:
    def __init__(self, part):
        self.part = part
        self.themes = []

def themes_by_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    parts = Participation.objects.filter(user=user).order_by('season')
    result = []
    for part in parts:
        part_res = UserResult.objects.filter(participation=part).order_by('-solved')
        if not part_res:
            continue
        cur_res = PartResult(str(part))
        for theme_res in part_res:
            cur_res.themes.append([theme_res.theme.name, theme_res.solved])
        result.append(cur_res)
    return result
