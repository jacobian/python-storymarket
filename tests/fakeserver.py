"""
A fake server that "responds" to methods with pre-canned results.
"""

from __future__ import with_statement
from __future__ import absolute_import

import httplib2
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
    BASE_URL = ''

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
        return (200, [self.get_content_category_1()[1]])
    
    def get_content_category_1(self, **kw):
        return (200, {
            u"id": 1,
            u"name": u"Technology", 
            u"links": [
                {u"rel": u"self",
                 u"href": u"content/category/1/",
                 u"allowed_methods": [u"GET"]},
            ],
            u"description": u"Tech!"
        })
    
    get_content_sub_category = get_content_category
    get_content_sub_category_1 = get_content_category_1
    
    def get_content_data(self, **kw):
        return (200, [self.get_content_data_1()[1]])
        
    def get_content_data_1(self, **kw):
        return (200, self._content_dict(u"data",
                                        title=u'Data',
                                        data=u'http://example.com/datas/2010/05/14/revsys.ppt'))
    
    def get_content_audio(self, **kw):
        return (200, [self.get_content_audio_1()[1]])
        
    def get_content_audio_1(self, **kw):
        return (200, self._content_dict(u"audio",
                                        title=u'Audio',
                                        audio=u"http://example.com/audios/2010/05/14/revsys.avi"))
    
    def get_orgs(self, **kw):
        return (200, [self.get_orgs_1()[1]])
    
    def get_orgs_1(self, **kw):
        return (200, {
            u"id": 1, 
            u"name": u"Test Org", 
            u"links": [
                {u"rel": u"self",
                 u"href": u"orgs/1/",
                 u"allowed_methods": [u"GET"]},
            ],
        })
    
    def get_content_photo(self, **kw):
        return (200, [self.get_content_photo_1()[1]])
        
    def get_content_photo_1(self, **kw):
        return (200, self._content_dict("photo",
                                        title='Photo',
                                        photo=u'http://eample.com/photos/2010/05/15/cat.jpg',
                                        caption=u'My cat'))
    
    def get_pricing(self, **kw):
        return (200, [self.get_pricing_1()[1]])
        
    def get_pricing_1(self, **kw):
        return (200, {
            u"id": 1,
            u"default_for_audio": False, 
            u"default_for_data": False, 
            u"name": u"Default Pricing", 
            u"links": [
                {u"rel": u"self",
                 u"href": u"pricing/1/",
                 u"allowed_methods": [u"GET"]},
            ],
            u"default": True, 
            u"org_prices": [], 
            u"base_price_small": None, 
            u"default_for_package": False, 
            u"base_price": u"10.00", 
            u"base_price_medium": None, 
            u"base_price_large": None, 
            u"default_for_video": False, 
            u"default_for_text": False, 
            u"org": self.get_orgs_1(), 
            u"default_for_photo": False, 
            u"group_prices": [], 
            u"description": u""
        })
    
    def get_rights(self, **kw):
        return (200, [self.get_rights_1()[1]])
        
    def get_rights_1(self, **kw):
        return (200, {
            u"id": 1,
            u"other_limitations": u"", 
            u"name": u"Public", 
            u"links": [
                {u"rel": u"self",
                 u"href": u"rights/1/",
                 u"allowed_methods": [u"GET"]},
            ],
            u"default": False, 
            u"tv_only": False, 
            u"online_only": False, 
            u"included_states": [], 
            u"print_only": False, 
            u"org": self.get_orgs_1(), 
            u"exclude": True, 
            u"include": False, 
            u"excluded_states": [], 
            u"public": True, 
            u"description": u""
        })
    
    def get_content_text(self, **kw):
        return (200, [self.get_content_text_1()[1]])
    
    def get_content_text_1(self, **kw):
        return (200, self._content_dict(u"text", title=u'Text', content=u'lorum ipsum...'))
    
    def get_content_video(self, **kw):
        return (200, [self.get_content_video_1()[1]])
        
    def get_content_video_1(self, **kw):
        return (200, self._content_dict(u"video",
                                        title=u'Video',
                                        photo=u'http://eample.com/photos/2010/05/15/cat.mov'))
    
    def _delete_method(self, **kw):
        assert_not_in('body', kw)
        return (200, None)
    
    delete_content_audio_1 = _delete_method
    delete_content_data_1 = _delete_method
    delete_content_photo_1 = _delete_method
    delete_content_text_1 = _delete_method
    delete_content_video_1 = _delete_method
    
    def _check_post_method(self, body, required=(), optional=()):
        assert_has_keys(body,
            required = required + ('org', 'category', 'title', ),
            optional = optional + ('author', 'one_off_author', 'fact_checked',
                                   'description', 'rights_scheme',
                                   'pricing_scheme', 'tags')
        )
        assert_equal(body['org'], '/orgs/1/')
        assert_equal(body['category'], '/content/sub_category/1/')
    
    def post_content_text(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('content',))
        return (201, self.get_content_text_1()[1])
        
    def post_content_photo(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('caption',))
        return (201, self.get_content_photo_1()[1])
                                            
    def post_content_audio(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('duration',))
        return (201, self.get_content_audio_1()[1])
    
    def post_content_video(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('duration',))
        return (201, self.get_content_video_1()[1])
        
    def post_content_data(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'])
        return (201, self.get_content_data_1()[1])
    
    def put_content_text_1(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('content',))
        return (200, None)
        
    def put_content_photo_1(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('caption',))
        return (200, None)
                                            
    def put_content_audio_1(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('duration',))
        return (200, None)
    
    def put_content_video_1(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'], required=('duration',))
        return (200, None)
        
    def put_content_data_1(self, **kw):
        assert_in('body', kw)
        self._check_post_method(kw['body'])
        return (200, None)
    
    def _blob_put(self, **kw):
        assert_in('body', kw)
        assert_in('headers', kw)
        headers = kw['headers']
        assert headers['Content-Type'].startswith('multipart/form-data')
        assert_in('Content-Length', headers)
        return (204, None)

    put_content_photo_1_blob = _blob_put
    put_content_audio_1_blob = _blob_put
    put_content_video_1_blob = _blob_put
    put_content_data_1_blob = _blob_put
    
    def _content_dict(self, type, **kw):
        """Helper to generate content objects"""
        d = {
            u"id": 1,
            u"category": self.get_content_sub_category_1()[1],
            u"uploaded_by": {
                u"username": u"frank", 
                u"first_name": u"Frank", 
                u"last_name": u"Wiles", 
                u"email": u"frank@revsys.com"
            }, 
            u"description": u"", 
            u"links": [
                {u"rel": u"self",
                 u"href": u"content/%s/1/" % type,
                 u"allowed_methods": [u"GET", u"POST", u"PUT", u"DELETE"]}
            ],
            u"title": u"Test resource", 
            u"author": {
                u"username": u"frank", 
                u"first_name": u"Frank", 
                u"last_name": u"Wiles", 
                u"email": u"frank@revsys.com"
            }, 
            u"duration": 57,
            u"one_off_author": u"", 
            u"tags": [u'hi', u'there'], 
            u"expire_date": u"2011-05-14 14:59:28", 
            u"fact_checked": False, 
            u"org": self.get_orgs_1()[1], 
            u"rights_scheme": self.get_rights_1()[1],
            u"pricing_scheme": self.get_pricing_1()[1],
            u"size": 2123
        }
        d = d.copy()
        d.update(kw)
        return d