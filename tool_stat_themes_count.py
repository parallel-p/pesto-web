from argparse import ArgumentParser
import xml.etree.ElementTree as ETree
import os
import os.path
import sqlite3


def parse_args():
    parser = ArgumentParser(description="tool_stat_themes_count - cout problems for every user, theme and season")

    parser.add_argument('database', help='sqlite3 database file')

    return vars(parser.parse_args())


args = parse_args()
database_file = args['database']

conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# (participation_id, problem_id)
solved = set()

cursor.execute("SELECT problem_id, participation_id, outcome FROM stats_submit")
for submit in cursor.fetchall():
    problem_id, participation_id, outcome = submit
    if outcome in ("PD", "OK", "AC"):
        solved.add((participation_id, problem_id))

# stats[(participation_id, theme_id)] = solved
stats = dict()
for p in solved:
    cursor.execute("SELECT theme_id FROM stats_problem WHERE id=?", (p[1],))
    key = (participation_id, cursor.fetchone()[0])
    if key in stats:
        stats[key] += 1
    else:
        stats[key] = 1

for row in stats:
    cursor.execute("INSERT INTO themes_userresults VALUES (NULL,?,?,?)", (row[0], row[1], stats[row]))

conn.commit()
conn.close()
