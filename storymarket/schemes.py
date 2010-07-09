"""
API classes for pricing and rights schemes.
"""

from __future__ import absolute_import

from . import base

class PricingScheme(base.Resource):
    """
    A pricing scheme for content.
    """
    def __repr__(self):
        return "<PricingScheme: %s>" % self.name
        
class PricingSchemeManager(base.Manager):
    resource_class = PricingScheme
    
    def all(self):
        """
        Get a list of all pricing schemes.
        
        :rtype: list of :class:`PricingScheme`` resources.
        """
        return self._list('/pricing/')
        
    def get(self, resource):
        """
        Get an individual pricing scheme.

        :param resource: The pricing scheme instance or its ID.
        :rtype: A list of pricing scheme instances.
        """
        return self._get('/pricing/%s/' % (self.urlbit, base.getid(resource)))
        
class RightsScheme(base.Resource):
    """
    A rights scheme for content.
    """
    def __repr__(self):
        return "<RightsScheme: %s>" % self.name
        
class RightsSchemeManager(base.Manager):
    resource_class = RightsScheme
    
    def all(self):
        """
        Get a list of all rights schemes.
        
        :rtype: list of :class:`RightsScheme`` resources.
        """
        return self._list('/rights/')
        
    def get(self, resource):
        """
        Get an individual rights scheme.

        :param resource: The rights scheme instance or its ID.
        :rtype: A list of rights scheme instances.
        """
        return self._get('/rights/%s/' % (self.urlbit, base.getid(resource)))

