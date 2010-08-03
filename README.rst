Python bindings to the Storymarket API
======================================

This is a client for the `Storymarket API <http://storymarket.com/api/v1/>`_.

You'll need a Storymarket account to use this library, and you'll need to
generate an API token by visiting the 
`Developer API page <http://storymarket.com/users/api/>`_.

Usage
-----

First create an instance of the API with your creds::

    >>> import storymarket
    >>> api = storymarket.Storymarket(YOUR_API_KEY)
    
Then call methods::

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
        
For details, 
`see the documentation <http://packages.python.org/python-storymarket/>`_ 
and/or Storymarket's `API documentation <http://storymarket.com/api/v1/>`_.

Contributing
------------

Development takes place 
`on GitHub <http://github.com/jacobian/python-storymarket>`_; please file
bugs/pull requests there.

Development on this project was funded by the 
`Lawrence Journal-World <http://ljworld.com/>`_ - thanks!