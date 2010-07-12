from __future__ import absolute_import

import mock
from nose.tools import assert_equal, assert_not_equal
from storymarket import (Audio, Data, Photo, Text, Video, Category, Org,
                         PricingScheme, RightsScheme)
from storymarket.content import User
from .fakeserver import FakeStorymarket
from .utils import (assert_isinstance, assert_list_api, assert_get_api,
                    assert_delete_api, assert_create_api, assert_update_api)

sm = FakeStorymarket()

def test_content_apis():
    test_data = [
        (sm.audio,  Audio, 'audio', {'duration': '1:00'}),
        (sm.data,   Data,  'data',  {}),
        (sm.photos, Photo, 'photo', {'caption': 'Hi!'}),
        (sm.text,   Text,  'text',  {'content': 'Hi!'}),
        (sm.video,  Video, 'video', {'duration': '1:00'})
    ]

    create_update_data = {
        'category': '/content/sub_category/1/',
        'author': 'frank',
        'title': 'Sample API title',
        'org': '/orgs/1/',
        'tags': 'one, two, three'
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
    