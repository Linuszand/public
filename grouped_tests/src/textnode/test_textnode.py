import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
   
    def test_eq(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("hello", TextType.ITALIC)
        node2 = TextNode("huh", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("hello", TextType.BOLD)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()
