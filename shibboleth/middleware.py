from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from shibboleth.app_settings import SHIBBOLETH_USER_KEY, DJANGO_SESSION_MAY_OUTLIVE_SHIBBOLETH_SESSION


class ShibbolethRemoteUserMiddleware(RemoteUserMiddleware):

    header=SHIBBOLETH_USER_KEY

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist 
            if request.user.is_authenticated() and not DJANGO_SESSION_MAY_OUTLIVE_SHIBBOLETH_SESSION:
                # if we do not allow the django session to outlive the shibboleth session,
                # then remove any existing authenticated remote-user
                self._remove_invalid_user(request)
            return
        if request.user.is_authenticated():
        # If the shibboleth session exists, we are making sure any authenticated user matches the user passed by shibboleth
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the user authorized by shibboleth.
                self._remove_invalid_user(request)

        # At this point, there is a shibboleth header but the user is not authenticated
        # So we are now authenticating him using the custom backend
        user = auth.authenticate(remote_user=username,meta=request.META)
        if user:
            # If authentication worked, set the new user object and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
