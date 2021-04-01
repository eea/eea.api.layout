""" Layout Blocks serializer
"""
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter
from plone.schema import IJSONField
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.blocks import BlocksJSONFieldSerializer
from eea.api.layout.interfaces import ILayoutBlocks
import copy


@adapter(IJSONField, ILayoutBlocks, Interface)
@implementer(IFieldSerializer)
class LayoutBlocksJSONFieldSerializer(BlocksJSONFieldSerializer):
    """ Blocks with layout serializer
    """
    def get_uid_data(self, layout, blocks, default=None):
        for uid, block in blocks.items():
            if block.get("@layout") == layout:
                return uid, block.get("data", default)
        return layout, default

    def blocks(self, blocks):
        res = {}
        default = copy.deepcopy(self.field.default)

        # Render layout with real data
        for layout, block in default.items():
            uid, data = self.get_uid_data(layout, blocks, block.get('data'))
            res[uid] = block
            res[uid]['@layout'] = layout

            if block.get('readOnly'):
                continue

            if 'data' in block:
                res[uid]['data'] = data

        # Render blocks that are not in layout
        for uid, block in blocks.items():
            if uid not in res:
                res[uid] = block

        return res

    def blocks_layout(self, blocks_layout):
        return blocks_layout

    def __call__(self):
        value = super(LayoutBlocksJSONFieldSerializer, self).__call__()
        if not self.field.default:
            return value

        if self.field.getName() == "blocks":
            return self.blocks(value)

        if self.field.getName() == 'blocks_layout':
            return self.blocks_layout(value)
