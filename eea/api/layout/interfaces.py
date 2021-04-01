"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.restapi.behaviors import IBlocks


class IEeaApiLayoutLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ILayoutBlocks(IBlocks):
    """Blocks with Layout (TTW, external, etc.)"""
