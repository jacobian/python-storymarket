from . import base

class Link(object):
    """
    A link object from one resource to another.
    
    Links in the Storymarket API are represented as dicts::
    
        {"rel": "self",
         "href": "/foo/bar/",
         "allowed_methods": ["GET"]}

    This encapsulates them as an object.
    """
    def __init__(self, rel, href, allowed_methods):
        self.rel = rel
        self.href = href
        self.allowed_methods = allowed_methods
        
    def __str__(self):
        return self.href
        
    def __repr__(self):
        return "<Link rel=%r href=%r>" % (self.rel, self.href)
        
    def __eq__(self, other):
        return isinstance(other, Link) and self.__dict__ == other.__dict__

class LinkedResource(base.Resource):
    """
    A Resource subclass that provides `self.links`.
    """
    def _add_details(self, info):
        # Create self.links, and also remove info.links so that
        # it doesn't overwrite our new version..
        self.links = {}
        for link in info.pop('links', []):
            link_obj = Link(rel=link['rel'], href=link['href'],
                            allowed_methods=link['allowed_methods'])
            self.links[link['rel']] = link_obj
        super(LinkedResource, self)._add_details(info)
    
