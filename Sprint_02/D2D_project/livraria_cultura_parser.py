import io
from lxml import etree
import requests
import Parent_Scrape_Threading

URL = "https://www3.livrariacultura.com.br/harry-potter-and-philosophy-107221717/p"

def fetch(url):
    response = requests.get(url)
    return response.content

def parse_for_title(content):
    return Parent_Scrape_Threading.parse(content, ".//h1[@class='title_product']/div")[0].text

def parse_for_subtitle(content):
    subtitle_element = Parent_Scrape_Threading.parse(content, "//*[@class='value-field Subtitulo']")
    if len(subtitle_element)>0:
        subtitle = subtitle_element[0].text
        return subtitle

def parse_for_book_image_url(content):
    return Parent_Scrape_Threading.parse(content, "//*[@id='image-main']/@src")[0]

def parse_for_isbn(content):
    return Parent_Scrape_Threading.parse(content, "//*[@class='value-field ISBN']")[0].text

def parse_for_description(content):
    return Parent_Scrape_Threading.parse(content, "//meta[@itemprop='description']/@content")[0]

def parse_for_authors(content):
    authors_element = Parent_Scrape_Threading.parse(content, "//*[@class='value-field Colaborador']")[0]
    authors = authors_element.text
    authors = authors.replace('Autor:', '')
    authors = authors.replace('Tradutor:', '')
    authors = authors.replace('Coordenador/Editor:', '')
    return authors

def parse_for_book_id(content):
    return Parent_Scrape_Threading.parse(content, "//meta[@itemprop='gtin13']/@content")[0]

def parse_for_url(content):
    return Parent_Scrape_Threading.parse(content, "//meta[@itemprop='url']/@content")[0]

# def parse_for_ready_for_sale(content):
#     return Parent_Scrape.parse(content, "//*[@class='value-field Sinopse']")[0].text

content = fetch(URL)
# f = open("html.txt", "wb")
# f.write(content)

book_title = parse_for_title(content)
subtitle = parse_for_subtitle(content)
book_image_url = parse_for_book_image_url(content)
isbn_13 = parse_for_isbn(content)
description = parse_for_description(content)
authors = parse_for_authors(content)
book_id = parse_for_book_id(content)
url = parse_for_url(content)

print('Title: ', book_title)
print('Subtile: ', subtitle)
print('Book Image URL: ', book_image_url)
print('ISBN13: ', isbn_13)
print('Description: ', description)
print('Authors: ', authors)
print('Book ID: ', book_id)
print('URL: ', url)