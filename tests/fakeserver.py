"""
A fake server that "responds" to methods with pre-canned results.
"""

from __future__ import with_statement
from __future__ import absolute_import

import httplib2
import urllib
import urlparse
from os.path import splitext
from storymarket import Storymarket
from storymarket.client import StorymarketClient
from nose.tools import assert_equal
from .utils import fail, assert_in, assert_not_in, assert_has_keys

class FakeStorymarket(Storymarket):
    def __init__(self, apikey=None):
        super(FakeStorymarket, self).__init__('apikey')
        self.client = FakeClient()

    def assert_called(self, method, url, body=None):
        """
        Assert than an API method was just called.
        """
        expected = (method, url)
        called = self.client.callstack[-1][0:2]
        assert self.client.callstack, "Expected %s %s but no calls were made." % expected
        assert expected == called, 'Expected %s %s; got %s %s' % (expected + called)
        if body is not None:
            assert_equal(self.client.callstack[-1][2], body)

class FakeClient(StorymarketClient):
    def __init__(self):
        self.apikey = 'apikey'
        self.callstack = []
        
    def _storymarket_request(self, url, method, *args, **kwargs):
        # Check that certain methods are called correctly
        if method in ['GET', 'DELETE']:
            assert_not_in('body', kwargs)
        elif method in ['PUT', 'POST']:
            assert_in('body', kwargs)
        
        # Make sure the authorization header got set correctly
        assert_equal(kwargs['headers']['Authorization'], self.apikey)
        
        # Call a method on self instead
        _, _, path_prefix, _, _ = urlparse.urlsplit(self.BASE_URL)
        munged_path = splitext(path.replace(path_prefix, ''))[0].strip('/').replace('/', '_')
        callback = "%s_%s" % (method.lower(), munged_path)
        if not hasattr(self, callback):
            fail('Called unknown API method: %s %s' % (method, url))
        
        # Note the call. To make comparisons easier in testing easy, we'll
        # sort the GET kwargs by name.
        called_url = "/%s" % path.replace(path_prefix, '')
        if query:
            sorted_qs = urllib.urlencode(sorted(urlparse.parse_qsl(query)))
            called_url = '%s?%s' % (called_url, sorted_qs)
        self.callstack.append((method, called_url, kwargs.get('body', None)))
        
        status, body = getattr(self, callback)(**kwargs)
        return httplib2.Response({"status": status}), body
        