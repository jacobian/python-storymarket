from __future__ import absolute_import

from . import base
from .content import (ContentResource, ContentManager, Audio, Data, Photo,
                      Text, Video)

class Package(ContentResource):
    _related_keys = ContentResource._related_keys + ['audio_items',
                                                     'data_items',
                                                     'photo_items',
                                                     'text_items',
                                                     'video_items']
                                                     
    @property
    def audio_items(self):
        return [Audio(self.manager.api.audio, audio)
                for audio in self._audio_items]
        
    @property
    def data_items(self):
        return [Data(self.manager.api.data, data)
                for data in self._data_items]
        
    @property
    def photo_items(self):
        return [Photo(self.manager.api.photos, photo)
                for photo in self._photo_items]
    
    @property
    def text_items(self):
        return [Text(self.manager.api.text, text)
                for text in self._text_items]
                
    @property
    def video_items(self):
        return [Video(self.manager.api.video, video)
                for video in self._video_items]

class PackageManager(ContentManager):
    resource_class = Package
    urlbit = 'package'
    
    def _flatten(self, resource):
        # Extend flattening to handle all the *_items fields.
        
        flattened = super(PackageManager, self)._flatten(resource)
        
        for related_type in ['audio', 'data', 'photo', 'text', 'video']:
            key = '%s_items' % related_type
            
            flattened_related = []
            for related in flattened.get(key, []):
                if not isinstance(related, basestring):
                    related = '/content/%s/%s/' % (related_type, base.getid(related))
                flattened_related.append(related)
            
            flattened[key] = flattened_related
                              
        return flattened