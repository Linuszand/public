import unittest
from textnode import TextType, TextNode, text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text(self):
        node = TextNode("Hello", TextType.TEXT)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.value, "Hello")
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.props, None)
        self.assertEqual(htmlnode.children, None)
        self.assertEqual(TextType.TEXT.value, 'text')
    def test_bold(self):
        node = TextNode("Hello", TextType.BOLD)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.value, "Hello")
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.children, None)
        self.assertEqual(htmlnode.props, None)

if __name__ == "__main__":
    unittest.main()
