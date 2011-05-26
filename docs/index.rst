Python bindings to the Storymarket API
======================================

.. module:: storymarket
   :synopsis: A client library for the Storymarket API.
   
.. currentmodule:: storymarket

This is a client for the `Storymarket API <http://storymarket.com/api/v1/>`_.

You'll need a Storymarket account to use this library, and you'll need to
generate an API token by visiting the 
`Developer API page <http://storymarket.com/users/api/>`_.

Usage
-----

First create an instance of the API with your creds::

    >>> import storymarket
    >>> api = storymarket.Storymarket(STORYMARKET_API_KEY)
    
Then call on the :class:`Storymarket` object:

.. class:: Storymarket

    .. attribute:: audio
        
        An :class:`AudioManager` - get, create, and update audio content.

    .. attribute:: data
        
        A :class:`DataManager` - get, create, and update data content.
    
    .. attribute:: photos
        
        A :class:`PhotoManager` - get, create, and update photo content.
    
    .. attribute:: text
        
        A :class:`TextManager` - get, create, and update text content.
    
    .. attribute:: video
        
        A :class:`VideoManager` - get, create, and update photo content.
    
    .. attribute:: packages
    
        A :class:`PackageManager` - get, create, and update packages of content.
    
    .. attribute:: categories
        
        A :class:`CategoryManager` - get categories.
    
    .. attribute:: subcategories
        
        A :class:`SubcategoryManager` - get subcategories.

    .. attribute:: sub_type

        A :class:`SubtypeManager` - get subtypes.
    
    .. attribute:: orgs
        
        An :class:`OrgManager` - get organizations.
    
    .. attribute:: pricing
        
        A :class:`PricingSchemeManager` - get pricing schemes.
    
    .. attribute:: rights
        
        A :class:`RightsSchemeManager` - get rights schemes.
    
For example::

    >>> api.orgs.all()
    [<Org: My Org>]
    
    >>> api.text.create({
    ...     'title': 'Man Bite Dog',
    ...     'content': '...',
    ...     'tags': ['man', 'dog', 'biting'],
    ...     'org': api.orgs.all()[0],
    ...     'category': api.categories.get(123)
    ... })
    >>> <Text: Man Bites Dog>
        
For details, see:

    .. toctree::
       :maxdepth: 1
       
       content
       packages
       categories
       orgs
       schemes

.. seealso:: 
    
    `Storymarket's API documentation <http://storymarket.com/api/v1/>`_.

Contributing
------------

Run tests with ``python setup.py test`` or install 
`Nose <pypi.python.org/pypi/nose/>`_ and run ``nosetests``.

Development takes place 
`on GitHub <http://github.com/jacobian/python-storymarket>`_; please file
bugs/pull requests there.

Development on this project was funded by the 
`Lawrence Journal-World <http://ljworld.com/>`_ - thanks!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

