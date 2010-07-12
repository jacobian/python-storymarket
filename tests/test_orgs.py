from __future__ import absolute_import

from storymarket import Org
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api

sm = FakeStorymarket()

def test_list_orgs():
    assert_list_api(sm, sm.orgs.all, Org, 'orgs/')

def test_get_org():
    assert_get_api(sm, sm.orgs.get, Org, 'orgs/1/')