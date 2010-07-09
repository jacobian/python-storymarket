"""
API classes for categories and subcategories.
"""

from __future__ import absolute_import

from . import base

class Category(base.Resource):
    """
    A category or sub-category.
    """
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)
        
class CategoryManager(base.Resource):
    """
    Manage categories.
    """
    resource_class = Category
    urlbit = 'category'
    
    def all(self):
        """
        Get a list of all categories.

        :rtype: A list of category instances.
        """
        return self._list('/content/%s/' % self.urlbit)
        
    def get(self, resource):
        """
        Get an individual category.
        
        :param resource: The resource instance or its ID.
        :rtype: A list of category instances.
        """
        return self._get('/content/%s/%s/' % (self.urlbit, base.getid(resource)))
        
class SubcategoryManager(CategoryManager):
    urlbit = 'sub_category'
        