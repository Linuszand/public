from pudb import set_trace

from textnode import TextType, TextNode
import re

#def split_nodes_delimiter(old_nodes, delimiter, text_type):
#    set_trace()
#    new_nodes = []
#    inside_delimiter = False
#    for old_node in old_nodes:
#        if old_node.text_type != TextType.TEXT:
#            new_nodes.append(old_node)
#        else:
#            segments = old_node.text.split(delimiter)
#            inside_delimiter = False
#
#            for segment in segments:
#                if inside_delimiter:
#                    new_nodes.append(TextNode(segment, text_type))
#                else:
#                    new_nodes.append(TextNode(segment, TextType.TEXT))
#              
#               inside_delimiter = True
#
#    return new_nodes

def text_to_textnodes(text):
    tnodes = [TextNode(text, TextType.TEXT)]
    tnodes = split_nodes_delimiter(tnodes, "**", TextType.BOLD)
    tnodes = split_nodes_delimiter(tnodes, "*", TextType.ITALIC)
    tnodes = split_nodes_delimiter(tnodes, "`", TextType.CODE)
    tnodes = split_nodes_image(tnodes)
    tnodes = split_nodes_link(tnodes) 
    return tnodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text

def extract_markdown_links(text):
    text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if isinstance(old_node.text, (int, float)):
            raise Exception("You need to enter a string")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        the_text = old_node.text
        get_links = extract_markdown_links(the_text)
        if get_links == []:
            new_nodes.append(old_node)
            continue
        for link in get_links:
            the_split = the_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(the_split) != 2:
                raise Exception("Invalid syntax, you need to close the link properly.")
            if the_split[0] != "":
                new_nodes.append(TextNode(the_split[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            
            the_text = the_split[1]
        if the_text != "":
            new_nodes.append(TextNode(the_text, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = [] # Tom lista
    for old_node in old_nodes: # old_node = varje TextNode objekt in old_nodes listan [ TextNode("Hej, min vän", TextType.TEXT) ]
        if isinstance(old_node.text, (int, float)): # Om TextNode objektets(old_node) text(.text) egenskap är int eller float
            raise Exception("You need to enter a string") # Lyft en error/exception "You need to enter a string"
        if old_node.text_type != TextType.TEXT: # Om old_node.text_type inte är av typen TextType.TEXT
            new_nodes.append(old_node) # lägg in old_node objektet i new_nodes listan
            continue # fortsätt
        the_text = old_node.text # lägger in old_node.text värdet i variabeln the_text
        get_images = extract_markdown_images(the_text) # extraherar bildtext värdet från the_text in i variabeln get_images som en lista med tuples [ (alt_text, image_link), (alt_text, image_link) ]. Det är REGEX magi som gör detta.
        if get_images == []: # om get_images listan är tom
            new_nodes.append(old_node) # lägg till old_node längs back i new_nodes listan
            continue # fortsätt
        for image in get_images: # för varje element i get images, alltså [ (alt_text, image_link) ] - (alt_text, image_link) är det första elementet.
            the_split = the_text.split(f"![{image[0]}]({image[1]})", 1) # delar old_node.text värdet på t.ex. ![to boot dev](https://www.boot.dev/asfasgas.jpg), vilket vi hade en text som var: "hello, here is image: ![to boot dev](https://www.boot.dev/asfasgas.jpg). Enjoy!", så skulle vi få en lista delad på bildtexten: [ "hello, here is image: ","Enjoy!" ]
            if len(the_split) != 2: # om antalet element i the_split inte är 2, då betyder det att det inte finns en bildtext
                raise ValueError("Invalid syntax, you need to close the image properly.") # lyfter en error som säger att bildtexten är ogiltig
            if the_split[0] != "": # om det första elementet i the_split listan inte är tom
                new_nodes.append(TextNode(the_split[0], TextType.TEXT)) # lägg in ett TextNode objekt, med the_split[0](en text) och av typen TEXT, vilket är normal text.
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1])) # Lägger in ett TextNode Objekt i new_nodes image[0] = alt_text, TextType.IMAGE = typen är av IMAGE, image[1] = bildlänken


            the_text = the_split[1] # Ändra the_text till det textvärdet som kommer efter den första bildtexten som vi delade the_text på först. Vilket är "Enjoy!" I det här fallet.
        if the_text != "": # Om the_text variabeln inte är tom
            new_nodes.append(TextNode(the_text, TextType.TEXT)) # lägg in TextNode Objektet, med textvärdet och vilken texttyp det är.
    return new_nodes # Slutligen, ge tillbaka new_nodes listan, som borde se ut så här: [ TextNode("hello, here is image: ", TextType.TEXT), TextNode("alt_text", TextType.IMAGE, "image_link"), TextNode("Enjoy!", TextType.TEXT) ]
  
# node = TextNode("![Cat](https://google.com/asd.png) and ![Cat](https://google.com/asd.png) and ![Cat](https://google.com/asd.png) and ![Cat]#(https://google.com/asd.png) and ![Cat](https://google.com/asd.png)", TextType.TEXT)
#new_nodes = split_nodes_image([node])


