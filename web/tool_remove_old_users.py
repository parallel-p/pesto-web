from argparse import ArgumentParser
import xml.etree.ElementTree as ETree
import os
import os.path
import sqlite3


def main(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stats_season WHERE year < 2008 OR (year = 2008 AND 'order' != 6)")
    cursor.execute("DELETE FROM stats_participation WHERE (SELECT COUNT(*) FROM stats_season WHERE id=season_id)=0")
    cursor.execute("DELETE FROM stats_user WHERE (SELECT COUNT(*) FROM stats_participation WHERE stats_participation.user_id=stats_user.id)=0")

    conn.commit()
    conn.close()


def parse_args():
    parser = ArgumentParser(description="tool_remove_old_users - remove users from old seasons.")
    parser.add_argument('database', help='sqlite3 database_file')
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    database_file = args['database']
    main(database_file)
