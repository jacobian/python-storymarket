from __future__ import absolute_import

from nose.tools import assert_raises, assert_equal
from storymarket import Category
from .fakeserver import FakeStorymarket
from .utils import assert_isinstance, assert_list_api, assert_get_api

sm = FakeStorymarket()

def test_list_categories():
    assert_list_api(sm, sm.categories.all, Category, 'content/category/')
    
def test_list_subcategories():
    assert_list_api(sm, sm.subcategories.all, Category, 'content/sub_category/')
    
def test_get_category():
    assert_get_api(sm, sm.categories.get, Category, 'content/category/1/')
    
def test_get_subcategory():
    assert_get_api(sm, sm.subcategories.get, Category, 'content/sub_category/1/')
