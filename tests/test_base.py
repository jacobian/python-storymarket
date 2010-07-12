from __future__ import absolute_import

from storymarket import Text
from storymarket.base import Resource
from .fakeserver import FakeStorymarket
from nose.tools import assert_equal, assert_not_equal, assert_raises

sm = FakeStorymarket()

def test_resource_repr():
    r = Resource(None, dict(foo="bar", baz="spam"))
    assert_equal(repr(r), "<Resource baz=spam, foo=bar>")
        
def test_resource_lazy_getattr():
    t = Text(sm.text, {'id': 1})
    assert_equal(t.title, 'Text')
    sm.assert_called('GET', 'content/text/1/')
    
    # Missing stuff still fails after a second get
    assert_raises(AttributeError, getattr, t, 'blahblah')
    sm.assert_called('GET', 'content/text/1/')

def test_eq():
    # Two resources of the same type with the same id: equal
    r1 = Resource(None, {'id':1, 'name':'hi'})
    r2 = Resource(None, {'id':1, 'name':'hello'})
    assert_equal(r1, r2)

    # Two resources of different types: never equal
    r1 = Resource(None, {'id': 1})
    r2 = Text(None, {'id': 1})
    assert_not_equal(r1, r2)

    # Two resources with no ID: equal if their info is equal
    r1 = Resource(None, {'name': 'joe', 'age': 12})
    r2 = Resource(None, {'name': 'joe', 'age': 12})
    assert_equal(r1, r2)