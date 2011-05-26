from __future__ import absolute_import

from storymarket import Subtype
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api

sm = FakeStorymarket()

def test_list_subtypes():
    assert_list_api(sm, sm.sub_types.all, Subtype, 'content/sub_type/')
    
def test_filter_subtype():
    assert_list_api(sm, sm.sub_types.filter, Subtype, 'content/sub_type/?')

def test_get_subtype():
    assert_get_api(sm, sm.sub_types.get, Subtype, 'content/sub_type/1/')

