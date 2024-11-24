import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    
    def test_to_html(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_children(self):
        node = ParentNode("p", None, None)
        try:
            node.to_html()
        except:
            self.assertRaises(ValueError)
        else:
            print("Fail, ValueError not raised")

    def test_props_working(self):
        node = ParentNode("p", [ LeafNode("b", "hehe", { "class": "laugh" }) ], { "class": "greetings" })
        self.assertEqual(node.to_html(), '<p class="greetings"><b class="laugh">hehe</b></p>')

    def test_nested_lists(self):
        node = ParentNode("p", [ ParentNode( "b", [ LeafNode("b", "Bold Text") ]) ] )
        self.assertEqual(node.to_html(), '<p><b><b>Bold Text</b></b></p>')


if __name__ == "__main__":
    unittest.main()
