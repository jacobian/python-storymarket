class StorymarketError(Exception):
    def __init__(self, code, message=None, details=None):
        self.code = code
        self.msg = message or self.__class__.__name__
        self.details = details
        
    def __str__(self):
        return "%s (HTTP %s)" % (self.msg, self.code)

class StorymarketObjectDoesNotExist(StorymarketError):
    http_status = 404

_code_map = dict((c.http_status, c) for c in StorymarketError.__subclasses__())

def from_response(response, body):
    """
    Return an instance of a StorymarketError or subclass
    based on an httplib2 response. 
    
    Usage::
    
        resp, body = http.request(...)
        if resp.status != 200:
            raise exception_from_response(resp, body)
    """
    cls = _code_map.get(response.status, StorymarketError)
    if body:
        return cls(code=response.status, message=body)
    else:
        return cls(code=response.status)