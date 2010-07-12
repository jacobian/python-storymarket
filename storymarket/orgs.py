"""
Organizations.
"""

from __future__ import absolute_import

from . import base

class Org(base.Resource):
    def __repr__(self):
        return "<Org: %s>" % self.name
        
class OrgManager(base.Manager):
    resource_class = Org

    def all(self):
        """
        Get a list of all orgs.

        :rtype: list of org instances.
        """
        return self._list('/orgs/')

    def get(self, resource):
        """
        Get an individual org.

        :param resource: The org instance or its ID.
        :rtype: A list of org instances.
        """
        return self._get('/orgs/%s/' % base.getid(resource))