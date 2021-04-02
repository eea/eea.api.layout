""" Sync layout
"""
from zope.interface import implementer
from zope.component import adapter
from zope.publisher.interfaces.browser import IBrowserRequest
from eea.api.layout.interfaces import IFixedLayoutBlockSerializationSync
from eea.api.layout.interfaces import IFixedLayoutBlocks


@implementer(IFixedLayoutBlockSerializationSync)
@adapter(IFixedLayoutBlocks, IBrowserRequest)
class DefaultFixedLayoutSync(object):
    """Sync basic layout block properties"""

    layout = {
        "placeholder": True,
        "required": True,
        "fixed": True,
        "disableNewBlocks": True,
        "readOnly": True,
    }

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, layout, block):
        res = {}

        # Get block properties from layout
        for key, value in layout.items():
            if self.layout.get(key):
                res[key] = value

        # Get all the other block properties
        for key, value in block.items():
            if key not in res:
                res[key] = value

        return res


@implementer(IFixedLayoutBlockSerializationSync)
@adapter(IFixedLayoutBlocks, IBrowserRequest)
class ExtendedFixedLayoutSync(DefaultFixedLayoutSync):
    """Sync extended layout block properties"""

    extended_layout = {
        "instructions": True,
        "allowedBlocks": True,
        "maxChars": True,
        "readOnlySettings": ["title", "as"],
        "disableInnerButtons": True,
        "fixedLayout": True,
    }

    def __call__(self, layout, block):
        res = super(ExtendedFixedLayoutSync, self).__call__(layout, block)

        # Get block properties from layout
        readOnlySettings = layout.get("readOnlySettings")
        for key, value in layout.items():
            if self.extended_layout.get(key):
                res[key] = value
            if readOnlySettings and (
                key in self.extended_layout.get("readOnlySettings")
            ):
                res[key] = value

        return res
