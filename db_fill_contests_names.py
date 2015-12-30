from argparse import ArgumentParser
import xml.etree.ElementTree as ETree
import os
import os.path
import sqlite3
import re


name_to_order = {
    "июль": 1,
    "август": 2,
    "кострома": 3,
    "николаев": 4,
    "подмосковье": 5,
    "зима": 6
}
parallel_convert = {
    'A\'': 'A\'',
    'A0': 'A0',
    'AA': 'AA',
    'AS': 'AS',
    'AY': 'AY',
    'B\'': 'B\'',
    'C\'': 'C\'',
    'Ccpp': 'C.cpp',
    'Cpy': 'C.py',
    'A\'+': 'A\'',
    'A0+': 'A0',
    'AA+': 'AA',
    'AS+': 'AS',
    'AY+': 'AY',
    'B\'+': 'B\'',
    'C\'+': 'C\'',
    'Ccpp+': 'C.cpp',
    'Cpy+': 'C.py'
}


def parse_args():
    parser = ArgumentParser(description="db_fill_contest_names - read contest names from xmls, get parallels and seasos from names and write it to database.")

    parser.add_argument('xmls', help='directory with xmls')
    parser.add_argument('database', help='sqlite3 database file')

    return vars(parser.parse_args())


def ejudge_get_contest_name(xml_filename):
    try:
        with open(xml_filename, encoding='utf-8') as f:
            data = f.read()
    except UnicodeError:
        return None
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        return None
    try:
        return xml_root.find("name").text
    except AttributeError:
        return None


year_regex = re.compile('20[0-9]{2}')
parallel_regex = re.compile('(?:' + re.escape('.') + '|\\s)' +
                            '(?:[ABCDPSKWTMEFZСА]|AS|AA|AY)(?:\.?py|\.?python|prime|' +
                            '\.?' + re.escape('c++') + '|' + re.escape('++') + '|\.?cpp|[0-9]+|' +
                            re.escape('\'') + ')?' + re.escape('+') +
                            '?(?:' + re.escape('.') + '|\\s|$)')
season_regex = re.compile('(?:Июль|Август|Зима|Николаев|Подмосковье)', re.I)
day_regex = re.compile(
    '(?:(?:день|day)(?:\\s|\\.)*[0-9]{1,2}|(?:(?:\\s|\\.|D)[0-9]{1,2}(?:\\s|\\.|[^0-9]|$))(?!(?:день|day)))',
    re.I)


def get_contest_info(contest_name): # (year, order, parallel, day)
    if 'ЛКШ' not in contest_name or 'template' in contest_name.lower():
        return None
    year, order, parallel = 0, 0, ""
    if not year_regex.findall(contest_name):
        year = 0
    else:
        year = int(year_regex.findall(contest_name)[0])
    if 'олимпиада' in contest_name.lower() or 'contest' in contest_name.lower() or 'соревнование' in contest_name.lower():
        return None
    if not parallel_regex.findall(contest_name):
        return None

    # Please, think twice, if you want to change this replaces.
    parallel = re.sub('\\s', '', parallel_regex.findall(contest_name)[0].replace('.', ''))
    parallel = re.sub('prime', '\'', parallel)
    parallel = re.sub('python', 'py', parallel)
    parallel = re.sub(re.escape('c++'), 'cpp', parallel)
    parallel = re.sub(re.escape('++'), 'cpp', parallel)
    parallel = re.sub(re.escape('С'), 'C', parallel)  # Russian letters!
    parallel = re.sub(re.escape('А'), 'A', parallel)

    if parallel.startswith('D') and parallel != 'D':
        parallel = 'D'

    if len(parallel) == 1 or (len(parallel) == 2 and parallel[1] == '+'):
        parallel = parallel[0]
    elif parallel not in parallel_convert:
        return None
    else:
        parallel = parallel_convert[parallel]

    if not season_regex.findall(contest_name):
        return None
    order_name = season_regex.findall(contest_name)[0].lower()
    order = name_to_order.get(order_name, 0)

    if 'зачет' in contest_name.lower() or 'зачёт' in contest_name.lower() or 'зачот' in contest_name.lower() or 'exam' in contest_name.lower():
        return None
    if not day_regex.findall(contest_name):
        day = 0
    else:  # This replaces is also dangerous.
        day = day_regex.findall(contest_name)[0]
        day = re.sub('\\s', '', day)
        day = re.sub('\\.', '', day)
        day = re.sub('(?:день|day)', '', day, flags=re.I)
        day = day.lstrip('D')
        day = day.lstrip('d')
        day = day.lstrip('0')
        day = re.sub('[^0-9]', '', day)
        try:
            day = int(day)
        except ValueError:
            return None
    return (year, order, parallel, day)


args = parse_args()
xmls_dir = args['xmls']
if xmls_dir[-1] != '/':
    xmls_dir += '/'
database_file = args['database']

conn = sqlite3.connect(database_file)
cursor = conn.cursor()

for xml_filename in os.listdir(xmls_dir):
    try:
        contest_id = int(xml_filename.split('.')[0])
    except ValueError:
        continue
    contest_name = ejudge_get_contest_name(xmls_dir + xml_filename)
    if contest_name is None:
        continue
    contest_info = get_contest_info(contest_name)
    if contest_info is None:
        continue

    year, order, parallel_name, day = contest_info

    cursor.execute("SELECT id FROM stats_parallel WHERE name=?", (parallel_name,))
    parallel_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM stats_season WHERE year=? AND \"order\"=?", (year, order))
    season_id = cursor.fetchone()[0]

    cursor.execute("UPDATE stats_contest SET name=?, parallel_id=?, season_id=?, day=? WHERE contest_id=?",
        (contest_name, parallel_id, season_id, day, contest_id))

conn.commit()
conn.close()
