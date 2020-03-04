import io
from lxml import etree
import requests
import Parent_Scrape_Threading


class book_site_livraria_cultura(): 

    def __fetch__(self, url):
        response = requests.get(url)
        return response.content

    def __get_title__(self, content):
        return Parent_Scrape_Threading.parse(content, ".//h1[@class='title_product']/div")[0].text

    def __get_subtitle__(self, content):
        subtitle_element = Parent_Scrape_Threading.parse(content, "//*[@class='value-field Subtitulo']")
        if len(subtitle_element)>0:
            subtitle = subtitle_element[0].text
            return subtitle

    def __get_book_image_url__(self, content):
        return Parent_Scrape_Threading.parse(content, "//*[@id='image-main']/@src")[0]

    def __get_isbn__(self, content):
        return Parent_Scrape_Threading.parse(content, "//*[@class='value-field ISBN']")[0].text

    def __get_description__(self, content):
        return Parent_Scrape_Threading.parse(content, "//meta[@itemprop='description']/@content")[0]

    def __get_authors__(self, content):
        authors_element = Parent_Scrape_Threading.parse(content, "//*[@class='value-field Colaborador']")[0]
        authors = authors_element.text
        # authors = authors.replace('Autor:', '')
        # authors = authors.replace('Tradutor:', '')
        # authors = authors.replace('Coordenador/Editor:', '')
        return authors

    def __get_book_id__(self, content):
        book_id = self.__get_url__(content)
        book_id = book_id.replace('https://www3.livrariacultura.com.br/', '')
        book_id = book_id.replace('/p', '')
        return book_id

    def __get_url__(self, content):
        return Parent_Scrape_Threading.parse(content, "//meta[@itemprop='url']/@content")[0]

    # def get_ready_for_sale(content):
    #     return Parent_Scrape.parse(content, "//*[@class='value-field Sinopse']")[0].text

    def get_book_data_from_site(self, url):

        content = self.__fetch__(url)

        format = None
        book_title = None
        book_image = None
        book_image_url = None
        isbn_13 = None
        description = None
        series = None
        volume_number = None
        subtitle = None
        authors = None
        book_id = None
        site_slug = None
        parse_status = None
        url = None
        ready_for_sale = None
        extra = None

        #format
        format = 'DIGITAL'

        #book_title
        book_title = self.__get_title__(content)

        #subtitle
        subtitle = self.__get_subtitle__(content)

        #book_image_url
        book_image_url = self.__get_book_image_url__(content)

        #book_image
        book_image = Parent_Scrape_Threading.get_book_image_from_image_url(book_image_url)

        #isbn_13
        isbn_13 = self.__get_isbn__(content)

        #description
        description = self.__get_description__(content)

        #authors
        authors = self.__get_authors__(content)

        #book_id
        book_id = self.__get_book_id__(content)

        #site_slug
        site_slug = 'LC'

        #url
        url = self.__get_url__(content)

        #ready_for_sale
        ready_for_sale = True


        #price = None

        if subtitle == None:
            parse_list = [format, book_title, book_image, book_image_url, isbn_13, description, authors, book_id, site_slug, url, content, ready_for_sale]
        else:
            parse_list = [format, book_title, book_image, book_image_url, isbn_13, description, subtitle, authors, book_id, site_slug, url, content, ready_for_sale]

        #parse_status
        parse_status = Parent_Scrape_Threading.parse_status(parse_list)

        SiteBookData = [format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]

        return SiteBookData

    def find_book_matches_at_site(self, book_data):
        return None

    def convert_book_id_to_url(self, book_id):
        primary_url = "https://www3.livrariacultura.com.br/"
        return primary_url + book_id + "/p"


URL = "https://www3.livrariacultura.com.br/harry-potter-e-o-prisioneiro-de-azkaban-2010606463/p"
lc = book_site_livraria_cultura()
print(lc.get_book_data_from_site(URL))

print(lc.convert_book_id_to_url('harry-potter-e-o-prisioneiro-de-azkaban-2010606463'))