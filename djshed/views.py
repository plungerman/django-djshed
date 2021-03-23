from django.conf import settings
from django.http import  Http404
from django.shortcuts import render
from django.core.cache import cache

from djshed.constants import SCHEDULE_SQL
from djshed.constants import DATES
from djimix.constants import TERM_LIST
from djimix.core.database import get_connection, xsql

from collections import OrderedDict


def get_sched():
    """Create the schedule dictionary."""
    SCHED = OrderedDict()
    SCHED['R'] = ['Semester Courses']
    SCHED['A'] = ['Adult Undergraduate Studies 7-Week Courses']
    SCHED['G'] = ['Graduate Education']
    return SCHED.copy()


def home(request):
    """Home page view with list of course types and links to relevant year."""
    sched = get_sched()
    weir = """
        AND web_display_date <= today
        AND web_display_end >= today
    """
    sql = """
        {0} AND sec_rec.sess[1,1] in ("R","A","G","T","P")
        ORDER BY
        sec_rec.yr DESC,
        program,
        (
            CASE sec_rec.sess
            WHEN 'RC' THEN 1
            WHEN 'RB' THEN 2
            WHEN 'RE' THEN 3
            WHEN 'RA' THEN 4
            END
        ) ASC
    """.format(SCHEDULE_SQL(where=weir))
    with get_connection() as connection:
        courses = xsql(sql, connection)

        if courses:
            for course in courses:
                sess = course[10].strip()
                program = course[11].strip()
                dic = {
                    'sess':sess,'name':TERM_LIST[sess],
                    'yr':course[9],'program':program,
                }
                try:
                    sched[program].append(dic)
                except:
                    pass
        else:
            sched = None

    return render(request, 'home.html', {'sched': sched})


def schedule(request, program, term, year, content_type='html'):
    """
    Display the full course schedule for all classes.

    Required:
        program
        term
        year
    """
    if not program and not term and not year:
        raise Http404
    else:
        with get_connection() as connection:
            SCHED = get_sched()
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
                    title = '{0} <br> {1} {2}'.format(
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
                        {'title':title,'dates': dates,'sched':sched}
                    )
                else:
                    response = render(
                        request, 'schedule.json.html', {'sched':sched,},
                        content_type='application/json; charset=utf-8'
                    )

                return response
            else:
                raise Http404
