from __future__ import absolute_import

from storymarket import (Audio, Data, Photo, Text, Video, Category, Org,
                         PricingScheme, RightsScheme)
from storymarket.content import User
from .fakeserver import FakeStorymarket
from .utils import assert_isinstance, assert_list_api, assert_get_api

sm = FakeStorymarket()


def test_content_apis():
    test_data = [
        (sm.audio, Audio, 'audio'),
        (sm.data, Data, 'data'),
        (sm.photos, Photo, 'photo'),
        (sm.text, Text, 'text'),
        (sm.video, Video, 'video')
    ]

    for (manager, cls, urlbit) in test_data:
        yield assert_list_api, sm, manager.all, cls, 'content/%s/' % urlbit
        yield assert_get_api, sm, manager.get, cls, 'content/%s/1/' % urlbit
        
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
        
        