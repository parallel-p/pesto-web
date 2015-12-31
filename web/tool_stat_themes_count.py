from argparse import ArgumentParser
import xml.etree.ElementTree as ETree
import os
import os.path
import sqlite3


def main(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # (participation_id, problem_id)
    solved = set()
    total = dict()

    cursor.execute("SELECT problem_id, participation_id, outcome FROM stats_submit")
    for problem_id, participation_id, outcome in cursor.fetchall():
        if outcome in ("PD", "OK", "AC"):
            solved.add((participation_id, problem_id))
        total.add((participation_id, problem_id))

    # stats[(participation_id, theme_id)] = solved
    stats = dict()
    stats_total = dict()
    theme_cache = {}
    for participation_id, problem_id in total:
        if problem_id in theme_cache:
            theme = theme_cache[problem_id]
        else:
            cursor.execute("SELECT stats_contest.theme_id FROM stats_problem JOIN stats_contest on stats_problem.contest_id = stats_contest.id WHERE stats_problem.id=?", (problem_id,))
            theme = cursor.fetchone()[0]
            theme_cache[problem_id] = theme
        key = (participation_id, theme)
        if key[1] is not None:
            stats_total[key] = stats.get(key, 0) + 1
    for participation_id, problem_id in solved:
        key = (participation_id, theme_cache[problem_id])
        if key[1] is not None:
            stats[key] = stats.get(key, 0) + 1

    cursor.execute("DELETE FROM themes_userresult")
    for row in stats:
        cursor.execute("INSERT INTO themes_userresult (participation_id, theme_id, solved, total) VALUES (?,?,?,?)",
            (row[0], row[1], stats[row], stats_total[row]))

    conn.commit()
    conn.close()


def parse_args():
    parser = ArgumentParser(description="tool_stat_themes_count - cout problems for every user, theme and season")
    parser.add_argument('database', help='sqlite3 database_file')
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    database_file = args['database']
    main(database_file)
