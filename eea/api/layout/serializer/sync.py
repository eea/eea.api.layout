""" Sync layout
"""
from plone import api
from zope.interface import implementer
from zope.component import adapter
from zope.publisher.interfaces.browser import IBrowserRequest
from eea.api.layout.interfaces import IFixedLayoutBlockSerializationSync
from eea.api.layout.interfaces import IFixedLayoutBlocks
from eea.api.layout.interfaces import IFixedLayoutBlocksSettings


@implementer(IFixedLayoutBlockSerializationSync)
@adapter(IFixedLayoutBlocks, IBrowserRequest)
class DefaultFixedLayoutSync(object):
    """Sync basic layout block properties"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._layout = None
        self._readOnlySettings = None

    @property
    def layout(self):
        """ Layout fixed settings
        """
        if self._layout is None:
            self._layout = api.portal.get_registry_record(
                "layout",
                interface=IFixedLayoutBlocksSettings,
                default=[]
            )
        return self._layout

    @property
    def readOnlySettings(self):
        """ Read-only settings
        """
        if self._readOnlySettings is None:
            self._readOnlySettings = api.portal.get_registry_record(
                "readOnlySettings",
                interface=IFixedLayoutBlocksSettings,
                default=[]
            )
        return self._readOnlySettings

    def __call__(self, layout, block):
        res = {}

        readOnlySettings = layout.get("readOnlySettings")
        for key, value in layout.items():
            # Get block properties from layout
            if key in self.layout:
                res[key] = value

            # Get readOnlySettings from layout if enabled
            if readOnlySettings and (key in self.readOnlySettings):
                res[key] = value

        # Get all the other block properties
        for key, value in block.items():
            if key not in res:
                res[key] = value

        return res
