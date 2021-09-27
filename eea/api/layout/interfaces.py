"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.restapi.behaviors import IBlocks
from eea.api.layout import EEAMessageFactory as _


class IEeaApiLayoutLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFixedLayoutBlocks(IBlocks):
    """Blocks with Layout (TTW, external, etc.)"""


class IFixedLayoutBlockSerializationSync(Interface):
    """ Sync block properties with Layout
    """


class IFixedLayoutBlocksSettings(Interface):
    """ Sync block settings
    """
    layout = schema.List(
        title=_(u"Fixed properties"),
        description=_(
            u"This block properties will be always read from layout"),
        value_type=schema.ASCIILine(title=_(u"Block property")),
        default=[
            "placeholder",
            "required",
            "fixed",
            "disableNewBlocks",
            "readOnly",
            "instructions",
            "allowedBlocks",
            "maxChars",
            "readOnlyTitles",
            "readOnlySettings",
            "disableInnerButtons",
            "fixedLayout",
            "styles",
            "fields",
        ]
    )

    readOnlySettings = schema.List(
        title=_(u"Read only properties"),
        description=_(
            u"This block properties will be read from layout "
            u"if readOnlySettings is enabled"),
        value_type=schema.ASCIILine(title=_(u"Block property")),
        default=[
            "align",
            "as",
            "collapsed",
            "id",
            "non_exclusive",
            "right_arrows",
            "size"
            "title_size",
            "title",
        ]
    )
