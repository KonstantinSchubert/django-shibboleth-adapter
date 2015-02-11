from django.contrib.auth.models import User, Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from shibboleth.app_settings import SHIB_ATTRIBUTE_LIST



class ShibbolethRemoteUserBackend(RemoteUserBackend):
    """
    Inherits from and slightly modifies https://docs.djangoproject.com/en/1.6/_modules/django/contrib/auth/backends/#RemoteUserBackend
    """


    def authenticate(self, remote_user, meta):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not remote_user:
            return
        user = None
        username = self.clean_username(remote_user)

        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username
            })
            if created:
                user = self.configure_user(user,meta)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass
        return user

    def configure_user(self,user,meta):
        for attribute in SHIB_ATTRIBUTE_LIST:
            try:
                user.__setattr__(attribute["user_attribute"] ,meta[attribute["shibboleth_key"]])
            except AttributeError as e:
                if attribute["required"]:
                    raise e
        user.set_unusable_password()
        user.save() # necessary?
        return user


class ShibbolethValidationError(Exception):
    pass
