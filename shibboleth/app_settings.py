
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


SHIB_ATTRIBUTE_LIST = getattr(settings, 'SHIBBOLETH_ATTRIBUTE_LIST')
#Set to true if you are testing and want to insert sample headers.
SHIB_MOCK_HEADERS = getattr(settings, 'SHIBBOLETH_MOCK_HEADERS', False)

SHIBBOLETH_LOGIN_URL = getattr(settings, 'SHIBBOLETH_LOGIN_URL', None)

if not SHIBBOLETH_LOGIN_URL:
    raise ImproperlyConfigured("A SHIBBOLETH_LOGIN_URL is required.  Specify in settings.py")

#Optional logout parameters
#This should look like: https://sso.school.edu/idp/logout.jsp?return=%s
#The return url variable will be replaced in the LogoutView.
SHIBBOLETH_LOGOUT_URL = getattr(settings, 'SHIBBOLETH_LOGOUT_URL', None)
#LOGOUT_REDIRECT_URL specifies a default logout page that will always be used when
#users logout from Shibboleth.
LOGOUT_REDIRECT_URL = getattr(settings, 'SHIBBOLETH_LOGOUT_REDIRECT_URL', None)
#Name of key.  Probably no need to change this.  
SHIBBOLETH_USER_KEY = getattr(settings, 'SHIBBOLETH_USER_KEY', None)



DJANGO_SESSION_MAY_OUTLIVE_SHIBBOLETH_SESSION = getattr(settings, 'SHIBBOLETH_DJANGO_SESSION_MAY_OUTLIVE_SHIBBOLETH_SESSION', False)
