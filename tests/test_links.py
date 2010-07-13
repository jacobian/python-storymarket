from __future__ import absolute_import

from nose.tools import assert_equal, assert_not_equal, assert_raises
from storymarket.links import Link
from .fakeserver import FakeStorymarket
from .utils import assert_isinstance

sm = FakeStorymarket()

def test_links_attribute():
    o = sm.orgs.get(1)
    assert_isinstance(o.links["self"], Link)
    assert_raises(KeyError, o.links.__getitem__, "badrel")
    
def test_links_repr():
    l = Link(rel="self", href="/foo", allowed_methods=['GET'])
    assert_equal(str(l), "/foo")
    assert_equal(repr(l), "<Link rel='self' href='/foo'>")
    
def test_links_eq():
    l1 = Link(rel="self", href="/foo", allowed_methods=['GET'])
    l2 = Link(rel="self", href="/bar", allowed_methods=['GET'])
    l3 = Link(rel="self", href="/bar", allowed_methods=['POST'])
    l4 = Link(rel="self", href="/foo", allowed_methods=["GET"])
    
    assert_equal(l1, l1)
    assert_equal(l1, l4)
    assert_not_equal(l1, l2)
    assert_not_equal(l1, l3)
    assert_not_equal(l2, l3)
    