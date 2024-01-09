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
    '--new_term',
    action='store_true',
    help="Are the API data for new term(s)?",
    dest='new_term',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Fetch the workday people data from API."""
    if new_term:
        # for new terms, we set all course status to False and
        # then fetch the new courses from API which then have a
        # status of True.
        Course.objects.all().update(status=False)
        api_courses = get_courses(test=test)
    else:
        # we fetch all of the courses for the current term(s)
        # and compare them to the courses from the API.
        # if a course no longer appears in the API data,
        # we remove it from the local database.
        current_courses = Course.objects.filter(status=True)
        api_courses = get_courses(test=test)
        for course in current_courses:
            if course not in api_courses:
                course.delete()


if __name__ == '__main__':
    args = parser.parse_args()
    new_term = args.new_term
    test = args.test
    sys.exit(main())
