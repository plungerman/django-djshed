#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from django.core.management import execute_from_command_line


def main():
    """Clear the cache and repopulate it for API data."""
    execute_from_command_line(['manage.py', 'clearcache'])


if __name__ == '__main__':
    sys.exit(main())
