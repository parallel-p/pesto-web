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

def parse_ejudge(sqlite_dir, mysql_config):
    import os.path
    print(os.path.abspath(sqlite_dir))

    ejudge_status = {0: 'OK',
                     1: 'CE',
                     2: 'RT',
                     3: 'TL',
                     4: 'PE',
                     5: 'WA',
                     6: 'CF',
                     7: 'PT',
                     8: 'AC',
                     9: 'IG',
                     10: 'DQ',
                     11: 'PD',
                     12: 'ML',
                     13: 'SE',
                     14: 'SV',
                     15: 'WT',
                     16: 'PR',
                     17: 'RJ',
                     18: 'SK'}

    print('CONNECTING TO DATA...', end='')
    sqlite_db = SQLiteConnector(sqlite_dir)
    mysql_db = MySQLConnector(mysql_config)
    mysql_cur = mysql_db.get_cursor()
    sqlite_cur = sqlite_db.get_cursor()
    print('OK\nREADING DATA...', end='')

    mysql_cur.execute('SELECT contest_id, prob_id, lang_id, status, user_id, run_id FROM runs')
    print('OK\nWRITING USERS...', end='')

    ids_for_problems = {}
    ids_for_contests = {}
    ids_for_users = {}

    list_for_problems = []
    list_for_submits = []
    list_for_contests = []
    list_for_users = []

    for i in mysql_cur:
        list_for_problems.append( (i[0], i[1]) )
        list_for_submits.append(i)
        list_for_contests.append(i[0])
        list_for_users.append(i[4])

    for i in set(list_for_users):
        # sqlite_cur.execute('INSERT INTO stats_user (user_id) VALUES ({0})'.format(i))
        ids_for_users[i] = sqlite_cur.lastrowid
    print('OK\nWRITING CONTESTS...', end='')

    sqlite_cur.execute('DELETE FROM stats_contest')
    for i in set(list_for_contests):
        sqlite_cur.execute('INSERT INTO stats_contest (contest_id) VALUES ({0})'.format(i))
        ids_for_contests[i] = sqlite_cur.lastrowid
    print('OK\nWRITING PROBLEMS...', end='')

    sqlite_cur.execute('DELETE FROM stats_problem')
    for i in set(list_for_problems):
        sqlite_cur.execute("INSERT INTO stats_problem (contest_id, name) VALUES ({0}, '{1}')".format(ids_for_contests[i[0]], ''))
        ids_for_problems[i] = sqlite_cur.lastrowid
    print('OK\nWRITING SUBMITS...', end='')

    sqlite_cur.execute('DELETE FROM stats_submit')
    for i in list_for_submits:
        try:
            sqlite_cur.execute("INSERT INTO stats_submit (outcome, lang_id, problem_id, user_id, submit_id) VALUES ('{0}', {1}, {2}, {3}, {4})".format(ejudge_status[i[3]], i[2], ids_for_problems[i[0], i[1]], i[4], i[5]))
        except KeyError:
            pass
    print('OK')



    sqlite_db.close_connection()
    mysql_db.close_connection()

if __name__ == "__main__":
    config = {'user': 'root', 'passwd': 'root', 'host': 'localhost', 'port': 3306, 'db': 'ejudgedata'}
    parse_ejudge('db.sqlite3', config)
