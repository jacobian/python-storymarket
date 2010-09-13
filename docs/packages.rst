========
Packages
========

.. currentmodule:: storymarket

Storymarket supports grouping of collected content into packages (which
can have their own pricing and rights schemes).

Packages (managed via :attr:`Storymarket.packages`) are fairly similar to
other content types (see :doc:`content`). The difference is that packages
have a set of content "inside" the packages, so when uploading packages
you'll need to provide that data. Like all related objects, you can provide
related data as either instances of the appropriate content object or as
IDs. For example::

    >>> api = storymarket.Storymarket(STORYMARKET_API_KEY)

    # Grab a few objects to create a package with.
    >>> text1 = api.text.get(123)
    >>> text2 = api.text.get(456)
    >>> vid1 = api.text.get(444)
    
    # Make the package.
    >>> api.packages.create({
    ...     'title': 'My Content Package',
    ...     'tags': ['hi'],
    ...     'org': api.orgs.all()[0],
    ...     'category': api.categories.get(123),
    ...     'text_items': [text1, text2, 789],
    ...     'video_items': [vid1],
    ...     'audio_items': [111, 222]
    ... })

As you can see, each type has its own key in the creation dict --
``audio_items``, ``data_items``, ``text_items``, ``photo_items``, or
``video_items`` -- and each item in those lists can be an int or an
instance.

Reference
=========

Detailed reference for the package classes follow:

.. autoclass:: PackageManager
   :members: all, get, create, update
   
.. autoclass:: Package
   :members: save
   
   .. attribute:: audio_items
   
        List of :class:`Audio` items in this package.
   
   .. attribute:: author

   .. attribute:: category

   .. attribute:: data_items

        List of :class:`Data` items in this package.

   .. attribute:: description

   .. attribute:: expire_date

   .. attribute:: fact_checked

   .. attribute:: links

   .. attribute:: one_off_author

   .. attribute:: photo_items

        List of :class:`Photo` items in this package.

   .. attribute:: pricing_scheme
   
   .. attribute:: rights_scheme
   
   .. attribute:: tags
   
   .. attribute:: text_items
   
        List of :class:`Text` items in this package.
   
   .. attribute:: title
   
   .. attribute:: uploaded_by
   
   .. attribute:: video_items
   
        List of :class:`Video` items in this package.
