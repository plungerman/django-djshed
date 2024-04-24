# -*- coding: utf-8 -*-

from collections import OrderedDict
from django.conf import settings
from django.http import  Http404
from django.shortcuts import render
from django.core.cache import cache
from djimix.constants import TERM_LIST
from djimix.core.database import get_connection, xsql
from djshed.constants import SCHEDULE_SQL
from djshed.constants import DATES
from djshed.models import Course


def get_sched():
    """Create the schedule dictionary."""
    SCHED = OrderedDict()
    SCHED['R'] = ['Semester Courses']
    SCHED['A'] = ['7-Week Courses']
    SCHED['G'] = ['Graduate Education']
    return SCHED.copy()


def home(request):
    """Home page view with list of course types and links to relevant year."""
    return render(request, 'home.html', {})


def schedule(request, program, term, year):
    """
    Display the full course schedule for all classes.

    Required:
        program
        term
        year
    """
    SCHED = get_sched()
    content_type = 'html'
    program = program.upper()
    term = term.upper()
    # deal with old requests like:
    # /schedule/R/RC/2014&method%3Ddetail&dept%3D_GFW/
    year = year[0:4]
    if not program and not term and not year:
        raise Http404
    elif int(year) > 2022 and term != 'GE':
        term = TERM_LIST[term.upper()]
        try:
            title = '{0}: {1} {2}'.format(
                SCHED[program][0], term, year
            )
        except Exception:
            raise Http404
        term = '{0} {1}'.format(year, term)
        courses = Course.objects.filter(
            year=year,
        ).filter(
            term=term,
        ).order_by('department', 'number', 'section')
        response = render(
            request, 'schedule.api.html',
            {'title': title, 'dates': None, 'sched': courses},
        )
    else:
        with get_connection() as connection:
            key = 'dates_{0}_{1}_{2}_{3}_api'.format(
                year, term, program, content_type
            )
            dates = cache.get(key)
            if not dates:
                # dates
                sql = '{0} WHERE sess = "{1}" AND yr = "{2}"'.format(
                    DATES, term, year
                )
                dates = xsql(sql, connection)
                columns = [column[0] for column in dates.description]
                results = []
                for row in dates.fetchall():
                    results.append(dict(zip(columns, row)))
                dates = results
                cache.set(key, dates)

            title = None
            if dates:
                # this will barf if the request is an old URL like /T/TC/2011/
                # so we raise 404 in that case
                try:
                    title = '{0}: {1} {2}'.format(
                        SCHED[program][0], TERM_LIST[term], year
                    )
                except:
                    raise Http404

                key = 'schedule_{0}_{1}_{2}_{3}_api'.format(
                    year, term, program, content_type,
                )
                sched = cache.get(key)
                if not sched:
                    weir = """
                        AND sec_rec.sess = '{0}' AND sec_rec.yr = '{1}'
                    """.format(term, year)
                    sql = '{0} {1}'.format(
                        SCHEDULE_SQL(where=weir), 'ORDER BY dept, crs_no, sec_no',
                    )
                    sched = xsql(sql, connection)
                    columns = [column[0] for column in sched.description]
                    results = []
                    for row in sched.fetchall():
                        results.append(dict(zip(columns, row)))
                    sched = results
                    cache.set(key, sched)

                if content_type == 'html':
                    response = render(
                        request, 'schedule.html',
                        {'title': title, 'dates': dates, 'sched': sched}
                    )
                else:
                    response = render(
                        request, 'schedule.json.html', {'sched':sched,},
                        content_type='application/json; charset=utf-8'
                    )
            else:
                raise Http404
    return response
