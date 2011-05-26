from __future__ import absolute_import

from storymarket import Subtype
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api

sm = FakeStorymarket()

def test_list_subtypes():
    assert_list_api(sm, sm.sub_types.all, Subtype, 'content/sub_type/')
    
def test_filter_subtype_default():
    assert_list_api(sm, sm.sub_types.filter, Subtype, 'content/sub_type/?is_default=1', {'is_default':True})

def test_filter_subtype_nondefault():
    assert_list_api(sm, sm.sub_types.filter, Subtype, 'content/sub_type/?is_default=0', {'is_default':False})

def test_filter_subtype_type():
    assert_list_api(sm, sm.sub_types.filter, Subtype, 'content/sub_type/?type__model=text', {'type':'text'})

def test_get_subtype():
    assert_get_api(sm, sm.sub_types.get, Subtype, 'content/sub_type/1/')

