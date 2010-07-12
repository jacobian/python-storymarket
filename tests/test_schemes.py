from __future__ import absolute_import

from nose.tools import assert_raises, assert_equal
from storymarket import PricingScheme, RightsScheme
from .fakeserver import FakeStorymarket
from .utils import assert_isinstance

sm = FakeStorymarket()

def test_list_pricing_schemes():
    _test_list(PricingScheme, sm.pricing, 'pricing/')

def test_list_rights_schemes():
    _test_list(RightsScheme, sm.rights, 'rights/')

def test_get_pricing_scheme():
    _test_get(PricingScheme, sm.pricing, 'pricing/1/')
    
def test_get_rights_scheme():
    _test_get(RightsScheme, sm.rights, 'rights/1/')

def _test_list(cls, manager, url):
    scheme_list = manager.all()
    sm.assert_called('GET', url)
    for scheme in scheme_list:
        assert_isinstance(scheme, cls)

def _test_get(cls, manager, url):
    # Test get(id)
    scheme = manager.get(1)
    sm.assert_called('GET', url)
    assert_isinstance(scheme, cls)

    # Test get(instance)
    scheme = manager.get(cls(None, {'id': 1}))
    sm.assert_called('GET', url)
    assert_isinstance(scheme, cls)
