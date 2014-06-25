#!/usr/bin/env python
import os
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'html2xlsx', 'tests',
        ]
    )

from django.test.simple import DjangoTestSuiteRunner

def runtests():
    test_runner = DjangoTestSuiteRunner(verbosity=1)
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
