django-shibboleth-adapter
============================

Middleware for using Shibboleth with Django.  Requires Django 1.6 or above.

[![Build Status](https://travis-ci.org/KonstantinSchubert/django-shibboleth-adapter.svg)](https://travis-ci.org/KonstantinSchubert/django-shibboleth-adapter)

Installation and configuration
------
 * Install directly from Github with pip:

   ```
   pip install git@github.com:KonstantinSchubert/django-shibboleth-adapter.git

   ```

 * In settings.py :

  * Enable the RemoteUserBackend.
  
    ```python
    AUTHENTICATION_BACKENDS += (
      'shibboleth.backends.ShibbolethRemoteUserBackend',
    )
    ```
  * Add the Django Shibboleth middleware.
    You must add the django.contrib.auth.middleware.ShibbolethRemoteUserMiddleware to the MIDDLEWARE_CLASSES setting after the django.contrib.auth.middleware.AuthenticationMiddleware.
    For example:
    ```python
    MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
    ...
    )
    ```

  * Define the shibboleth user key. This is the shibboleth attribute that is used to identify the user. It becomes the user name in django.
    ```python
    SHIBBOLETH_USER_KEY='<shibboleth-attribute>'
    ```
	
  * Map Shibboleth attributes to Django User model attributes via `SHIBBOLETH_ATTRIBUTE_LIST`. The exsting attributes [can be found in the django documentation](https://docs.djangoproject.com/en/1.7/ref/contrib/auth/#user). You might want to extend them via inheritance. 

  ```
   SHIBBOLETH_ATTRIBUTE_LIST= [
    {
      "shibboleth_key": "<name of shibboleth attribute>",
      "user_attribute" : "<name of User model attribute>",
      "required" : <True or false>
    },
    {
      "shibboleth_key": "shib_user_email",
      "user_attribute" : "email",
      "required" : True
    },
    ...
  ]
  ```

  Note: The Django user object has not many attributes. Note that all shibboleth attributes will be accessible in django via  the `META` dictionary in the `request` object. 

  * Login and Logout url - set this to the login/Logout handler of your shibboleth installation. 
    In most cases, this will be something like:

    ```python
    SHIBBOLETH_LOGIN_URL = 'https://your_domain.edu/Shibboleth.sso/Login'
    SHIBBOLETH_LOGOUT_URL = 'https://your_domain.edu/Shibboleth.sso/Logout'
   ```
  * Set the django `LOGIN_URL` to the login-view provided by this package:
   
     ```python
     LOGIN_URL = '/shib/login/'
     ```
     You can also manually set this this url in your templates. It is necessary to specify a redirect location using the url parameter `next`.

  * You can try to set the SHIBBOLETH_LOGOUT_REDIRECT_URL which defines where the user will be redirected after logout. You identity provider might ignore this setting.

 * Apache configuration - make sure the shibboleth attributes are available to the app.  The shibboleth variables are passed into the HttpRequest.META dictionary via wsgi.

    ```
    <Location /app>
      AuthType shibboleth
      Require shibboleth
    </Location>
    ```

Verify configuration
--------
If you would like to verify that everything is configured correctly, follow the next two steps below.  It will create a route in your application at /yourapp/shib/ that echos the attributes obtained from Shibboleth.  If you see the attributes you mapped above on the screen, all is good.  
 * Add shibboleth to installed apps.

    ```python
    INSTALLED_APPS += (
      'shibboleth',
    )
    ```

 * Add below to urls.py to enable the included sample view.  This view just echos back the parsed user attributes, which can be helpful for testing.

    ```python
    urlpatterns += patterns('',
      url(r'^shib/', include('shibboleth.urls', namespace='shibboleth')),
    )
    ```

##Optional
###Template tags
 * Template tags are included which will allow you to place {{ login_link }} or {{ logout_link }} in your templates for routing users to the login or logout page.  These are available as a convenience and not required.  To activate add the following to settings.py.

   ```python
    TEMPLATE_CONTEXT_PROCESSORS += (
       'shibboleth.context_processors.login_link',
       'shibboleth.context_processors.logout_link'
    )
   ```


