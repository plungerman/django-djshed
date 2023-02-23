#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import django
import os
import sys


django.setup()

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djshed.settings.shell')

from djshed.api import get_courses
from djshed.models import Course


# set up command-line options
desc = "Load course data from workday into database."

parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Fetch the workday people data from API."""
    # destroy
    Course.objects.all().delete()
    for course in get_courses(test=test):
        print(course)


if __name__ == '__main__':
    args = parser.parse_args()
    test = args.test
    if test:
        test = True
    else:
        test = False

    sys.exit(main())
