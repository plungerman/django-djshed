# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.8/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djshed.settings")

from django.conf import settings

from djshed.constants import *

from djzbar.utils.informix import do_sql as do_esql

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
    dest="term"
)
parser.add_argument(
    "-y", "--year",
    required=True,
    help="Four digit year.",
    dest="year"
)

def main():
    """
    Fetch the data and print
    """
    weir = """
        AND sec_rec.sess = '{}'
        AND sec_rec.yr = '{}'
        ORDER BY dept, crs_no, sec_no
    """.format(term, year)
    sql = "{} {}".format(SCHEDULE_SQL, weir)
    print sql
    objs = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=settings.INFORMIX_EARL)
    sched = None
    if objs:
        sched = objs.fetchall()
        count = 0
        for s in sched:
            if count < 20:
                print s
                count += 1
    else:
        print "No schedule data"

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    term = args.term
    year = args.year

    print args

    sys.exit(main())

