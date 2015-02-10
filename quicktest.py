"""
Adapted from LA Times datadesk credit to Ben Welsh. 

http://datadesk.latimes.com/posts/2012/06/test-your-django-app-with-travisci/

"""

import os
import sys
from django.conf import settings


class QuickDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.
    
    Example usage:
    
        >>> QuickDjangoTest('app1', 'app2')
    
    Based on a script published by Lukasz Dziedzia at: 
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    )
    
    def __init__(self, *args, **kwargs):
        self.apps = args
        self._tests()
        
    
    def _tests(self):
        settings.configure(
            DEBUG = True,
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            SHIBBOLETH_LOGIN_URL = 'https://your_domain.edu/Shibboleth.sso/Login',
            SHIBBOLETH_LOGOUT_URL = 'https://your_domain.edu/Shibboleth.sso/Logout',
            LOGIN_URL = '/shib/login/',
            INSTALLED_APPS = self.INSTALLED_APPS + self.apps,
            ROOT_URLCONF = 'shib.urls',
        )
        import django
        django.setup()
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner().run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)

if __name__ == '__main__':
    """
    What do when the user hits this file from the shell.
    
    Example usage:
    
        $ python quicktest.py app1 app2
    
    """
    apps = sys.argv[1:]
    QuickDjangoTest(*apps)
