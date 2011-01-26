import httplib2
import urlparse
import urllib
import storymarket
from . import exceptions

try:                                # pragma: no cover
    import json
except ImportError:                 # pragma: no cover
    import simplejson as json
    
class StorymarketClient(httplib2.Http):
    
    USER_AGENT = 'python-storymarket/%s' % storymarket.__version__
    BASE_URL = 'https://www.storymarket.com/api/v1/'
    
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
        
        if resp.status in (400, 401, 403, 404, 405, 406, 413, 500):
            raise exceptions.from_response(resp, body)
            
        return resp, body
    
    def _storymarket_request(self, url, method, *args, **kwargs):
        """Real request method for mocking and testing."""
        # Encode the body as JSON unless otherwise specified
        if 'body' in kwargs:
            ctype = kwargs['headers'].setdefault('Content-Type', 'application/json')
            if ctype == 'application/json':
                kwargs['body'] = json.dumps(kwargs['body'])

        resp, body = super(StorymarketClient, self).request(url, method, *args, **kwargs)

        # Automatically decode the response body from JSON. We can't do this
        # unconditionally: if there's a redirect chain then self.request() may
        # have been called more than once recursively and may have already
        # decoded the response body. So we have to do a nasty isinstance().
        if isinstance(body, basestring):
            try:
                body = json.loads(body) if body else None
            except ValueError:
                # Raised by simplejson if the body can't be decoded.
                # This will be accompanied by an error status, which'll get 
                # raised by request(), above, so skip it.
                pass

        return resp, body
    
    def get(self, url, **kwargs):
        return self.request(url, 'GET', **kwargs)
    
    def post(self, url, **kwargs):
        return self.request(url, 'POST', **kwargs)
    
    def put(self, url, **kwargs):
        return self.request(url, 'PUT', **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request(url, 'DELETE', **kwargs)
    
