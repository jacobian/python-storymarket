from __future__ import absolute_import

from nose.tools import assert_raises, assert_equal
from storymarket import Category
from .fakeserver import FakeStorymarket
from .utils import assert_isinstance

sm = FakeStorymarket()

def test_list_categories():
    cl = sm.categories.all()
    sm.assert_called('GET', 'content/category/')
    [assert_isinstance(c, Category) for c in cl]
    
def test_list_subcategories():
    cl = sm.subcategories.all()
    sm.assert_called('GET', 'content/sub_category/')
    [assert_isinstance(c, Category) for c in cl]
    
def test_get_category():
    c = sm.categories.get(1)
    sm.assert_called('GET', 'content/category/1/')
    assert_isinstance(c, Category)
    c = sm.categories.get(Category(None, {'id': 1}))
    sm.assert_called('GET', 'content/category/1/')
    assert_isinstance(c, Category)
    
def test_get_subcategory():
    c = sm.subcategories.get(1)
    sm.assert_called('GET', 'content/sub_category/1/')
    assert_isinstance(c, Category)
    c = sm.subcategories.get(Category(None, {'id': 1}))
    sm.assert_called('GET', 'content/sub_category/1/')
    assert_isinstance(c, Category)
    
