"""
Base utilities to build API operation managers and objects on top of.
"""
class Manager(object):
    """
    Managers interact with a particular type of resource and provide CRUD
    operations for them.
    """
    resource_class = None
    
    def __init__(self, api):
        self.api = api

    def _list(self, url, response_key=None):
        resp, body = self.api.client.get(url)
        if body:
            if response_key: 
                body = (res[response_key] for res in body)
            return [self.resource_class(self, res) for res in body]
        return body
    
    def _get(self, url, response_key=None):
        resp, body = self.api.client.get(url)
        if response_key:
            return self.resource_class(self, body[response_key])
        else:
            return self.resource_class(self, body)
    
    def _create(self, url, body, response_key=None):
        resp, body = self.api.client.post(url, body=body)
        if response_key:
            return self.resource_class(self, body[response_key])
        else:
            return self.resource_class(self, body)
        
    def _delete(self, url):
        resp, body = self.api.client.delete(url)
    
    def _update(self, url, body):
        resp, body = self.api.client.put(url, body=body)
                    
class Resource(object):
    """
    A resource represents a particular instance of a resource.
    
    It's pretty much just a bag for attributes.
    """
    def __init__(self, manager, info):
        self.manager = manager
        self._info = info
        self._add_details(info)
        
    def _add_details(self, info):
        for (k, v) in info.iteritems():
            setattr(self, k, v)
            
    def __getattr__(self, k):
        self.get()
        if k not in self.__dict__:
            raise AttributeError(k)
        else:
            return self.__dict__[k]
            
    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys() if k[0] != '_' and k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    def get(self):
        new = self.manager.get(self.id)
        self._add_details(new._info)
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id
        return self._info == other._info
        
def related_resource(cls, keyname):
    """
    Helper to create properties that access other Resource instances from a
    sub-dict on the resource.
    
    For example, if a ``Book`` resource returned data of the form::
    
        {
            'title': 'The Sun Also Rises',
            'author': {
                'first': 'Ernest',
                'last': 'Hemingway'
            }
        }
        
    You could make ``Book.author`` into a property that returned ``Author``
    resources thusly::
    
        class Book(Resource):
            ...
            
            author = related_resource(Author, 'author')
    
    This is just syntactic sugar for::
    
        class Book(Resource):
            ...
            
            @property
            def author(self):
                return Author(self.manager, self._info['author'])
    """
    # FIXME: self.manager is wrong - should be the resource class's manager.
    def getter(self):
        return cls(self.manager, self._info['author'])
    return property(getter)
    
def getid(obj):
    """
    Abstracts the common pattern of allowing both an object or an object's ID
    (integer) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return int(obj)