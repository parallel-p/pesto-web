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

        themes = set()
        for user in solved:
            for ures in user:
                if ures.parallel == parallel:
                    themes |= {res[0] for res in ures.themes}
                    break
        themes = list(themes)
        themes.sort()
        theme_to_index = {theme: index for index, theme in enumerate(themes)}

        user_results = []
        for user in solved:
            for ures in user:
                if ures.parallel == parallel:
                    curr_result = [0] * len(themes)
                    for res in ures.themes:
                        curr_result[theme_to_index[res[0]]] = res[3]
                    user_results.append(curr_result)
                    break
        user_results = list(map(list, zip(*([themes] + user_results))))
        print(user_results)
        user_results.sort(key=lambda x:-x[1])
        user_results = [[''] + list(map(str, users))] + user_results
        result.append([parallel, DataTable(user_results)]) 
    return render(request, 'compare.html', {'data': str(result)})
