============
Content APIs
============

.. currentmodule:: storymarket

Storymarket supports five types of content: audio_, data_ sets, photos_,
text_, and video_. This library exposes each as a separate manager and
content object, but each type is extremely similar -- they only differ in
the specific content data fields.

Basic usage
===========

Each content manager supports five operations:

    ``all()``
        List all objects of this type.
        
    ``get()``
        Get a specific object by ID.
        
    ``delete()``
        Delete a specific object.
        
    ``create()``
        Create a new object (see `uploading new objects`_, below).
        
    ``update()``
        Update an existing object, perhaps with new data (see `updating
        existing objects`_, below).
        
Additionally, every content type except for text has associated binary
data, so these content types have additional ``upload_blob()`` methods to
post a new binary data blob. See `uploading binary data`_ for details.

Uploading new objects
---------------------

There's two ways to upload a new bit of content to Storymarket. 

The hard way... well, let's skip the hard way: it's hard. The easy way to
upload content is to pass in a flat dictionary to ``create()``. For
example, to create a new text item::

    >>> api = storymarket.Storymarket(STORYMARKET_API_KEY)
    >>> api.text.create({
    ...     'title': 'Man Bite Dog',
    ...     'content': '...',
    ...     'tags': ['man', 'dog', 'biting'],
    ...     'org': api.orgs.all()[0],
    ...     'category': api.categories.get(123)
    ... })
    >>> <Text: Man Bites Dog>

In general, this is pretty flexible, but there's a few things worth
understanding here:

    * The required and optional fields vary a bit from type to type. See
      `content object fields`_, below, for details.
      
    * Fields that represent related objects -- that's the ``org`` and
      ``category`` fields -- can take either objects (e.g. :class:`Org`,
      :class:`Category`, etc.) or IDs (e.g. ``13``, ``22``).
      
    * The ``tags`` field is required, and must be either a ``list`` of tags
      or a string of comma-separated tags.
      
    * The ``category`` field, despite the name, is actually a
      *subcategory*, so when looking up values for this field make sure to
      use :attr:`Storymarket.subcategories`
      
    * Binary data -- i.e. everything except for text -- requires an extra
      step to upload the actual blob; see `uploading binary data`_ for
      details.
      
Content object fields
~~~~~~~~~~~~~~~~~~~~~

As mentioned above, each content type has a slightly different set of
fields. The table below summarizes these fields. All objects share the
required/optional fields listed next to "All types"; the additional fields
specific to each type are then listed next to that type.

    ==============  ==========================  ===============================
    Content type    Required fields             Optional fields
    ==============  ==========================  ===============================
    All types       ``category``, ``org``,      ``author``, ``description``,
                    ``tags``, ``title``         ``fact_checked``,
                                                ``one_off_author``,
                                                ``pricing_scheme``,
                                                ``rights_scheme``
    
    Audio                                       ``duration``, ``expire_date``
    
    Data                                        ``expire_date``
    
    Photo           ``caption``                 ``expire_date``
    
    Text            ``content``                 ``words``
    
    Video                                       ``duration``, ``expire_date``
    ==============  ==========================  ===============================
    
Uploading binary data
~~~~~~~~~~~~~~~~~~~~~

Uploading new binary data or changing an existing binary blob requires a
separate step after calling ``create()`` or ``update()``: you need to call
``upload_blob()`` to upload the actual binary object. This method can take
either a file-like object or a string of the actual binary data to upload.

An example should help make this clear: to upload a new photo, you'd do
something like::

    >>> api = storymarket.Storymarket(STORYMARKET_API_KEY)
    
    # Look up an Org and Category to use for the photo.
    >>> org = api.orgs.get(MY_ORG_ID)
    >>> category = api.subcategories.GET(SOME_CATEGORY_ID)
    
    # Create a new photo object
    >>> new_photo = api.photos.create({
    ...     'title': 'Man biting dog',
    ...     'caption': 'This man is biting a dog.',
    ...     'tags': 'man, dog, biting',
    ...     'org': org,
    ...     'category': 'category'
    ... })
    
    # Upload a file as the photo's blob
    >>> fp = open('path/to/awesome_photo.jpg')
    >>> new_photo.upload_blob(fp)
    
Updating existing objects
-------------------------

Updating existing objects is easy. Just modify the content object in place
and call its ``save()`` method::

    >>> api = storymarket.Storymarket(STORYMARKET_API_KEY)

    >>> t = api.text.get(SOME_ID)
    >>> t.title = 'Look, I updated it!'
    >>> t.save()

Reference
=========

Detailed reference for each content type follows.

Audio
-----

.. autoclass:: AudioManager
   :members: all, get, delete, create, update, upload_blob
   
.. autoclass:: Audio
   :members: save, delete, upload_blob
   
   .. attribute:: audio
   .. attribute:: author
   .. attribute:: category
   .. attribute:: description
   .. attribute:: duration
   .. attribute:: expire_date
   .. attribute:: fact_checked
   .. attribute:: links
   .. attribute:: one_off_author
   .. attribute:: pricing_scheme
   .. attribute:: rights_scheme
   .. attribute:: size
   .. attribute:: tags
   .. attribute:: title
   .. attribute:: uploaded_by

Data
----

.. autoclass:: DataManager
   :members: all, get, delete, create, update, upload_blob
   
.. autoclass:: Data
   :members: save, delete, upload_blob
   
   .. attribute:: author
   .. attribute:: category
   .. attribute:: data
   .. attribute:: description
   .. attribute:: duration
   .. attribute:: expire_date
   .. attribute:: fact_checked
   .. attribute:: links
   .. attribute:: one_off_author
   .. attribute:: pricing_scheme
   .. attribute:: rights_scheme
   .. attribute:: size
   .. attribute:: tags
   .. attribute:: title
   .. attribute:: uploaded_by

Photos
------

.. autoclass:: PhotoManager
   :members: all, get, delete, create, update, upload_blob
   
.. autoclass:: Photo
   :members: save, delete, upload_blob
   
   .. attribute:: author
   .. attribute:: caption
   .. attribute:: category
   .. attribute:: description
   .. attribute:: duration
   .. attribute:: expire_date
   .. attribute:: fact_checked
   .. attribute:: links
   .. attribute:: one_off_author
   .. attribute:: photo
   .. attribute:: pricing_scheme
   .. attribute:: rights_scheme
   .. attribute:: size
   .. attribute:: tags
   .. attribute:: title
   .. attribute:: uploaded_by

Text
----

.. autoclass:: TextManager
   :members: all, get, delete, create, update
   
.. autoclass:: Text
   :members: save, delete
      
   .. attribute:: author
   .. attribute:: category
   .. attribute:: content
   .. attribute:: data
   .. attribute:: description
   .. attribute:: duration
   .. attribute:: expire_date
   .. attribute:: fact_checked
   .. attribute:: links
   .. attribute:: one_off_author
   .. attribute:: pricing_scheme
   .. attribute:: rights_scheme
   .. attribute:: size
   .. attribute:: tags
   .. attribute:: title
   .. attribute:: uploaded_by
   .. attribute:: words

Video
-----

.. autoclass:: VideoManager
   :members: all, get, delete, create, update, upload_blob
   
.. autoclass:: Video
   :members: save, delete, upload_blob
   
   .. attribute:: author
   .. attribute:: category
   .. attribute:: description
   .. attribute:: duration
   .. attribute:: expire_date
   .. attribute:: fact_checked
   .. attribute:: links
   .. attribute:: one_off_author
   .. attribute:: pricing_scheme
   .. attribute:: rights_scheme
   .. attribute:: size
   .. attribute:: tags
   .. attribute:: title
   .. attribute:: uploaded_by
   .. attribute:: video
