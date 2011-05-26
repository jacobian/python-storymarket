from __future__ import absolute_import

import mock
from nose.tools import assert_equal, assert_not_equal
from storymarket import (Audio, Data, Photo, Text, Video, Category, Subtype, Org,
                         PricingScheme, RightsScheme)
from storymarket.content import User, BinaryContentManager
from StringIO import StringIO
from .fakeserver import FakeStorymarket
from .utils import (assert_isinstance, assert_list_api, assert_get_api,
                    assert_delete_api, assert_create_api, assert_update_api)

sm = FakeStorymarket()

# Use a predictable MIME boundary.

BOUNDARY = 'BOUNDARY'
def setup():
    BinaryContentManager._multipart_boundary = BOUNDARY
def teardown():    
    BinaryContentManager._multipart_boundary = None

def test_content_apis():
    test_data = [
        (sm.audio,  Audio, 'audio', {'duration': '1:00'}),
        (sm.data,   Data,  'data',  {}),
        (sm.photos, Photo, 'photo', {'caption': 'Hi!'}),
        (sm.text,   Text,  'text',  {'content': 'Hi!'}),
        (sm.video,  Video, 'video', {'duration': '1:00'})
    ]

    # Data carefully constructed so that we've got both URLs and objects
    # for related data.
    create_update_data = {
        'category': '/content/sub_category/1/',
        'author': 'frank',
        'title': 'Sample API title',
        'org': sm.orgs.get(1),
        'tags': 'one, two, three',
        'rights_scheme': 1,
        'pricing_scheme': sm.pricing.get(1),
    }

    def assert_instance_delete(instance, manager):
        with mock.patch.object(manager, 'delete'):
            instance.delete()
            manager.delete.assert_called_with(instance)

    def assert_instance_save(instance, manager):
        with mock.patch.object(manager, 'update'):
            instance.save()
            manager.update.assert_called_with(instance)

    for (manager, cls, urlbit, extra_data) in test_data:
        list_url = 'content/%s/' % urlbit
        detail_url = 'content/%s/1/' % urlbit
        post_data = dict(create_update_data, **extra_data)
        instance = manager.get(1)
        
        yield assert_list_api, sm, manager.all, cls, list_url
        yield assert_get_api, sm, manager.get, cls, detail_url
        yield assert_delete_api, sm, manager.delete, cls, detail_url
        yield assert_instance_delete, instance, manager
        yield assert_create_api, sm, manager.create, instance, post_data, list_url
        yield assert_update_api, sm, manager.update, instance, post_data, detail_url
        yield assert_instance_save, instance, manager

def test_related_resource_properties():
    test_data = [
        ('author', User),
        ('category', Category),
        ('sub_type', Subtype),
        ('org', Org),
        ('pricing_scheme', PricingScheme),
        ('rights_scheme', RightsScheme),
        ('uploaded_by', User),
    ]
    
    resource = sm.audio.get(1)
    def check_related_resource_property(attname, cls):
        related = getattr(resource, attname)
        assert_isinstance(related, cls)

    for (attname, cls) in test_data:
        yield check_related_resource_property, attname, cls

def test_related_resource_properties_when_none():
    test_properties = ['author', 'category', 'org', 'pricing_scheme',
                       'rights_scheme', 'uploaded_by']
    
    def check_related_resource_property_when_none(attname):
        resource = sm.audio.get(1)
        setattr(resource, '_'+attname, None)
        assert_equal(getattr(resource, attname), None)
    
    for prop in test_properties:
        yield check_related_resource_property_when_none, prop

def test_blob_uploads():
    test_data = [
        (sm.audio, 'audio'),
        (sm.data, 'data'),
        (sm.photos, 'photo'),
        (sm.video, 'video')
    ]

    new_data = 'not really binary data'
    
    def check_blob_upload(manager, urlbit, data):
        resource = manager.get(1)
        expected_body = (
            '--%s\r\n' % BOUNDARY +
            'Content-Disposition: form-data; name="blob"\r\n' +
            'Content-Type: text/plain; charset=utf-8\r\n' +
            '\r\n%s\r\n' % new_data +
            '--%s--\r\n' % BOUNDARY
        )
        
        # Try with
        resource.upload_blob(data)
        sm.assert_called('PUT', 'content/%s/1/blob/' % urlbit, body=expected_body)
    
    for (manager, urlbit) in test_data:
        # Check with both a string object and a fike-like object.
        yield check_blob_upload, manager, urlbit, new_data
        yield check_blob_upload, manager, urlbit, StringIO(new_data)

def test_user_eq():
    u1 = User({'username': 'u1', 'first_name': 'u', 'last_name': '1', 'email': '1@example.org'})
    u2 = User({'username': 'u2', 'first_name': 'u', 'last_name': '2', 'email': '2@example.org'})
    # Same username as u1, so == to u1.
    u3 = User({'username': 'u1', 'first_name': 'u', 'last_name': '3', 'email': '3@example.org'})

    assert_equal(u1, u1)
    assert_not_equal(u1, u2)
    assert_equal(u1, u3)