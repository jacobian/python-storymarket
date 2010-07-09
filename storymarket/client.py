import httplib2
import urlparse
import urllib
import storymarket
from . import exceptions
try:
    import json
except ImportError:
    import simplejson as json
    
class StorymarketClient(httplib2.Http):
    
    USER_AGENT = 'python-storymarket/%s' % storymarket.__version__
    BASE_URL = 'http://storymarket.com/api/v1/'
    
    def __init__(self, apikey):
        super(StorymarketClient, self).__init__()
        self.apikey = apikey
        self.force_exception_to_status_code = True
        
    def request(self, url, method, *args, **kwargs):
        url = urlparse.urljoin(self.BASE_URL, url.lstrip('/'))
                
        # Add User-Agent headers
        kwargs.setdefault('headers', {})
        kwargs['headers']['User-Agent'] = self.USER_AGENT
        
        # Add authorization header
        kwargs['headers']['Authorization'] = self.apikey
        
        resp, body = self._storymarket_request(url, method, *args, **kwargs)
        
        if resp.status in (400, 401, 403, 404, 406, 413, 500):
            raise exceptions.from_response(resp, body)
            
        return resp, body
    
    def _storymarket_request(self, url, method, *args, **kwargs):
        # Separate method for mocking and testing.
        resp, body = super(StorymarketClient, self).request(url, method, *args, **kwargs)
        body = json.loads(body) if body else None
        return resp, body
    
    def get(self, url, **kwargs):
        return self.request(url, 'GET', **kwargs)
    
    def post(self, url, **kwargs):
        return self.request(url, 'POST', **kwargs)
    
    def put(self, url, **kwargs):
        return self.request(url, 'PUT', **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request(url, 'DELETE', **kwargs)
    
