import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_to_html(self):
        node = LeafNode("p", "hello", {"class": "greetings"})
        self.assertEqual(node.to_html(), '<p class="greetings">hello</p>')

    def test_to_html_none_val(self):
        node = LeafNode("p", None, None)
        try:
            node.to_html()
        except ValueError:
            pass
        else:
            print('Fail: ValueError was not raised')

    def test_no_tag(self):
        node = LeafNode(None, "Hello!", {"class": "greetings"})
        self.assertEqual(node.to_html(), "Hello!")

if __name__ == "__main__":
    unittest.main()

print('\n\n===================== STARTING TESTS =====================\n')
print("""
              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |     TESTING...        | |
              | |     LOADING...        | |
              | |     DONE?             | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
            ,---\_____     []     _______/------,
          /         /______________\           /|
        /___________________________________ /  | ___
        |                                   |   |    )
        |  _ _ _                 [-------]  |   |   (
        |  o o o                 [-------]  |  /    _)_
        |__________________________________ |/     /  /
    /-------------------------------------/|      ( )/
  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n""")
