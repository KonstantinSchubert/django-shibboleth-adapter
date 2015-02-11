# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.utils import unittest
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.client import Client

SAMPLE_META = {
  "persistent-id": 'testid',
  "shib_user_email" :  'mail@test.com',
}

settings.SHIBBOLETH_USER_KEY = "persistent-id"
settings.SHIBBOLETH_ATTRIBUTE_LIST = [
    {
      "shibboleth_key": "shib_user_email",
      "user_attribute" : "email",
      "required" : True
    }
  ]
  

settings.AUTHENTICATION_BACKENDS += (
    'shibboleth.backends.ShibbolethRemoteUserBackend',
)

settings.MIDDLEWARE_CLASSES += (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
)

settings.ROOT_URLCONF = 'shibboleth.urls'


class AttributesTest(unittest.TestCase):
    def setUp(self):
        self.c = Client()

    def test_inheritance_middleware(self):
      from shibboleth.middleware import ShibbolethRemoteUserMiddleware
      middleware = ShibbolethRemoteUserMiddleware()
      assert hasattr(middleware, "_remove_invalid_user")
      assert hasattr(middleware, "clean_username")

        
    def test_decorator_not_authenticated(self):
        """
        """
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 302)
        #Test the context - shouldn't exist
        self.assertEqual(resp.context, None) 
        
    def test_decorator_authenticated(self):
        """
        """
        resp = self.c.get('/', **SAMPLE_META)
        self.assertEqual(resp.status_code, 200)
        #Test the context
        user = resp.context.get('user')
        # self.assertEqual(user.entitlement , 'urn:mace:dir:entitlement:common-lib-terms')
        self.assertTrue(user.is_authenticated())
        self.assertFalse(user.is_anonymous())
