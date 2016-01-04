import os.path
import sqlite3

class SQLiteConnector:
    def __init__(self, db_dir):
        self.connection = sqlite3.connect(db_dir)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()

def fill_unknown_participations(sqlite_dir):
    sqlite_db = SQLiteConnector(sqlite_dir)
    sqlite_cur = sqlite_db.get_cursor()

    sqlite_cur.execute('SELECT id, user_id, season_id, parallel_id FROM stats_participation')
    participations = list(sqlite_cur)
    for part_id, user_id, season_id, parallel_id in participations:
        year, order = sqlite_cur.execute('SELECT year, "order" FROM stats_season WHERE id=?', (season_id,)).fetchone()
        if (year < 2008 or (year == 2008 and order != 6)) or (year == 2013 and order == 6):
            continue
        parallel_name = sqlite_cur.execute('SELECT name FROM stats_parallel WHERE id=?', (parallel_id,)).fetchone()[0]
        sqlite_cur.execute('SELECT id FROM stats_submit WHERE participation_id=?', (part_id,))
        if parallel_name[0] not in "PKMWS" and len(sqlite_cur.fetchall()) == 0:
            season_name = sqlite_cur.execute('SELECT name FROM stats_season WHERE id=?', (season_id,)).fetchone()[0]
            first_name, last_name = sqlite_cur.execute('SELECT first_name, last_name FROM stats_user WHERE id=?', (user_id,)).fetchone()
            print(part_id, last_name, " ", first_name, "  ", season_name, parallel_name)

    sqlite_db.close_connection()


if __name__ == "__main__":
   fill_unknown_participations('db.sqlite3')
