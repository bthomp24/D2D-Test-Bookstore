import io
from lxml import etree

"""
args:
    response: What you wish to input into an .html file
    target: What you wish to name the .html file
returns:
    NOT APPLICABLE
synopsis:
    This function will take any imput that you place in the first
    parameter, then it will write it to an .html file, which you
    will name using the second parameter.
"""
def write_Response(response, target):
    target = target + ".html"
    text_file = open(target, "w", encoding="utf-8")
    text_file.write(response.text)
    text_file.close()

"""
args:
    text: What you wish to input into a .txt file
    target: What you wish to name the .txt file
returns:
    NOT APPLICABLE
synopsis:
    This function will take any imput that you place in the first
    parameter, then it will write it to an .txt file, which you
    will name using the second parameter.
"""
def write_Txt(text, target):
    target = target + ".txt"
    text_file = open(target, "w", encoding="utf-8")
    text_file.write(text)
    text_file.close()


"""
args:
    content: What you wish to be searched using xpath
    path: what the xpath will use to search the content
returns:
    result: what is returned by the xpath searching the content
synopsis:
    This function will search a the first parameter using the
    second parameter as an xpath.
"""
def parse(content, path):
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root.xpath(path)
