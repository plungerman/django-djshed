from django.conf import settings
from django.http import  Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from djshed.constants import *

from djzbar.utils.informix import do_sql as do_esql

from collections import OrderedDict

SCHED = OrderedDict()
SCHED["R"] = ["Semester Courses"]
SCHED["A"] = ["Adult Education 7-Week Courses"]
SCHED["G"] = ["Graduate Education"]
#SCHED["T"] = ["Accelerated Certification for Teachers (ACT)"]
SCHED["P"] = ["Paralegal Program"]

EARL = settings.INFORMIX_EARL

def home(request):
    """
    home page view with list of course types and links to relevant year
    """

    sched = SCHED.copy()
    weir = 'AND  sec_rec.sess[1,1] in ("R","A","G","T","P")'
    sql = "{} {} {}".format(SCHEDULE_SQL, weir, SCHEDULE_ORDER_BY)
    objs = do_esql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)
    if objs:
        for o in objs.fetchall():
            dic = {
                "sess":o.sess,"name":TERM_LIST[o.sess],
                "yr":o.yr,"program":o.program
            }
            sched[o.program].append(dic)
    else:
        sched = None

    return render_to_response(
        "home.html",
        {"sched": sched},
        context_instance=RequestContext(request)
    )

def schedule(request, program, term, year):
    """
    Display the full course schedule for all classes given:
    program
    term
    year
    """
    if not program and not term and not year:
        raise Http404
    else:
        # dates
        sql = '{} WHERE sess = "{}" AND yr = "{}"'.format(DATES, term, year)
        objs = do_esql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)
        dates = None
        title = None
        if objs:
            dates = objs.fetchall()
            title = "{} <br> {} {}".format(
                SCHED[program][0], TERM_LIST[term], year
            )
            weir = """
                AND sec_rec.sess = '{}' AND sec_rec.yr = '{}'
                ORDER BY dept, crs_no, sec_no
            """.format(term, year)
            sql = "{} {}".format(SCHEDULE_SQL, weir)
            objs = do_esql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)
            sched = None
            if objs:
                sched = objs.fetchall()
            return render_to_response(
                "schedule.html",
                {"title":title,"dates": dates,"sched":sched},
                context_instance=RequestContext(request)
            )
        else:
            raise Http404

