# -*- coding: utf-8 -*-
import os, sys
# env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djshed.settings')

from django.conf import settings

from djshed.constants import *

from djimix.core.utils import get_connection

import argparse

"""
Grabs all of the course schedule data and displays it properly
"""

# set up command-line options
desc = """
Accepts as input: term, year
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-t", "--term",
    required=True,
    help="Two letter term code: e.g. RA",
    dest='term'
)
parser.add_argument(
    "-y", "--year",
    required=True,
    help="Four digit year.",
    dest='year'
)


def main():
    """
    Fetch the data and print
    """
    weir = '''
        AND sec_rec.sess = '{}'
        AND sec_rec.yr = '{}'
        ORDER BY dept, crs_no, sec_no
    '''.format(term, year)
    sql = '{} {}'.format(SCHEDULE_SQL, weir)
    print(sql)
    connection = get_connection()
    cursor = connection.cursor()
    sched = cursor.execute(sql)
    if sched:
        count = 1
        columns = [column[0]for column in sched.description]
        results = []
        for row in sched.fetchall():
            results.append(dict(zip(columns, row)))
        for r in results:
            count += 1
            print("{}|{}".format(count, r))
    else:
        print("No schedule data")

    # close our database cursor and connection
    cursor.close()
    connection.close()


if __name__ == '__main__':
    args = parser.parse_args()
    term = args.term
    year = args.year

    print(args)

    sys.exit(main())

