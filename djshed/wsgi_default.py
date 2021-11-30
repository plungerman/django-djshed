# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys


# python
sys.path.append('/data2/python_venv/3.8/djshed/lib/python3.8/')
sys.path.append('/data2/python_venv/3.8/djshed/lib/python3.8/site-packages/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djshed.settings')
os.environ.setdefault('PYTHON_EGG_CACHE', '/var/cache/python/.python-eggs')
os.environ.setdefault('TZ', 'America/Chicago')
# informix
os.environ['INFORMIXSERVER'] = ''
os.environ['DBSERVERNAME'] = ''
os.environ['INFORMIXDIR'] = ''
os.environ['ODBCINI'] = ''
os.environ['ONCONFIG'] = ''
os.environ['INFORMIXSQLHOSTS'] = ''
os.environ['LD_LIBRARY_PATH'] = '$INFORMIXDIR/lib:$INFORMIXDIR/lib/esql:$INFORMIXDIR/lib/tools:/usr/lib/apache2/modules:$INFORMIXDIR/lib/cli'
os.environ['LD_RUN_PATH'] = '$INFORMIXDIR/lib:$INFORMIXDIR/lib/esql:$INFORMIXDIR/lib/tools:/usr/lib/apache2/modules'
# wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
