import os
import django 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from doreshka.models import UserResult, DinnerTime
from stats.models import Submit, User, Participation, Season
import time

def start_of_day(timestamp):
    local = time.localtime(timestamp)
    start = time.struct_time((local.tm_year, local.tm_mon, local.tm_mday, 0, 0, 0, 0, 0, 0))
    return time.mktime(start)
    
def fill_doreshka(default_dinner=14*3600):
    users = User.objects.all()
    UserResult.objects.all().delete()
    season_cache = {}
    cnt = 0
    part_max = {}


    users = User.objects.all()
    res_by_user_rj = {}
    res_by_user_pf = {}
    first_submit_by_user_problem = {}
    for user in users:
        res_by_user_rj[user.id] = 0
        res_by_user_pf[user.id] = 0
        first_submit_by_user_problem[user.id] = {}

    submits = Submit.objects.all()
    for submit in submits:
        cnt += 1
        if cnt % 100 == 0:
            print(cnt, '/', len(submits), 'submits processed')

        if submit.outcome == 'RJ' or submit.outcome == 'SV':
            try:
                res_by_user_rj[submit.participation.user.id] += 1
            except Exception:
                pass
        try:
            if submit.problem.id not in first_submit_by_user_problem[submit.participation.user.id].keys():
                first_submit_by_user_problem[submit.participation.user.id][submit.problem.id] = (submit.timestamp, submit.outcome)
            if first_submit_by_user_problem[submit.participation.user.id][submit.problem.id][0] > submit.timestamp:
                first_submit_by_user_problem[submit.participation.user.id][submit.problem.id] = (submit.timestamp, submit.outcome)
        except Exception:
            pass

    for user in users:
        for problem_id in first_submit_by_user_problem[user.id]:
            try:
                if first_submit_by_user_problem[user.id][problem_id][1] == 'OK':
                    res_by_user_pf[user.id] += 1
            except Exception:
                pass

    cnt = 0
    for user in users:
        cnt += 1
        if cnt % 100 == 0:
            print(cnt, '/', len(users), 'users processed')
        max_time_by_day = {}
        participations = Participation.objects.filter(user=user).all()
        for part in participations:
            if 'Зима' in part.season.name:
                continue
            submits = Submit.objects.filter(participation=part).all()
            dinner = default_dinner
            max_time_by_season_day = part_max.get(part.season.id, {})
            if part.season.id not in season_cache:
                try:
                    dt = DinnerTime.objects.filter(season=part.season)[0]
                except:
                    season_cache[part.season.id] = 0
                else:
                    season_cache[part.season.id] = dt.dinner_delta
            dinner += season_cache[part.season.id]
            for submit in submits:
                submit_time = submit.timestamp
                day = int(start_of_day(submit_time))
                max_time_by_day[day] = max(max_time_by_day.get(day, 0), submit_time - day - dinner)
                max_time_by_season_day[day, user] = max(max_time_by_season_day.get((day, user), 0), submit_time - day - dinner)
            part_max[part.season.id] = max_time_by_season_day
        if not max_time_by_day:
            continue
        avg_time = int(sum(max_time_by_day.values()) / len(max_time_by_day))
        res = UserResult(user=user, average_time=avg_time, rj=res_by_user_rj[user.id], pf=res_by_user_pf[user.id])
        res.save()
    for pid in part_max:
        if not part_max[pid]:
            continue
        avg = int(sum(part_max[pid].values()) / len(part_max[pid]) / 60)
        name = Season.objects.filter(id=pid)[0].name
        print(name, '%d:%02d' % (avg // 60, avg % 60))
                    
    
if __name__ == "__main__":
    fill_doreshka()