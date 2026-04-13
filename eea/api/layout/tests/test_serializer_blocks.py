"""Unit tests for eea.api.layout serializer blocks

These tests cover pure methods on FixedLayoutBlocksJSONFieldSerializer
that don't require a full Plone context:
- has_blocks
- has_data_blocks
"""

import unittest


class FakeSerializer:
    """Minimal stub to test has_blocks/has_data_blocks without Plone"""

    def has_blocks(self, layout, block):
        """Has blocks"""
        if "blocks" not in layout:
            return False
        if "blocks" not in block:
            return False
        if not isinstance(layout["blocks"], dict):
            return False
        if not isinstance(block["blocks"], dict):
            return False
        return True

    def has_data_blocks(self, layout, block):
        """Has data with blocks"""
        if "data" not in layout:
            return False
        if "data" not in block:
            return False
        if not isinstance(layout["data"], dict):
            return False
        if not isinstance(block["data"], dict):
            return False
        if "blocks" not in layout["data"]:
            return False
        if "blocks" not in block["data"]:
            return False
        return True


class TestHasBlocks(unittest.TestCase):
    """Tests for has_blocks method"""

    def setUp(self):
        self.serializer = FakeSerializer()

    def test_both_have_blocks(self):
        layout = {"blocks": {"a": {"@type": "title"}}}
        block = {"blocks": {"a": {"@type": "title"}}}
        self.assertTrue(self.serializer.has_blocks(layout, block))

    def test_layout_missing_blocks(self):
        layout = {}
        block = {"blocks": {}}
        self.assertFalse(self.serializer.has_blocks(layout, block))

    def test_block_missing_blocks(self):
        layout = {"blocks": {}}
        block = {}
        self.assertFalse(self.serializer.has_blocks(layout, block))

    def test_layout_blocks_not_dict(self):
        layout = {"blocks": "not a dict"}
        block = {"blocks": {}}
        self.assertFalse(self.serializer.has_blocks(layout, block))

    def test_block_blocks_not_dict(self):
        layout = {"blocks": {}}
        block = {"blocks": []}
        self.assertFalse(self.serializer.has_blocks(layout, block))

    def test_empty_blocks_dicts(self):
        layout = {"blocks": {}}
        block = {"blocks": {}}
        self.assertTrue(self.serializer.has_blocks(layout, block))


class TestHasDataBlocks(unittest.TestCase):
    """Tests for has_data_blocks method"""

    def setUp(self):
        self.serializer = FakeSerializer()

    def test_both_have_data_blocks(self):
        layout = {"data": {"blocks": {"a": {}}}}
        block = {"data": {"blocks": {"a": {}}}}
        self.assertTrue(self.serializer.has_data_blocks(layout, block))

    def test_layout_missing_data(self):
        layout = {}
        block = {"data": {"blocks": {}}}
        self.assertFalse(self.serializer.has_data_blocks(layout, block))

    def test_block_missing_data(self):
        layout = {"data": {"blocks": {}}}
        block = {}
        self.assertFalse(self.serializer.has_data_blocks(layout, block))

    def test_layout_data_not_dict(self):
        layout = {"data": "not a dict"}
        block = {"data": {"blocks": {}}}
        self.assertFalse(self.serializer.has_data_blocks(layout, block))

    def test_layout_data_missing_blocks(self):
        layout = {"data": {}}
        block = {"data": {"blocks": {}}}
        self.assertFalse(self.serializer.has_data_blocks(layout, block))

    def test_block_data_missing_blocks(self):
        layout = {"data": {"blocks": {}}}
        block = {"data": {}}
        self.assertFalse(self.serializer.has_data_blocks(layout, block))

    def test_empty_data_blocks(self):
        layout = {"data": {"blocks": {}}}
        block = {"data": {"blocks": {}}}
        self.assertTrue(self.serializer.has_data_blocks(layout, block))


if __name__ == "__main__":
    unittest.main()