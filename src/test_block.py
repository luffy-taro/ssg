import unittest

from BlockNode import BlockType, block_to_block_type



class TestBlock(unittest.TestCase):
    def test_paragraph(self):
        text = "This is paragraph"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        text = """1. l1\n2. l2\n3. l3"""
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_unordered_list(self):
        text = """- l1\n- l2\n- l3"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_heading(self):
        text = """# This is heading"""
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_not_a_heading(self):
        text = """#This is heading"""
        self.assertNotEqual(block_to_block_type(text), BlockType.HEADING)

    def test_quote(self):
        text = """>This is heading"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
        text = """> This is heading"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_code(self):
        text = """```This is code block```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

if __name__ == "__main__":
    unittest.main()