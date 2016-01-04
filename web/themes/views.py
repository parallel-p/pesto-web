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
    parallels = [pr.parallel for pr in solved[0]]
    for ures in solved[1:]:
        all_parallels = [cp.parallel for cp in ures]
        parallels = [pr for pr in parallels if pr in all_parallels]  # participated by everyone
    
    result = []
    for parallel in parallels:
        if parallel == 'Всего':
            continue
        user_results = []
        themes = []
        for user in solved:
            for ures in user:
                if ures.parallel == parallel:
                    ures.themes.sort()
                    user_results.append([res[3] for res in ures.themes])
                    themes = [res[0] for res in ures.themes]
                    break
        user_results = list(map(list, zip(*([themes] + user_results))))
        user_results.sort(key=lambda x:-x[1])
        user_results = [[''] + list(map(str, users))] + user_results
        result.append([parallel, DataTable(user_results)]) 
    return render(request, 'compare.html', {'data': str(result)})
