from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import UserResult
from stats.models import User
from .themes_by_user import themes_by_user

class CompareResult:
    def __init__(self, result):
        self.part = result[0].part
        self.result = result

class MultiPartResult:
    def __init__(self, part_results):
        self.part = part_results[0].part
        self.themes = [theme[0] for theme in part_results[0].themes]
        self.result = []
        self.total = []
        self.rowspan = len(self.themes) + 2
        for cr in part_results:
            self.total.append([cr.solved, cr.total, cr.percent])
        for theme in range(len(self.themes)):
            cres = []
            for cr in part_results:
                cres.append(cr.themes[theme])
            self.result.append(cres)
    
    def __repr__(self):
        return 'MultiPartResult({})'.format(self.result)

def compare(request, users):
    users = sorted(map(int, users.split(',')))
    users = [get_object_or_404(User, id=uid) for uid in users]
    solved = [themes_by_user(user.id) for user in users]
    parts = [pr.part for pr in solved[0]]
    for ures in solved[1:]:
        parts = [pr for pr in parts if pr in [cp.part for cp in ures]]  # participated by everyone
    
    result = []
    for part in parts:
        if part == 'Всего':
            continue
        user_results = []
        for user in solved:
            for ures in user:
                if ures.part == part:
                    user_results.append(ures)
                    break
        for ures in user_results:
            ures.themes.sort(key=lambda x:x[0])
        result.append(MultiPartResult(user_results)) 
    return render(request, 'compare.html', {'users': users, 'result': result})