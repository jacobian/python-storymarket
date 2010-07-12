"""
API classes for content (text, data, autdio, video, packages) resources.
"""

from __future__ import absolute_import

from . import base
from .schemes import PricingScheme, RightsScheme
from .orgs import Org
from .categories import Category

class User(base.Resource):
    """
    A user object.
    
    Not actually a resource, but used in lieu of the raw dict of user info.
    """
    def __init__(self, info):
        # Make sure User(some_other_user) works
        if isinstance(info, self.__class__):
            info = info.__dict__
        
        self.username = info['username']
        self.first_name = info['first_name']
        self.last_name = info['last_name']
        self.email = info['email']
    
    def __repr__(self):
        return "<User: %s>" % self.username
        
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.username == other.username
        
class ContentResource(base.Resource):
    """
    Abstract base class for content resources.
    """
    
    def _add_details(self, info):
        # So that related objects can be properties, save their info under.
        # slightly different names.
        for k in ('author', 'category', 'org', 'pricing_scheme', 'rights_scheme', 'uploaded_by'):
            if k in info:
                info['_%s' % k] = info.pop(k)
        super(ContentResource, self)._add_details(info)
    
    @property
    def author(self):
        return User(self._author)

    @property
    def category(self):
        return Category(self.manager.api.subcategories, self._category)

    @property
    def org(self):
        return Org(self.manager.api.orgs, self._org)

    @property
    def pricing_scheme(self):
        return PricingScheme(self.manager.api.pricing, self._pricing)

    @property
    def rights_scheme(self):
        return RightsScheme(self.manager.api.rights, self._rights_scheme)
        
    @property
    def uploaded_by(self):
        return User(self._uploaded_by)
    
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.title)
    
    def delete(self):
        """
        Delete this resource.
        """
        self.manager.delete(self)
        
    def save(self):
        """
        Save changes to this resource by PUTing it back to the server.
        """
        self.manager.update(self)

    # @property
    # def links(self):
    #     raise NotImplementedError # TODO

class ContentManager(base.Manager):
    """
    Abstract base manager for content resources.
    """
    # Subclasses should set this to the bit of the URL that differs --
    # that is: /content/{urlbit}/
    urlbit = None
    
    def all(self):
        """
        Get a list of all content resources of this type.
        
        :rtype: A list of instances of apropriate ``ContentResource`` subclasses
                (e.g. ``Audio``, ``Video``, etc.)
        """
        return self._list('/content/%s/' % self.urlbit)
        
    def get(self, resource):
        """
        Get a single content resource of this type.
        
        :param resource: The resource instance or its ID.
        :rtype: An instance of an apropriate ``ContentResource`` subclass
                (e.g. ``Audio``, ``Video``, etc.)
        """
        return self._get('/content/%s/%s/' % (self.urlbit, base.getid(resource)))
    
    def delete(self, resource):
        """
        Delete a resource of this type.
        
        :param resource: The resource instance or its ID.
        :rtype: None
        """
        return self._delete('/content/%s/%s/' % (self.urlbit, base.getid(resource)))
    
    def create(self, resource):
        """
        Create a new resource of this type.
        
        :param resource: The resource to create (as a class or dict)
        :rtype: The created resource class.
        """
        # FIXME: use the simplified PUT/POST representation
        body = getattr(resource, '_info', resource)
        return self._create('/content/%s/' % self.urlbit, body)
        
    def update(self, resource):
        """
        Update an existing resource.
        
        :param resource: The resource instance or its ID.
        :rtype: None
        """
        # FIXME: use the simplified PUT/POST representation
        url = '/content/%s/%s/' % (self.urlbit, base.getid(resource))
        body = getattr(resource, '_info', resource)
        return self._update(url, body)

class BinaryContentResource(ContentResource):
    """
    Abstract base class for content resources that have associated binary blobs
    (Audio, Video, etc.)
    """
    def upload_blob(self, blob):
        """
        Upload a new blob for this resource.
        
        :param blob: A string of file-like object to upload.
        :rtype: None
        """
        self.manager.upload_blog(self, blob)

class BinaryContentManager(ContentManager):
    """
    Abstract base class for content resources that have associated binary
    content (Audio, Video, etc.).
    """
    
    def upload_blob(self, resource, blob):
        """
        Upload a new blob for a given resource.
        
        :param resource: The resource object or its ID to upload a blob to.
        :param blob: A string of file-like object to upload.
        :rtype: None
        """
        raise NotImplementedError # TODO

class Audio(BinaryContentResource):
    "An audio resource."
    pass
    
class Data(BinaryContentResource): 
    "A data resource."
    pass
    
class Photo(BinaryContentResource):
    "A photo resource."
    pass

class Text(ContentResource):
    "A text resource."
    pass
    
class Video(BinaryContentResource):
    "A video resource."
    pass

# TODO: packages

class AudioManager(BinaryContentManager):
    "Manager for audio resources."
    resource_class = Audio
    urlbit = 'audio'
    
class DataManager(BinaryContentManager):
    "Manager for data resources."
    resource_class = Data
    urlbit = 'data'
    
class PhotoManager(BinaryContentManager):
    "Manager for photo resources."
    resource_class = Photo
    urlbit = 'photo'

class TextManager(ContentManager):
    "Manager for text resources."
    resource_class = Text
    urlbit = 'text'

class VideoManager(BinaryContentManager):
    "Manager for video resources."
    resource_class = Video
    urlbit = 'video'