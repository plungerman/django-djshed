from django.conf import settings
from django.http import  Http404
from django.shortcuts import render
from django.core.cache import cache

from djshed.constants import *
from djimix.constants import TERM_LIST
from djimix.core.utils import get_connection

from collections import OrderedDict


def get_sched():
    SCHED = OrderedDict()
    SCHED['R'] = ['Semester Courses']
    SCHED['A'] = ['Adult Undergraduate Studies 7-Week Courses']
    SCHED['G'] = ['Graduate Education']
    return SCHED.copy()


def home(request):
    """
    home page view with list of course types and links to relevant year
    """

    sched = get_sched()
    weir = 'AND  sec_rec.sess[1,1] in ("R","A","G","T","P")'
    sql = '{} {} {}'.format(SCHEDULE_SQL, weir, SCHEDULE_ORDER_BY)

    connection = get_connection()
    cursor = connection.cursor()
    objs = cursor.execute(sql)

    if objs:
        for o in objs:
            sess = o[10].strip()
            program = o[11].strip()
            dic = {
                'sess':sess,'name':TERM_LIST[sess],
                'yr':o[9],'program':program
            }
            try:
                sched[program].append(dic)
            except:
                pass
    else:
        sched = None

    return render(
        request, 'home.html', {'sched': sched}
    )


def schedule(request, program, term, year, content_type='html'):
    """
    Display the full course schedule for all classes given:
    program
    term
    year
    """
    if not program and not term and not year:
        raise Http404
    else:
        # open database connection
        connection = get_connection()
        cursor = connection.cursor()

        SCHED = get_sched()
        key = 'dates_{}_{}_{}_{}_api'.format(year, term, program, content_type)
        dates = cache.get(key)
        if not dates:
            # dates
            sql = '{} WHERE sess = "{}" AND yr = "{}"'.format(DATES, term, year)
            dates = cursor.execute(sql)
            columns = [column[0] for column in dates.description]
            results = []
            for row in dates.fetchall():
                results.append(dict(zip(columns, row)))
            dates = results
            cache.set(key, dates, timeout=604800)

        title = None
        if dates:
            # this will barf if the request is an old URL like /T/TC/2011/
            # so we raise 404 in that case
            try:
                title = '{} <br> {} {}'.format(
                    SCHED[program][0], TERM_LIST[term], year
                )
            except:
                raise Http404

            key = 'schedule_{}_{}_{}_{}_api'.format(year, term, program, content_type)
            sched = cache.get(key)
            if not sched:
                weir = """
                    AND sec_rec.sess = '{}' AND sec_rec.yr = '{}'
                    ORDER BY dept, crs_no, sec_no
                """.format(term, year)
                sql = '{} {}'.format(SCHEDULE_SQL, weir)
                sched = cursor.execute(sql)
                columns = [column[0] for column in sched.description]
                results = []
                for row in sched.fetchall():
                    results.append(dict(zip(columns, row)))
                sched = results
                cache.set(key, sched, timeout=604800)
            # close our database cursor and connection
            cursor.close()
            connection.close()

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
            # close our database cursor and connection
            cursor.close()
            connection.close()
            raise Http404

