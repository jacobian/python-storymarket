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
    
def assert_list_api(api, api_method, expected_class, expected_url, kw={}):
    """
    Call an API list method, asserting that the returned class is correct
    and that the called URL was correct.
    
    :param api: An instance of the fake API server (so that assert_called can be used).
    :param api_method: The API method to call.
    :param expected_class: Assert that returned instances are of this class.
    :param expected_url: Assert that this URL was called with GET.
    """
    resource_list = api_method(**kw)
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
    
def assert_delete_api(api, api_method, expected_class, expected_url, resource_id=1):
    """
    Call an API delete method, asserting that the returned class is correct and
    that the called URL was correct.
    
    :param api: An instance of the fake API server (so that assert_called can be used).
    :param api_method: The API method to call.
    :param expected_class: Assert that the returned instance is of this class.
    :param expected_url: Assert that this URL was called with DELETE.
    :param resource_id: The ID of the resource to try DELETEing.
    """
    # Test get(id)
    api_method(resource_id)
    api.assert_called('DELETE', expected_url)

    # Test get(instance)
    api_method(expected_class(None, {'id': resource_id}))
    api.assert_called('DELETE', expected_url)

def assert_create_api(api, api_method, instance, post_data, expected_url):
    """
    Call an API create method, asserting that the returned class is
    correct and that the called URL was correct.
    
    :param api: An instance of the fake API server (so that assert_called can be used).
    :param api_method: The API method to call.
    :param instance: The resource instance that should be created.
    :param expected_class: Assert that the returned instance is of this class.
    :param expected_url: The URL we'd expected to be POSTed to.
    """
    # Try POSTing with raw data
    resp = api_method(post_data)
    api.assert_called('POST', expected_url)
    assert_isinstance(resp, instance.__class__)
    
    # And now with an instance instead
    resp = api_method(instance)
    api.assert_called('POST', expected_url)
    assert_isinstance(resp, instance.__class__)
    
def assert_update_api(api, api_method, instance, post_data, expected_url, resource_id=1):
    """
    Call an API update method, asserting that the returned class is
    correct and that the called URL was correct.

    :param api: An instance of the fake API server (so that assert_called can be used).
    :param api_method: The API method to call.
    :param instance: The resource instance that should be updated.
    :param post_data: The data to use for a POST.
    :param expected_url: The URL we'd expected to be POSTed to.
    """
    # PUT raw data
    api_method(instance, post_data)
    api.assert_called('PUT', expected_url)

    # PUT an instance and post_data
    api_method(instance, instance)
    api.assert_called('PUT', expected_url)
    
    # PUT just a new instance
    api_method(instance)
    api.assert_called('PUT', expected_url)
