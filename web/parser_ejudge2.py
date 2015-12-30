class SQLiteConnector:
    def __init__(self, db_dir):
        import sqlite3
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
        import pymysql
        self.connection = pymysql.connect(**config)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.close()

def parse_ejudge2(sqlite_dir, mysql_config):
    import os.path
    print(os.path.abspath(sqlite_dir))

    print('CONNECTING TO DATA...', end='')
    sqlite_db = SQLiteConnector(sqlite_dir)
    mysql_db = MySQLConnector(mysql_config)

    print('OK\nREADING DATA...', end='')
    mysql_cur = mysql_db.get_cursor()
    mysql_cur.execute('SELECT contest_id, user_id FROM runs')
    ejudge_con_and_usr_id_list = []
    for i in mysql_cur:
        ejudge_con_and_usr_id_list.append(i)
    mysql_cur = mysql_db.get_cursor()
    mysql_cur.execute('SET NAMES utf8')
    mysql_cur.execute('SELECT user_id, contest_id, username FROM users')
    ejudge_usr_id_and_name_list = []
    for i in mysql_cur:
        ejudge_usr_id_and_name_list.append(i)

    sqlite_cur = sqlite_db.get_cursor()
    sqlite_cur.execute('SELECT id, first_name, last_name FROM stats_user')
    sqlite_id_first_second = []
    for i in sqlite_cur:
        sqlite_id_first_second.append(i)
    sqlite_cur = sqlite_db.get_cursor()
    sqlite_cur.execute('SELECT contest_id, parallel_id, season_id FROM stats_contest')
    sqlite_contest_parallel_season = []
    for i in sqlite_cur:
        sqlite_contest_parallel_season.append(i)
    sqlite_cur.execute('SELECT id, parallel_id, season_id, user_id FROM stats_participation')
    sqlite_participation = []
    for i in sqlite_cur:
        sqlite_participation.append(i)
    participation_dict = {}
    for id, parallel_id, season_id, user_id in sqlite_participation:
        participation_dict[(parallel_id, season_id, user_id)] = id
    sqlite_cur.execute('SELECT stats_problem.id, stats_contest.parallel_id, stats_contest.season_id FROM stats_problem JOIN stats_contest ON stats_problem.contest_id=stats_contest.id')
    parallel_season_by_problem = {}
    for problem, parallel, season in sqlite_cur:
        parallel_season_by_problem[problem] = (parallel, season)
    submits = []
    sqlite_cur.execute('SELECT stats_submit.id, stats_submit.problem_id, stats_submit.user_id, stats_contest.contest_id FROM stats_submit JOIN stats_problem ON stats_submit.problem_id = stats_problem.id JOIN stats_contest ON stats_problem.contest_id = stats_contest.id')
    for i in sqlite_cur:
        submits.append(i)
    print('OK\nWRITING SUBMITS FIRST...', end='')
    ids_in_ej = {}
    for id, first_name, last_name in sqlite_id_first_second:
        for user_id, contest_id, name in ejudge_usr_id_and_name_list:
            if contest_id and name is not None and first_name in name and last_name in name and ',' not in name:
                ids_in_ej[user_id] = id
                #print(contest_id, user_id, ':', id, name, first_name, last_name)
                #input()

    p_and_s = {}
    for user_id, parallel, season, no_fate in sqlite_participation:
        p_and_s[user_id] = (parallel, season)
    print(len(ids_in_ej))
    print('OK\nWRITING SUBMITS SECOND...', end='')
    c111 = c222 = c333 = c444 = 0
    for id, problem_id, ejudge_user_id, ejudge_contest_id in submits:
        try:
            c111 += 1
            user_id = ids_in_ej[ejudge_user_id, ejudge_contest_id]
            c222 += 1
            parallel, season = parallel_season_by_problem[problem_id]
            c333 += 1
            participation = participation_dict[parallel, season, user_id]
            c444 += 1
        except KeyError:
            continue
        sqlite_cur.execute('UPDATE stats_submit SET participation_id = {0} WHERE id={1}'.format(participation, id))
    print('OK')
    print(c111, c222, c333, c444)
    sqlite_db.connection.commit()
    sqlite_db.close_connection()
    mysql_db.close_connection()

