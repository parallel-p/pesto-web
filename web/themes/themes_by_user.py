from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from stats.models import User, Participation
from .models import UserResult

class PartResult:
    def __init__(self, part):
        self.part = part
        self.themes = []
        self.solved = 0
        self.total = 0
        self.percent = 0
    def __repr__(self):
        return 'PartResult("{}", {})'.format(self.part, str(self.themes))
    
class DataTable:
    def __init__(self, arr):
        self.arr = arr
    def __repr__(self):
        return 'google.visualization.arrayToDataTable({})'.format(str(self.arr))
    
def solved_percent(res):
    if res.total:
        return res.solved * 100 // res.total
    else:
        return 0
    
    
def themes_by_user(user_id):
    user = get_object_or_404(User, pk=user_id)
    parts = Participation.objects.filter(user=user).order_by('season')
    result = []
    themes_total = dict()
    for part in parts:
        part_res = sorted(UserResult.objects.filter(participation=part), key=solved_percent, reverse=True)
        if not part_res:
            continue
        cur_res = PartResult(str(part))
        for theme_res in part_res:
            cur_res.themes.append([theme_res.theme.name, theme_res.solved, theme_res.total, solved_percent(theme_res)])
            theme = theme_res.theme
            if theme in themes_total:
                themes_total[theme][0] += theme_res.solved
                themes_total[theme][1] += theme_res.total
            else:
                themes_total[theme] = [theme_res.solved, theme_res.total]
            cur_res.solved += theme_res.solved
            cur_res.total += theme_res.total
        cur_res.percent = solved_percent(cur_res)  
        result.append(cur_res)

    total_res = PartResult("Всего")
    for theme in themes_total:
        solved, total = themes_total[theme]
        total_res.themes.append([theme.name, solved, total, solved * 100 // total])
        total_res.solved += solved
        total_res.total += total
    total_res.percent = solved_percent(total_res)
    total_res.themes.sort(key=lambda theme: theme[3], reverse=True)
    result.append(total_res)

    return result

def user_themes_chart(user_id):
    user = get_object_or_404(User, pk=user_id)
    solved = themes_by_user(user.id)
    result = []
            
    
    for part in solved:
        part_result = [['', 'Решено задач', 'Не решено']]
        for theme, solved, total, percent in part.themes:
            part_result.append([theme, solved, total - solved])
        result.append([part.part, DataTable(part_result)]) 
    result = result[-1:] + result[:-1]
    if len(result) == 1:
        return '[]'
    if len(result) == 2:
        result = [result[1]]
    return str(result)
