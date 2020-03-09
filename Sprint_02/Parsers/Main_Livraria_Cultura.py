import io
from lxml import etree
import requests
import Parsers.Parent_Scrape as Par_Scrape
import mechanize

import concurrent.futures

class book_site_livraria_cultura(): 

    def __fetch__(self, url):
        response = requests.get(url)
        return response.content

    def __get_title__(self, content):
        return Par_Scrape.parse(content, ".//h1[@class='title_product']/div")[0].text

    def __get_subtitle__(self, content):
        subtitle_element = Par_Scrape.parse(content, "//*[@class='value-field Subtitulo']")
        if len(subtitle_element)>0:
            subtitle = subtitle_element[0].text
            return subtitle

    def __get_book_image_url__(self, content):
        return Par_Scrape.parse(content, "//*[@id='image-main']/@src")[0]

    def __get_isbn__(self, content):
        return Par_Scrape.parse(content, "//*[@class='value-field ISBN']")[0].text

    def __get_description__(self, content):
        return Par_Scrape.parse(content, "//meta[@itemprop='description']/@content")[0]

    def __get_authors__(self, content):
        authors_element = Par_Scrape.parse(content, "//*[@class='value-field Colaborador']")[0]
        authors = authors_element.text
        author = authors.split("Autor:")[-1]
        
        return author

    def __get_book_id__(self, content):
        book_id = self.__get_url__(content)
        book_id = book_id.replace('https://www3.livrariacultura.com.br/', '')
        book_id = book_id.replace('/p', '')
        return book_id

    def __get_url__(self, content):
        return Par_Scrape.parse(content, "//meta[@itemprop='url']/@content")[0]

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
        book_image = Par_Scrape.get_book_image_from_image_url(book_image_url)

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
        parse_status = Par_Scrape.parse_status(parse_list)

        SiteBookData = [format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]

        return SiteBookData

    def __is_search_valid(self, search):
        #https://www3.livrariacultura.com.br/busca/?ft=test&originalText=what%20am%20i%20testing
        original_link = "https://www3.livrariacultura.com.br/"
        num_books = "?PS=48"
        search = search.replace(" ", "%20")
        link = original_link + search + num_books

        response = requests.get(link)
        if "Nenhum produto encontrado para sua pesquisa por" in response.text:
            return None

        return link

    def __get_search_link_from_book_data(self, book_data):
        book_title = book_data[1]
        book_ISBN = book_data[4]
        book_author = book_data[9]

        links = []

        if (book_title != None) or (book_ISBN != None) or (book_author != None):
            if book_ISBN != None:
                result0 = self.__is_search_valid(book_ISBN)
                if result0 != None:
                    links.append(result0)
                
            if book_title != None:
                result1 = self.__is_search_valid(book_title)
                if result1 != None:
                    links.append(result1)
            
            if book_author != None:
                result2 = self.__is_search_valid(book_author)
                if result2 != None:
                    links.append(result2)
        else:
            return None

        return links

    def __get_book_links_froms_search_site(self, url):
        content = self.__fetch__(url)
        return Par_Scrape.parse(content, ".//h2[@class='prateleiraProduto__informacao__nome']/a/@href")

    def find_book_matches_at_site(self, book_data):
        urls_gotten_from_form = self.__get_search_link_from_book_data(book_data)

        if not urls_gotten_from_form:
            return None

        site_book_data_total = []

        for url in urls_gotten_from_form:
            relevant_book_links = self.__get_book_links_froms_search_site(url)
            if relevant_book_links != None:
                site_book_data_list = []

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    Future_Threads = []
                    for book_link in relevant_book_links:
                        Future_Threads.append(executor.submit(self.get_book_data_from_site, book_link))

                    for future in concurrent.futures.as_completed(Future_Threads):
                        site_book_data_list.append(future.result())
                site_book_data_total += site_book_data_list

        cleaned_book_links = []
        cleaned_site_book_data_total = []
        for site_book in site_book_data_total:
            if site_book[13] not in cleaned_book_links:
                cleaned_book_links.append(site_book[13])
                cleaned_site_book_data_total.append(site_book)
        
        return Par_Scrape.site_book_data_relevancy(book_data, cleaned_site_book_data_total)

    def convert_book_id_to_url(self, book_id):
        primary_url = "https://www3.livrariacultura.com.br/"
        return primary_url + book_id + "/p"