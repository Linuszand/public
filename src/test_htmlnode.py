import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node = HTMLNode("h1", "hi", None, {"class": "derp"})
        self.assertEqual(node.props_to_html(), ' class="derp"')

    def test_repr(self):
        children = [
                HTMLNode("p", "hi", None, None),
                HTMLNode("h1", "Welcome", None, None)
                ]
        node = HTMLNode("div", None, children, {"class": "greetings"})
        self.assertEqual(node.__repr__(), "HTMLNode(div, None, [HTMLNode(p, hi, None, None), HTMLNode(h1, Welcome, None, None)], {'class': 'greetings'})")
if __name__ == "__main__":
    unittest.main()


