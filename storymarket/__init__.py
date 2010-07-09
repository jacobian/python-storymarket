from __future__ import absolute_import

__version__ = '1.0'

from .client import StorymarketClient
from .categories import CategoryManager, SubcategoryManager
from .content import AudioManager, DataManager, PhotoManager, TextManager, VideoManager
from .orgs import OrgManager
from .schemes import PricingSchemeManager, RightsSchemeManager

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
        self.data = DataManager(self)
        self.orgs = OrgManager(self)
        self.photos = PhotoManager(self)
        self.pricing = PricingSchemeManager(self)
        self.rights = RightsSchemeManager(self)
        self.subcategories = SubcategoryManager(self)
        self.text = TextManager(self)
        self.video = VideoManager(self)
