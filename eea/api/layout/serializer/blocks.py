""" Layout Blocks serializer
"""
import copy
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter, queryMultiAdapter
from plone.schema import IJSONField
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.blocks import BlocksJSONFieldSerializer
from eea.api.layout.interfaces import IFixedLayoutBlocks
from eea.api.layout.interfaces import IFixedLayoutBlockSerializationSync


@adapter(IJSONField, IFixedLayoutBlocks, Interface)
@implementer(IFieldSerializer)
class FixedLayoutBlocksJSONFieldSerializer(BlocksJSONFieldSerializer):
    """Blocks with layout serializer"""

    def sync_layout(self, layout, block):
        """Sync layout with block items"""
        value = copy.deepcopy(layout)
        if layout.get("readOnly"):
            return value

        handler = queryMultiAdapter(
            (self.context, self.request),
            IFixedLayoutBlockSerializationSync,
            name=layout.get("@type", ""),
            default=queryMultiAdapter(
                (self.context, self.request),
                IFixedLayoutBlockSerializationSync
            ),
        )

        if handler:
            value = handler(value, block)

        # Sync sub-blocks
        if "blocks" in layout and "blocks" in block:
            if (isinstance(layout['blocks'], dict) and
               isinstance(block["blocks"], dict)):
                value["blocks"] = self.blocks(
                    layout["blocks"],
                    block["blocks"]
                )
                # Sub-block has a fixed layout
                if (
                    layout.get('fixedLayout') and
                    "blocks_layout" in layout and
                    "blocks_layout" in block
                ):
                    value["blocks_layout"] = self.blocks_layout(
                        layout["blocks_layout"],
                        block["blocks_layout"],
                        block["blocks"]
                    )

        if "data" in layout and "data" in block:
            if (isinstance(layout["data"], dict) and
               isinstance(block["data"], dict)):
                if (
                    "blocks" in layout["data"] and
                    "blocks" in block["data"]
                ):
                    value["data"]["blocks"] = self.blocks(
                        layout["data"]["blocks"], block["data"]["blocks"]
                    )
                    # Sub-block has a fixed layout
                    if (
                        layout.get('fixedLayout') and
                        "blocks_layout" in layout['data'] and
                        "blocks_layout" in block['data']
                    ):
                        value["data"]["blocks_layout"] = self.blocks_layout(
                            layout['data']["blocks_layout"],
                            block['data']["blocks_layout"],
                            block['data']["blocks"]
                        )

        return value

    def get_uid(self, layout_id, blocks):
        """Get layout new uid"""
        for uid, block in blocks.items():
            if uid == layout_id:
                return uid
            if block.get("@layout") == layout_id:
                return uid
        return layout_id

    def get_uid_block(self, layout_id, layout, blocks):
        """Get UID and Block data"""
        for uid, block in blocks.items():
            if uid == layout_id:
                return uid, self.sync_layout(layout, block)
            if block.get("@layout") == layout_id:
                return uid, self.sync_layout(layout, block)
        return layout_id, layout

    def blocks(self, layout, blocks):
        """Get blocks"""
        res = {}

        # Render layout with real data
        for layout_id, layout_block in layout.items():
            uid, block = self.get_uid_block(layout_id, layout_block, blocks)
            res[uid] = block

        # Render blocks that are not in layout
        for uid, block in blocks.items():
            if uid not in res:
                res[uid] = block

        return res

    def blocks_layout(self, layout, value, blocks):
        """Get blocks layout"""
        items = layout.get("items", [])
        if not items:
            return value

        if not blocks:
            return value

        res = []
        for layout_id in items:
            uid = self.get_uid(layout_id, blocks)
            res.append(uid)
        return {"items": res}

    def __call__(self):
        value = super(FixedLayoutBlocksJSONFieldSerializer, self).__call__()
        if not self.field.default:
            return value

        layout = copy.deepcopy(self.field.default)

        if self.field.getName() == "blocks":
            return self.blocks(layout, value)

        if self.field.getName() == "blocks_layout":
            blocks = getattr(self.context, "blocks")
            return self.blocks_layout(layout, value, blocks)

        return value
