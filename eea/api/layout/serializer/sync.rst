Fixed Layout Block Synchronizer
===============================

A multi-adapter used to fill a layout block with content.

Imports
-------

    >>> from pprint import pprint
    >>> from zope.interface import alsoProvides
    >>> from zope.component import getMultiAdapter
    >>> from eea.api.layout.interfaces import IFixedLayoutBlocks
    >>> from eea.api.layout.interfaces import IFixedLayoutBlockSerializationSync

Set up
------

Setup sandbox

    >>> portal = layer["portal"]
    >>> request = layer["request"]
    >>> sandbox = portal["sandbox"]

Synchronize
-----------

Enable fixed.layout behavior

    >>> alsoProvides(sandbox, IFixedLayoutBlocks)

Get sync adapter

    >>> sync = getMultiAdapter((sandbox, request), IFixedLayoutBlockSerializationSync)
    >>> sync
    <eea.api.layout.serializer.sync.DefaultFixedLayoutSync object at ...>

Layout block:

    >>> layout = {
    ...   "@type": "image",
    ...   "required": True,
    ...   "fixed": True,
    ...   "disableNewBlocks": True,
    ...   "placeholder": "Add image",
    ...   "readOnlySettings": True,
    ...   "title": "Foo bar"
    ... }

Content block:

    >>> block = {
    ...   "@layout": "5956e52d-60d7-474f-bca3-c7efe09dc858",
    ...   "@type": "image",
    ...   "alt": "Flower",
    ...   "title": "Flower",
    ...   "disableNewBlocks": False,
    ...   "fixed": False,
    ...   "placeholder": "Add yout image here",
    ...   "required": False,
    ...   "url": "http://localhost:3000/api/flower.png",
    ...   "href": "http://flowers.com",
    ...   "openLinkInNewTab": True,
    ...   "size": "m",
    ...   "align": "center"
    ... }

Synced block:

    >>> synced = sync(layout, block)
    >>> pprint(synced)
    {'@layout': '5956e52d-60d7-474f-bca3-c7efe09dc858',
     '@type': 'image',
     'align': 'center',
     'alt': 'Flower',
     'disableNewBlocks': True,
     'fixed': True,
     'href': 'http://flowers.com',
     'openLinkInNewTab': True,
     'placeholder': 'Add image',
     'readOnlySettings': True,
     'required': True,
     'size': 'm',
     'title': 'Foo bar',
     'url': 'http://localhost:3000/api/flower.png'}
