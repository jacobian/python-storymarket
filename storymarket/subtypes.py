"""
API classes for subtypes.
"""

from __future__ import absolute_import
from urllib import urlencode
from . import base
from . import links


class Subtype(links.LinkedResource):
    """
    A  sub-type.
    """
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)
        
class SubtypeManager(base.Manager):
    """
    Manage subtypes.
    """
    resource_class = Subtype
    urlbit = 'sub_type'
    
    def all(self):
        """
        Get a list of all subtypes.

        :rtype: A list of subtype instances.
        """
        return self._list('/content/%s/' % self.urlbit)

    def filter(self, *args, **kwargs):
        """
        Get a list of subtypes filtered by content type.

        :param type__model: (optional) Filters by content type name, eg: 'text','photo','video', ecc.
        :param is_default: (optional) (Bool): Filters by is_default attribute.
        :rtype: A list of subtype instances.
        """
        return self._list('/content/%s/?%s' % (self.urlbit, urlencode(kwargs)))

    def get(self, resource):
        """
        Get an individual subtype.
        
        :param resource: The resource instance or its ID.
        :rtype: A list of subtype instances.
        """
        return self._get('/content/%s/%s/' % (self.urlbit, base.getid(resource)))
