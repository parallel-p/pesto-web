from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User, Participation
from themes.themes_by_user import themes_by_user


def choose_form(a, form1, form2, form5):
    if a % 10 in {0, 5, 6, 7, 8, 9} or 11 <= a <= 19:
        return str(a) + ' ' + form5
    elif a % 10 == 1:
        return str(a) + ' ' + form1
    else:
        return str(a) + ' ' + form2

class SimilarUserData:
    pass

def get_similar_user_data(first_user, parallels_1, solved_1, curr_user):
    if first_user.id == curr_user.id:
        return None
    result = SimilarUserData()
    result.user = curr_user

    parallels = {part.parallel for part in Participation.objects.filter(user=curr_user) if part.parallel.name[0] in "ABCD"} & parallels_1
    if len(parallels) == 0:
        return None

    solved_2 = themes_by_user(curr_user.id)
    res_parallels_1 = {pr.parallel for pr in solved_1 if pr.parallel != 'Всего'}
    res_parallels_2 = {cp.parallel for cp in solved_2 if cp.parallel != 'Всего'}
    res_parallels = res_parallels_1 & res_parallels_2
    
    similarity_data = dict()
    for ures in solved_1:
        if ures.parallel in res_parallels:
            for res in ures.themes:
                similarity_data[ures.parallel, res[0]] = similarity_data.get((ures.parallel, res[0]), 0) + res[3]
                print(res[0], res[3])
    print("")
    for ures in solved_2:
        if ures.parallel in res_parallels:
            for res in ures.themes:
                similarity_data[ures.parallel, res[0]] = similarity_data.get((ures.parallel, res[0]), 0) - res[3]
                print(res[0], -res[3])
    print("")
    print(similarity_data)

    similarity_sum = 0
    similarity_count = len(similarity_data)
    if similarity_count == 0:
        return None
    for value in similarity_data.values():
        similarity_sum += abs(value)
    
    result.similarity = 100 - similarity_sum // similarity_count

    return result

def get_similar_users(user):
    result = []
    parallels_1 = {part.parallel for part in Participation.objects.filter(user=user) if part.parallel.name[0] in "ABCD"}
    solved_1 = themes_by_user(user.id)
    for current_user in User.objects.all():
        similar_user_data = get_similar_user_data(user, parallels_1, solved_1, current_user)
        if similar_user_data is not None:
            result.append(similar_user_data)
    result.sort(key=lambda user: user.similarity, reverse=True)
    for index, current_user in enumerate(result):
        current_user.index = index + 1
    return result
