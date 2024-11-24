import unittest
import logging

from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes

class TestInline(unittest.TestCase):
    
    def test_bold(self):
        old_node = TextNode('Hello, **my** friend!', TextType.TEXT)     
        new_nodes = split_nodes_delimiter([old_node], '**', TextType.BOLD)
        self.assertListEqual([ TextNode("Hello, ", TextType.TEXT), TextNode("my", TextType.BOLD), TextNode(" friend!", TextType.TEXT) ], new_nodes)

    def test_code(self):
        old_node = TextNode('Hello, `my` friend!', TextType.TEXT)     
        new_nodes = split_nodes_delimiter([old_node], '`', TextType.CODE)
        self.assertListEqual([ TextNode("Hello, ", TextType.TEXT), TextNode("my", TextType.CODE), TextNode(" friend!", TextType.TEXT) ], new_nodes)

    def test_italic(self):
        old_node = TextNode('Hello, *my* friend!', TextType.TEXT)     
        new_nodes = split_nodes_delimiter([old_node], '*', TextType.ITALIC)
        self.assertListEqual([ TextNode("Hello, ", TextType.TEXT), TextNode("my", TextType.ITALIC), TextNode(" friend!", TextType.TEXT) ], new_nodes)
    
    # ======= extract_mark_down_images ========
    def test_image(self):
        text = "This is a text with a dog ![Cute dog](https://www.google.com/asd.png) and a cute little kitten ![such cute kitten](https://imgur.com/asd.jpg)"
        assert extract_markdown_images(text) == [("Cute dog", "https://www.google.com/asd.png"), ("such cute kitten", "https://imgur.com/asd.jpg")]

    def test_image_forgot_square_bracket(self):
        text = "This is a text with a dog ![Cute dog(https://www.google.com/asd.png) and a cute little kitten ![such cute kitten(https://imgur.com/asd.jpg)"
        assert extract_markdown_images(text) == []
    def test_image_forgot_paranthesis(self):
        text = "This is a text with a dog ![Cute dog]https://www.google.com/asd.png) and a cute little kitten ![such cute kitten]https://imgur.com/asd.jpg)"
        assert extract_markdown_images(text) == []

    # ======== extract_markdown_links =========
    def test_link(self):
        text = "This is a text with a link to google: [google, my friend](https://google.com)"
        assert extract_markdown_links(text) == [("google, my friend", "https://google.com")]
    
    def test_link_forgot_square_bracket(self):
        text = "This is a text with a link to google: [google, my friend(https://google.com)"
        assert extract_markdown_links(text) == []

    def test_link_forgot_parenthesis(self):
        text = "This is a text with a link to google: [google, my friend](https://google.com"
        assert extract_markdown_links(text) == []
    
    def test_link_extra_brackets(self):
        text = "This is a text with a link to google: [[google, my friend]](https://google.com)"
        assert extract_markdown_links(text) == []

    # ========= split_nodes_link ========
    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node]) 
        self.AssertListEqual = new_nodes, [ TextNode("This is a text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.TEXT), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev" ) ]
    
    def test_split_nodes_link_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_forgot_square_bracket(self):
        node = TextNode("This is a link to google](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("This is a link to google](https://google.com)", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)                                               
    
    def test_split_nodes_link_forgot_parenthesis(self):
        node = TextNode("This is a [link to google]https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("This is a [link to google]https://google.com)", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_number(self):
        node = TextNode(1, TextType.TEXT)
        try:
            new_nodes = split_nodes_link([node])
        except Exception as e:
            print(e)
        else:
            self.assertListEqual(new_nodes, [TextNode(1, TextType.TEXT) ])
    
    def test_split_nodes_link_only_link(self):
        node = TextNode("[link to google](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("link to google", TextType.LINK, "https://google.com") ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_multiple_links(self):
        node = TextNode("[link to google](https://google.com) and [link to google](https://google.com) and [link to google](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("link to google", TextType.LINK, "https://google.com"), TextNode(" and ", TextType.TEXT), TextNode("link to google", TextType.LINK, "https://google.com"), TextNode(" and ", TextType.TEXT), TextNode("link to google", TextType.LINK, "https://google.com") ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_malformed_link(self):
        node = TextNode("[google]))(https://google.com)))][", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("[google]))(https://google.com)))][", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_nested_link(self):
        node = TextNode("[google](https://google.com)(https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [ TextNode("google", TextType.LINK, "https://google.com"), TextNode("(https://google.com)", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)
    
    # ========= split_nodes_image =======
    def test_split_nodes_image(self):
        node = TextNode("This is a text with an image ![Cute cat](https://google.com/asdafkasfoaksf.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [ TextNode("This is a text with an image ", TextType.TEXT), TextNode("Cute cat", TextType.IMAGE, "https://google.com/asdafkasfoaksf.png") ] )
    
    def test_split_nodes_image_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [ TextNode("", TextType.TEXT) ])

    def test_split_nodes_image_forgot_square_bracket(self):
        node = TextNode("This is a text with an image !Cute cat](https://google.com/asdafkasfoaksf.png)", TextType.TEXT) 
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [ TextNode( "This is a text with an image !Cute cat](https://google.com/asdafkasfoaksf.png)", TextType.TEXT)])
    
    def test_split_nodes_image_forgot_parenthesis(self):
        node = TextNode("This is a text with an image ![Cute cat](https://google.com/asdafkasfoaksf.png", TextType.TEXT) 
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [ TextNode( "This is a text with an image ![Cute cat](https://google.com/asdafkasfoaksf.png", TextType.TEXT)])
    
    def test_split_nodes_image_number(self):
        node = TextNode(1, TextType.TEXT)
        try:
            new_nodes = split_nodes_image([node])
        except Exception as e:
            print(e)
        else:
            self.assertListEqual(new_nodes, [TextNode(1, TextType.TEXT) ])

    def test_split_nodes_image_only_image(self):
        node = TextNode("![A cute cat](https://google.com/asfo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [ TextNode("A cute cat", TextType.IMAGE, "https://google.com/asfo.png") ])
    
    def test_split_nodes_image_multiple_images(self):
        node = TextNode("![Cat](https://google.com/asd.png) and ![Cat](https://google.com/asd.png) and ![Cat](https://google.com/asd.png) and ![Cat](https://google.com/asd.png) and ![Cat](https://google.com/asd.png)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        expected = [ TextNode("Cat", TextType.IMAGE, "https://google.com/asd.png"), TextNode(" and ", TextType.TEXT), TextNode("Cat", TextType.IMAGE, "https://google.com/asd.png"), TextNode(" and ", TextType.TEXT), TextNode("Cat", TextType.IMAGE, "https://google.com/asd.png"), TextNode(" and ", TextType.TEXT), TextNode("Cat", TextType.IMAGE, "https://google.com/asd.png"), TextNode(" and ", TextType.TEXT), TextNode("Cat", TextType.IMAGE, "https://google.com/asd.png") ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_image_malformed_link(self):
        node = TextNode("![![Cat]]((https://google.com/asd.png))", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [ TextNode("![![Cat]]((https://google.com/asd.png))", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_image_nested_link(self):
        node = TextNode("![Cat](https://google.com/asd.png)(https://imgur.com/asd.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [ TextNode("Cat", TextType.IMAGE, "https://google.com/asd.png"), TextNode("(https://imgur.com/asd.jpg)", TextType.TEXT) ]
        self.assertListEqual(new_nodes, expected)

    # ============ text_to_textnode ==============
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [ 
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev")
                    ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_bold(self):
        text = "This is a **bold** guy"
        expected = [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" guy", TextType.TEXT)
                ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_italic(self):
        text = "This is an *italic* guy"
        expected = [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" guy", TextType.TEXT)
                ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_code(self):
        text = "This is a `hacker` guy"
        expected = [
                TextNode("This is a ", TextType.TEXT),
                TextNode("hacker", TextType.CODE),
                TextNode(" guy", TextType.TEXT)
                ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_image(self):
        text = "This is an ![Cat](https://boot.dev/asd.png) image"
        expected = [
                TextNode("This is an ", TextType.TEXT),
                TextNode("Cat", TextType.IMAGE, "https://boot.dev/asd.png"),
                TextNode(" image", TextType.TEXT)
                ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_link(self):
        text = "This is a [link](https://boot.dev) link"
        expected = [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" link", TextType.TEXT)
                ]
        self.assertListEqual(text_to_textnodes(text), expected)
    # bold links does not work yet, It just creates a bold textlink 
    def test_text_to_textnodes_bold_link(self):
        text = "**[link](https://boot.dev)**"
        expected = [
                TextNode("[link](https://boot.dev)", TextType.BOLD)
                ]
        self.assertListEqual(text_to_textnodes(text), expected)
if __name__ == "__main__":
    unittest.main()
