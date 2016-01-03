import os.path
import sqlite3
import pymysql

FIRST_NAME_CONVERT = {
    "Наталья": " Наталия ",
    "Наталия": " Наталья ",
    "Евгений": " Женя ",
    "Екатерина": " Катя ",
    "Сергей": " Сережа ",
    "Анна": " Аня ",
    "Елена": " Лена ",
    "Юлия": " Юля ",
    "Иван": " Ваня ",
    "Константин": " Костя ",
    "Михаил": " Миша ",
    "Владислав": " Влад ",
    "Роман": " Рома ",
    "Даниил": " Данил ",
    "Данил": " Даня ",
    "Мария": " Марья ",
    "Марья": " Мария ",
    "Григорий": " Гриша ",
    "Александр": " Саша ",
    "Дмитрий": " Дима "
}

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
    num = 0
    for id, first_name, last_name in sqlite_id_first_second:
        first_name_rp = (' ' + first_name + ' ').replace("Ё", "Е").replace("ё", "е")
        last_name_rp = (' ' + last_name + ' ').replace("Ё", "Е").replace("ё", "е")
        if first_name in FIRST_NAME_CONVERT:
            first_name_1 = FIRST_NAME_CONVERT[first_name]
            first_name_1_rp = (' ' + first_name_1 + ' ').replace("Ё", "Е").replace("ё", "е")
        else:
            first_name_1 = None
            first_name_1_rp = None
        last_name_1_rp = None
        if "(" in last_name:
            last_name_rp, last_name_1_rp = last_name_rp.replace("(", " ").replace(")", " ").split()[:2]
        for user_id, contest_id, name in ejudge_usr_id_and_name_list:
            try:
                parallel = sqlite_contest_parallel_season[contest_id // 100 * 100][0]
                season = sqlite_contest_parallel_season[contest_id // 100 * 100][1]
            except KeyError:
                continue
            if name is None:
                continue
            new_name = (' ' + name + ' ').replace("Ё", "Е").replace("ё", "е")
            if (parallel, season, id) in participation_dict and \
               ',' not in name and \
               (first_name_rp in new_name or (first_name_1_rp is not None and first_name_1_rp in new_name)) and \
               (last_name_rp in new_name or (last_name_1_rp is not None and last_name_1_rp in new_name)):
                ids_in_ej[(user_id, contest_id // 100 * 100)] = id
        num += 1
        if num % 10 == 0:
            print(num, "/", len(sqlite_id_first_second))
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
    config = {'user': 'root', 'passwd': '5382JOihyt', 'host': '192.168.2.13', 'port': 3306, 'db': 'ejudgedata'}
    parse_ejudge2('db.sqlite3', config)
