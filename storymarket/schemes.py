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
        
class PricingSchemeManager(base.Resource):
    resource_class = PricingScheme
    
    def all(self):
        """
        Get a list of all pricing schemes.
        
        :rtype: list of :class:`PricingScheme`` resources.
        """
        return self._list('/pricing/')
        
    def get(self, id):
        """
        Get an individual pricing scheme.
        
        :rtype: a :class:`PricingScheme` resource.
        """
        return self._get('/pricing/%s/' % id)
        
class RightsScheme(base.Resource):
    """
    A rights scheme for content.
    """
    def __repr__(self):
        return "<RightsScheme: %s>" % self.name
        
class RightsSchemeManager(base.Resource):
    resource_class = RightsScheme
    
    def all(self):
        """
        Get a list of all rights schemes.
        
        :rtype: list of :class:`RightsScheme`` resources.
        """
        return self._list('/rights/')
        
    def get(self, id):
        """
        Get an individual rights scheme.
        
        :rtype: a :class:`RightsScheme` resource.
        """
        return self._get('/rights/%s/' % id)
