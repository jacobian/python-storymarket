from __future__ import absolute_import

__version__ = '1.0b4'

from . import exceptions
from .client import StorymarketClient
from .categories import Category, CategoryManager, SubcategoryManager
from .subtypes import Subtype, SubtypeManager
from .content import (Audio, Data, Photo, Text, Video, AudioManager,
                      DataManager, PhotoManager, TextManager, VideoManager)
from .orgs import Org, OrgManager
from .packages import Package, PackageManager
from .schemes import (PricingScheme, RightsScheme, PricingSchemeManager,
                      RightsSchemeManager)

class Storymarket(object):
    """
    Access to the Storymarket API.
    
    To use, first create an instance with your creds::
    
        >>> storymarket = Storymarket(API_KEY)
        
    Then call methods::
        
        >>> storymarket.categories.all()
        [...]
                
    """
    
    def __init__(self, key):
        self.client = StorymarketClient(key)
        self.audio = AudioManager(self)
        self.categories = CategoryManager(self)
        self.sub_types = SubtypeManager(self)
        self.data = DataManager(self)
        self.orgs = OrgManager(self)
        self.packages = PackageManager(self)
        self.photos = PhotoManager(self)
        self.pricing = PricingSchemeManager(self)
        self.rights = RightsSchemeManager(self)
        self.subcategories = SubcategoryManager(self)
        self.text = TextManager(self)
        self.video = VideoManager(self)
