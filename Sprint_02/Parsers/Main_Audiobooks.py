import io
from lxml import etree
import requests
import Parent_Scrape as Par_Scrape

from bs4 import BeautifulSoup

import mechanize
import concurrent.futures

# URL = "https://www.audiobooks.com/search/book/flip"
URL = "https://www.audiobooks.com/audiobook/146247"
# URL = "https://www.audiobooks.com/audiobook/good-omens-the-bbc-radio-4-dramatisation/331959"
class book_site_audiobooks():
    def __init__(self, *args, **kwargs):
        self.content_table = "//*[@id='content']"
        pass
    def get_book_data_from_site(self, url):
        response = requests.get(url)
        

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
        book_url = None
        content = None
        ready_for_sale = None
        extra = None

       
        title = self.__get_book_title(response.content)
        book_image_url = self.__get_book_image_url(response.content)
        book_image = Par_Scrape.get_book_image_from_image_url(book_image_url)
        isbn_13 = self.__get_book_isbn_13()
        description = self.__get_book_description(response.content)
        series = self.__get_book_series()
        volume_number = self.__get_book_volume()
        subtitle = self.__get_book_subtitle()
        authors = self.__get_book_authors(response.content)

        format = self.__get_book_format()

    # Change url to Site Book Data when you prepare for the bar searching.
    def find_book_matches_at_site(self, url):
        results = self.__get_book_links_from_Search_site(url)


    def convert_book_id_to_url(self, book_id):
        primary_url = "https://www.audiobooks.com/audiobook/"
        return primary_url + book_id



    def __get_book_title(self, content):
        try:
            return Par_Scrape.parse(content, self.content_table + "//h1[@class='audiobookTitle']/text()")
        except:
            return None

    def __get_book_image_url(self, content):
        try:
            return Par_Scrape.parse(content, self.content_table + "//img[@class='book-cover']/@src")           
        except:
            return None

    def __get_book_isbn_13(self):
        return None

    def __get_book_description(self, content):
        try:
            description = Par_Scrape.parse(content, self.content_table + "//div[@class='book-description']/p/text()")

            if len(description) > 1:
                true_description = ""

                for part in description:
                    soup = BeautifulSoup(part, features='lxml')
                    text_part = soup.getText()
                    
                    if text_part != '':
                        true_description += text_part + " "
                return true_description

            return description[0]
        except:
            return None

    def __get_book_series(self):
        return None
    
    def __get_book_volume(self):
        return None
    
    def __get_book_subtitle(self):
        return None

    def __get_book_authors(self, content):
        try:        
            authors = Par_Scrape.parse(content, self.content_table + "//h4[@class='book-written-by']//a/text()")
            
            if len(authors) > 1:
                all_authors = ""
                for writer in authors:
                    
                    if writer == authors[-1]:
                        all_authors += writer
                    else:
                        all_authors += writer + ", "    
                return all_authors

            return authors[0]
        except:
            return None

    # work on this when you do the search page
    def __get_book_url():
        pass 

    def __get_book_site_slug(self):
        return "AU"

    def __get_book_id(self, url):
        fragmented = url.split('/')

        print(fragmented[-1])
        return fragmented[-1]

    def __get_book_format(self):
        return "AUDIOBOOK"

    def __get_book_sale_status(self, content):
        pass

    def __get_book_sale_price(self, content):
        pass
    
    # optionals I may do
    ########################################    
    def __get_book_narrators(self, content):
        pass

    def __get_book_duration(self, content):
        pass

    def __get_book_publisher(self, content):
        pass

    def __get_book_genre(self, content):
        pass
    ########################################


    def __get_book_links_from_Search_site(self, url):
        response = requests.get(url)

        collected_urls = Par_Scrape.parse(response.content, ("//*[@class='browseContainer__bookItem flexer']/a/@href"))
        relevant_urls = []

        # if no search results are found.
        if len(collected_urls) == 0:
            return None


        for proper_link in collected_urls:
            relevant_urls.append(proper_link)

        print(relevant_urls)
        return relevant_urls



audiob = book_site_audiobooks()

audiob.get_book_data_from_site(URL)
# audiob.find_book_matches_at_site(URL)
# rip = requests.get(URL)
# Par_Scrape.write_Response(rip, "SearchFlip")