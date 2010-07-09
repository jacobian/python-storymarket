"""
A fake server that "responds" to methods with pre-canned results.
"""

from __future__ import with_statement
from __future__ import absolute_import

import httplib2
from storymarket import Storymarket
from storymarket.client import StorymarketClient
from nose.tools import assert_equal
from .utils import fail, assert_in, assert_not_in

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
        
        # Call the method
        munged_url = url.strip('/').replace('/', '_').replace('.', '_')
        callback = "%s_%s" % (method.lower(), munged_url)
        if not hasattr(self, callback):
            fail('Called unknown API method: %s %s' % (method, url))
        
        # Note the call
        self.callstack.append((method, url, kwargs.get('body', None)))
        
        status, body = getattr(self, callback)(**kwargs)
        return httplib2.Response({"status": status}), body
    
    def get_content_category(self, **kw):
        return [self.get_content_category_1()]
    
    def get_content_category_1(self, **kw):
        return {
            "name": "Technology", 
            "links": [], # FIXME
            "description": "Tech!"
        },
    
    get_content_sub_category = get_content_category
    get_content_sub_category_1 = get_content_category_1
    
    def get_content_data(self, **kw):
        return [self.get_content_data_1()]
        
    def get_content_data_1(self, **kw):
        return self._content_dict(title='Data',
                                  data='http://example.com/datas/2010/05/14/revsys.ppt')
    
    def get_content_audio(self, **kw):
        return [self.get_content_audio_1()]
        
    def get_content_audio_1(self, **kw):
        return self._content_dict(title='Audio',
                                  audio="http://example.com/audios/2010/05/14/revsys.avi")
    
    def get_orgs(self, **kw):
        return [self.get_orgs_1()]
    
    def get_orgs_1(self, **kw):
        return {"name": "Test Org", "links": []}        
    
    def get_content_photo(self, **kw):
        return [self.get_content_photo_1()]
        
    def get_content_photo_1(self, **kw):
        return self._content_dict(title='Photo',
                                  photo='http://eample.com/photos/2010/05/15/cat.jpg')
    
    def get_pricing(self, **kw):
        return [self.get_pricing_1()]
        
    def get_pricing_1(self, **kw):
        return {
            "default_for_audio": False, 
            "default_for_data": False, 
            "name": "Default Pricing", 
            "links": [],
            "default": True, 
            "org_prices": [], 
            "base_price_small": None, 
            "default_for_package": False, 
            "base_price": "10.00", 
            "base_price_medium": None, 
            "base_price_large": None, 
            "default_for_video": False, 
            "default_for_text": False, 
            "org": self.get_orgs_1(), 
            "default_for_photo": False, 
            "group_prices": [], 
            "description": ""
        }
    
    def get_rights(self, **kw):
        return [self.get_rights_1()]
        
    def get_rights_1(self, **kw):
        return {
            "other_limitations": "", 
            "name": "Public", 
            "links": [],
            "default": False, 
            "tv_only": False, 
            "online_only": False, 
            "included_states": [], 
            "print_only": False, 
            "org": self.get_orgs_1(), 
            "exclude": True, 
            "include": False, 
            "excluded_states": [], 
            "public": True, 
            "description": ""
        }, 
    
    def get_content_text(self, **kw):
        return [self.get_content_text_1()]
    
    def get_content_text_1(self, **kw):
        return self._content_dict(title='Text', content='lorum ipsum...')
    
    def get_content_video(self, **kw):
        return [self.get_content_video_1()]
        
    def get_content_video_1(self, **kw):
        return self._content_dict(title='Video',
                                  photo='http://eample.com/photos/2010/05/15/cat.mov')
    
    def _content_dict(self, **kw):
        """Helper to generate content objects"""
        d = {
            "category": self.get_content_subcategory_1(),
            "uploaded_by": {
                "username": "frank", 
                "first_name": "Frank", 
                "last_name": "Wiles", 
                "email": "frank@revsys.com"
            }, 
            "description": "", 
            "links": [], #FIXME
            "title": "Test resource", 
            "author": {
                "username": "frank", 
                "first_name": "Frank", 
                "last_name": "Wiles", 
                "email": "frank@revsys.com"
            }, 
            "duration": 57,
            "one_off_author": "", 
            "tags": ['hi', 'there'], 
            "expire_date": "2011-05-14 14:59:28", 
            "fact_checked": False, 
            "org": self.get_orgs_1(), 
            "rights_scheme": self.get_rights_1(),
            "pricing_scheme": self.get_pricing_1(),
            "size": 2123
        }
        d = d.copy()
        d.update(kw)
        return d
