import os.path
import sqlite3
import pymysql

NAME_CONVERT = [
   ["Наталья", "Наталия"],
   ["Евгений", "Женя"],
   ["Екатерина", "Катя", "Катерина"],
   ["Сергей", "Сережа"],
   ["Анна", "Аня"],
   ["Елена", "Лена", "Алёна"],
   ["Юлия", "Юля"],
   ["Иван", "Ваня"],
   ["Константин", "Костя", "Констанитин"],
   ["Михаил", "Миша"],
   ["Владислав", "Влад"],
   ["Роман", "Рома"],
   ["Данииил", "Даниил", "Данил", "Даня"],
   ["Мария", "Марья", "Маша"],
   ["Григорий", "Гриша"],
   ["Александр", "Саша"],
   ["Ибрагим", "Ибрахим"],
   ["Мадибек", "Мадибеков"],
   ["Андрей", "Андреей"],
   ["Жуссупов", "Жусупов"],
   ["Белоногов", "Белонгов"],
   ["Одилзода", "Одил"],
   ["Мехрдод", "Мехрдоди"]
]

class SQLiteConnector:
    def __init__(self, db_dir):
        self.connection = sqlite3.connect(db_dir)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()

class MySQLConnector:
    """Example of config
    config = {'user': 'root', 'passwd': '', 'host': 'localhost', 'port': 3306, 'db': 'ejudge_db'}
    """

    def __init__(self, config):
        self.connection = pymysql.connect(**config)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.close()

def parse_ejudge2(sqlite_dir, mysql_config):
    print(os.path.abspath(sqlite_dir))
    print('CONNECTING TO DATA...', end='')
    sqlite_db = SQLiteConnector(sqlite_dir)
    mysql_db = MySQLConnector(mysql_config)

    print('OK\nREADING DATA...', end='')
    mysql_cur = mysql_db.get_cursor()
    mysql_cur.execute('SET NAMES utf8')
    mysql_cur.execute('SELECT user_id, contest_id, username FROM users')
    ejudge_usr_id_and_name_list = list(mysql_cur)
    sqlite_cur = sqlite_db.get_cursor()
    sqlite_cur.execute('SELECT id, first_name, last_name FROM stats_user')
    sqlite_id_first_second = list(sqlite_cur)
    sqlite_cur = sqlite_db.get_cursor()
    sqlite_cur.execute('SELECT contest_id, parallel_id, season_id FROM stats_contest')
    sqlite_contest_parallel_season = {}
    for contest, parallel, season in sqlite_cur:
        if sqlite_contest_parallel_season.get(contest // 100 * 100, (None, None))[0] is None:
            sqlite_contest_parallel_season[contest // 100 * 100] = (parallel, season)
    sqlite_cur.execute('SELECT id, parallel_id, season_id, user_id FROM stats_participation')
    sqlite_participation = list(sqlite_cur)
    participation_dict = {}
    for id, parallel_id, season_id, user_id in sqlite_participation:
        participation_dict[(parallel_id, season_id, user_id)] = id
    sqlite_cur.execute('SELECT stats_problem.id, stats_contest.parallel_id, stats_contest.season_id FROM stats_problem JOIN stats_contest ON stats_problem.contest_id=stats_contest.id')
    parallel_season_by_problem = {}
    for problem, parallel, season in sqlite_cur:
        parallel_season_by_problem[problem] = (parallel, season)
    sqlite_cur.execute('SELECT stats_submit.id, stats_submit.problem_id, stats_submit.user_id, stats_contest.contest_id FROM stats_submit JOIN stats_problem ON stats_submit.problem_id = stats_problem.id JOIN stats_contest ON stats_problem.contest_id = stats_contest.id')
    submits = list(sqlite_cur)

    print('OK\nWRITING SUBMITS...', end='')
    ids_in_ej = {}
    for id, first_name, last_name in sqlite_id_first_second:
        parts = list(sqlite_cur.execute('SELECT id, season_id, parallel_id FROM stats_participation WHERE stats_participation.user_id=?', (id,)))
        ok = False
        for part_id, season_id, parallel_id in parts:
            year, order = sqlite_cur.execute('SELECT year, "order" FROM stats_season WHERE id=?', (season_id,)).fetchone()
            if (year < 2008 or (year == 2008 and order != 6)) or (year == 2013 and order == 6):
                continue
            parallel_name = sqlite_cur.execute('SELECT name FROM stats_parallel WHERE id=?', (parallel_id,)).fetchone()[0]
            sqlite_cur.execute('SELECT id FROM stats_submit WHERE participation_id=?', (part_id,))
            if parallel_name[0] not in "PKMWS" and len(sqlite_cur.fetchall()) == 0:
                ok = True
                break
        if not ok:
            continue
        print(first_name, last_name)

        first_name_1 = first_name.replace("(", " ").replace(")", " ").split()
        first_name_2 = []
        for ln in first_name_1:
            new_first_names = [ln]
            for variants in NAME_CONVERT:
                if ln in variants:
                    new_first_names = variants
            first_name_2 += new_first_names
        first_name_1 = first_name_2
        first_name_1_rp = [(' ' + name + ' ').replace("Ё", "Е").replace("ё", "е") for name in first_name_1]

        last_name_1 = [last_name]
        last_name_1 = last_name.replace("(", " ").replace(")", " ").split()
        last_name_2 = []
        for ln in last_name_1:
            new_last_names = [ln]
            for variants in NAME_CONVERT:
                if ln in variants:
                    new_last_names = variants
            last_name_2 += new_last_names
        last_name_1 = last_name_2
        last_name_1_rp = [(' ' + name + ' ').replace("Ё", "Е").replace("ё", "е") for name in last_name_1]

        for user_id, contest_id, name in ejudge_usr_id_and_name_list:
            try:
                parallel = sqlite_contest_parallel_season[contest_id // 100 * 100][0]
                season = sqlite_contest_parallel_season[contest_id // 100 * 100][1]
            except KeyError:
                continue
            if name is None:
                continue
            new_name = (' ' + name + ' ').replace("Ё", "Е").replace("ё", "е")
            first_name_ok = False
            for fn in first_name_1_rp:
                if fn in new_name:
                    first_name_ok = True
                    break
            last_name_ok = False
            for ln in last_name_1_rp:
                if ln in new_name:
                    last_name_ok = True
                    break
            if (first_name_ok and last_name_ok and
                (parallel, season, id) in participation_dict and
                ',' not in name):
                ids_in_ej[(user_id, contest_id // 100 * 100)] = id
    for id, problem_id, ejudge_user_id, ejudge_contest_id in submits:
        try:
            user_id = ids_in_ej[ejudge_user_id, ejudge_contest_id // 100 * 100]
            parallel, season = parallel_season_by_problem[problem_id]
            participation = participation_dict[parallel, season, user_id]
        except KeyError:
            continue
        sqlite_cur.execute('UPDATE stats_submit SET participation_id={0} WHERE id={1}'.format(participation, id))

    print('OK')

    sqlite_db.close_connection()
    mysql_db.close_connection()

if __name__ == "__main__":
    config = {'user': 'root', 'passwd': '5382JOihyt', 'host': '127.0.0.1', 'port': 3306, 'db': 'ejudgedata'}
    parse_ejudge2('db.sqlite3', config)
