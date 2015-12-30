import sqlite3
import pymysql
import os.path


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

def add_timestamp(sqlite_dir, mysql_config):
    print(os.path.abspath(sqlite_dir))
    print('Connecting...', end='')
    sqlite_db = SQLiteConnector(sqlite_dir)
    mysql_db = MySQLConnector(mysql_config)
    mysql_cur = mysql_db.get_cursor()
    sqlite_cur = sqlite_db.get_cursor()
    print('OK')

    submits_sqlite = sqlite_cur.execute('SELECT stats_submit.id, stats_submit.submit_id, stats_contest.contest_id FROM stats_submit JOIN stats_problem ON stats_submit.problem_id = stats_problem.id JOIN stats_contest ON stats_problem.contest_id = stats_contest.id').fetchall()
    mysql_cur.execute('SELECT run_id, contest_id, UNIX_TIMESTAMP(create_time) FROM ejudgedata.runs')
    submit_time = {}
    submit_id = {}
    for rid, cid, ts in mysql_cur:
        submit_time[(rid, cid)] = ts
    for id, sid, cid in submits_sqlite:
        sqlite_cur.execute('UPDATE `stats_submit` SET `timestamp`={} WHERE `id`={}'.format(submit_time[sid, cid], id))
    print('Done')
    sqlite_db.close_connection()
    mysql_db.close_connection()

 
if __name__ == "__main__":
    sqlite_dir = './db.sqlite3'
    mysql_config = {'user': 'root', 'passwd': 'root', 'host': 'localhost', 'port': 3306, 'db': 'ejudgedata'}
    add_timestamp(sqlite_dir, mysql_config)