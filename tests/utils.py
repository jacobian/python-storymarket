from nose.tools import ok_

def fail(msg):
    raise AssertionError(msg)

def assert_in(thing, seq, msg=None):
    msg = msg or "'%s' not found in %s" % (thing, seq)
    ok_(thing in seq, msg)
    
def assert_not_in(thing, seq, msg=None):
    msg = msg or "unexpected '%s' found in %s" % (thing, seq)
    ok_(thing not in seq, msg)
    
def assert_has_keys(dict, required=[], optional=[]):
    keys = dict.keys()
    for k in required:
        assert_in(k, keys, "required key %s missing from %s" % (k, dict))
    allowed_keys = set(required) | set(optional)
    extra_keys = set(keys).difference(set(required + optional))
    if extra_keys:
        fail("found unexpected keys: %s" % list(extra_keys))
    
def assert_isinstance(thing, kls):
    ok_(isinstance(thing, kls), "%s is not an instance of %s" % (thing, kls))
    
def assert_list_api(api, api_method, expected_class, expected_url):
    """
    Call an API list method, asserting that the returned class is correct
    and that the called URL was correct.
    
    :param api: An instance of the fake API server (so that assert_called can be used).
    :param api_method: The API method to call.
    :param expected_class: Assert that returned instances are of this class.
    :param expected_url: Assert that this URL was called with GET.
    """
    resource_list = api_method()
    api.assert_called('GET', expected_url)
    for resource in resource_list:
        assert_isinstance(resource, expected_class)

def assert_get_api(api, api_method, expected_class, expected_url, resource_id=1):
    """
    Call an API get method, asserting that the returned class is correct and
    that the called URL was correct.
    
    :param api: An instance of the fake API server (so that assert_called can be used).
    :param api_method: The API method to call.
    :param expected_class: Assert that the returned instance is of this class.
    :param expected_url: Assert that this URL was called with GET.
    :param resource_id: The ID of the resource to try GETing.
    """
    # Test get(id)
    resource = api_method(resource_id)
    api.assert_called('GET', expected_url)
    assert_isinstance(resource, expected_class)

    # Test get(instance)
    resource = api_method(expected_class(None, {'id': resource_id}))
    api.assert_called('GET', expected_url)
    assert_isinstance(resource, expected_class)
