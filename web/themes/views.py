from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import UserResult
from stats.models import User
from .themes_by_user import themes_by_user

class DataTable:
    def __init__(self, arr):
        self.arr = arr
    def __repr__(self):
        return 'google.visualization.arrayToDataTable({})'.format(str(self.arr))

def compare(request, users):
    users = sorted(map(int, users.split(',')))
    users = [get_object_or_404(User, id=uid) for uid in users]
    solved = [themes_by_user(user.id) for user in users]
    parts = [pr.part for pr in solved[0]]
    for ures in solved[1:]:
        all_parts = [cp.part for cp in ures]
        parts = [pr for pr in parts if pr in all_parts]  # participated by everyone
    
    result = []
    for part in parts:
        if part == 'Всего':
            continue
        user_results = []
        themes = []
        for user in solved:
            for ures in user:
                if ures.part == part:
                    ures.themes.sort()
                    user_results.append([res[3] for res in ures.themes])
                    themes = [res[0] for res in ures.themes]
                    break
        user_results = list(map(list, zip(*([themes] + user_results))))
        user_results.sort(key=lambda x:-x[1])
        user_results = [[''] + list(map(str, users))] + user_results
        result.append([part, DataTable(user_results)]) 
    return render(request, 'compare.html', {'data': str(result)})
