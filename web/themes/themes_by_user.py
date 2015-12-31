from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User, Participation
from .models import UserResult

class PartResult:
    def __init__(self, part):
        self.part = part
        self.themes = []
    def __repr__(self):
        return 'PartResult("{}", {})'.format(self.part, str(self.themes))
    
def solved_percent(res):
    if res.total:
        return res.solved / res.total
    else:
        return 0
    
    
def themes_by_user(user_id):
    user = get_object_or_404(User, pk=user_id)
    parts = Participation.objects.filter(user=user).order_by('season')
    result = []
    for part in parts:
        part_res = sorted(UserResult.objects.filter(participation=part), key=solved_percent, reverse=True)
        if not part_res:
            continue
        cur_res = PartResult(str(part))
        for theme_res in part_res:
            cur_res.themes.append([theme_res.theme.name, theme_res.solved, theme_res.total, solved_percent(theme_res)])
        result.append(cur_res)
    return result
