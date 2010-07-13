"""
API classes for pricing and rights schemes.
"""

from __future__ import absolute_import

from . import base
from . import links

class BaseSchemeResource(links.LinkedResource):
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

class PricingScheme(BaseSchemeResource):
    """
    A pricing scheme for content.
    """
    pass

class RightsScheme(BaseSchemeResource):
    """
    A rights scheme for content.
    """
    pass
    
class BaseSchemeManager(base.Manager):
    def all(self):
        """
        Get a list of all schemes.
        
        :rtype: list of scheme resources.
        """
        return self._list('/%s/' % self.urlbit)
        
    def get(self, resource):
        """
        Get an individual scheme.

        :param resource: The scheme instance or its ID.
        :rtype: A list of scheme instances.
        """
        return self._get('/%s/%s/' % (self.urlbit, base.getid(resource)))
   
class PricingSchemeManager(BaseSchemeManager):
    resource_class = PricingScheme
    urlbit = 'pricing'
        
class RightsSchemeManager(BaseSchemeManager):
    resource_class = RightsScheme
    urlbit = 'rights'