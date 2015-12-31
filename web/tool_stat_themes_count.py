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

    cursor.execute("SELECT problem_id, participation_id, outcome FROM stats_submit")
    for problem_id, participation_id, outcome in cursor.fetchall():
        if outcome in ("PD", "OK", "AC"):
            solved.add((participation_id, problem_id))
    cursor.execute("SELECT stats_contest.season_id, stats_contest.parallel_id, stats_contest.theme_id , stats_problem.id FROM stats_problem JOIN stats_contest ON stats_problem.contest_id = stats_contest.id")
    total_dict = {}
    themes = set()
    for season, parallel, theme, pid in cursor.fetchall():
        total_dict[season, parallel, theme] = total_dict.get((season, parallel, theme), 0) + 1
        themes.add(theme)
    cursor.execute('SELECT id, season_id, parallel_id FROM stats_participation')
    part_dict = {}
    for id, season, parallel in cursor.fetchall():
        part_dict[id] = (season, parallel)

    # stats[(participation_id, theme_id)] = solved
    stats = dict()
    stats_total = dict()
    theme_cache = {}
    for participation_id, problem_id in solved:
        if problem_id in theme_cache:
            theme = theme_cache[problem_id]
        else:
            cursor.execute("SELECT stats_contest.theme_id FROM stats_problem JOIN stats_contest on stats_problem.contest_id = stats_contest.id WHERE stats_problem.id=?", (problem_id,))
            theme = cursor.fetchone()[0]
            theme_cache[problem_id] = theme
        key = (participation_id, theme)
        if key[1] is not None:
            stats[key] = stats.get(key, 0) + 1
    for part in part_dict:
        season, parallel = part_dict[part]
        for theme in themes:
            if total_dict.get((season, parallel, theme)) and not stats.get((part, theme)):
                stats[part, theme] = 0
    cursor.execute("DELETE FROM themes_userresult")
    for row in stats:
        if row[0] is None:
            continue
        season, parallel = part_dict[row[0]]
        total = total_dict[season, parallel, row[1]]
        cursor.execute("INSERT INTO themes_userresult (participation_id, theme_id, solved, total) VALUES (?,?,?,?)",
            (row[0], row[1], stats[row], total))

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
