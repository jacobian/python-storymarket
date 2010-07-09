from __future__ import absolute_import

import mock
import storymarket.exceptions
from nose.tools import assert_equal
from .utils import assert_isinstance

def test_exception_from_response():
    resp = mock.Mock()
    resp.status = 500
    # FIXME: what do error responses actually look like?
    exc = storymarket.exceptions.from_response(resp, {'errors':[{'message': 'Oops!'}]})
    assert_isinstance(exc, storymarket.exceptions.StorymarketError)
    assert_equal(str(exc), 'Oops! (HTTP 500)')
    
def test_exception_from_response_no_body():
    resp = mock.Mock()
    resp.status = 500
    exc = storymarket.exceptions.from_response(resp, None)
    assert_equal(str(exc), 'StorymarketError (HTTP 500)')
