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

def get_similar_user_data(first_user, parts_1, solved_1, curr_user):
    if first_user.id == curr_user.id:
        return None
    result = SimilarUserData()
    result.user = curr_user

    parts = {(part.season, part.parallel) for part in Participation.objects.filter(user=curr_user) if part.parallel.name[0] in "ABCD"} & parts_1
    if len(parts) == 0:
        return None

    solved_2 = themes_by_user(curr_user.id)
    res_parts_1 = {pr.part for pr in solved_1 if pr.part != 'Всего'}
    res_parts_2 = {cp.part for cp in solved_2 if cp.part != 'Всего'}
    res_parts = res_parts_1 & res_parts_2
    
    similarity_data = dict()
    for ures in solved_1:
        if ures.part in res_parts:
            for res in ures.themes:
                similarity_data[ures.part, res[0]] = similarity_data.get((ures.part, res[0]), 0) + res[3]
    for ures in solved_2:
        if ures.part in res_parts:
            for res in ures.themes:
                similarity_data[ures.part, res[0]] = similarity_data.get((ures.part, res[0]), 0) - res[3]

    similarity_sum = 0
    similarity_count = len(similarity_data)
    for value in similarity_data.values():
        similarity_sum += abs(value)
    if similarity_count == 0:
        return None
    
    result.similarity = 100 - similarity_sum // similarity_count

    return result

def get_similar_users(user):
    result = []
    parts_1 = {(part.season, part.parallel) for part in Participation.objects.filter(user=user) if part.parallel.name[0] in "ABCD"}
    solved_1 = themes_by_user(user.id)
    for current_user in User.objects.all():
        similar_user_data = get_similar_user_data(user, parts_1, solved_1, current_user)
        if similar_user_data is not None:
            result.append(similar_user_data)
    result.sort(key=lambda user: user.similarity, reverse=True)
    for index, current_user in enumerate(result):
        current_user.index = index + 1
    return result
