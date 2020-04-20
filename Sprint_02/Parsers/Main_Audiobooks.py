import io
from lxml import etree
import requests
import Parsers.Parent_Scrape as Par_Scrape

from bs4 import BeautifulSoup

import mechanize
import concurrent.futures


# Be sure to do try and except stuff when it comes to parsing and stuff.

# URL = "https://www.audiobooks.com/audiobook/untitled-a-court-of-thorns-and-roses-6/370201"
# URL = "https://www.audiobooks.com/"
# URL = "https://www.audiobooks.com/search/book/flip"
# URL = "https://www.audiobooks.com/audiobook/146247"
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

       
        book_title = self.__get_book_title(response.content)
        book_image_url = self.__get_book_image_url(response.content)
        book_image = Par_Scrape.get_book_image_from_image_url(book_image_url)
        isbn_13 = self.__get_book_isbn_13()
        description = self.__get_book_description(response.content)
        series = self.__get_book_series()
        volume_number = self.__get_book_volume()
        subtitle = self.__get_book_subtitle()
        authors = self.__get_book_authors(response.content)
        book_url = url
        site_slug = self.__get_book_site_slug()
        book_id = self.__get_book_id(response.url)

        format = self.__get_book_format()
        content = response.content
        ready_for_sale = self.__get_book_sale_status(response.content)

        parse_status = Par_Scrape.parse_status([format, book_title, book_image, book_image_url, description, authors, book_id, site_slug, url, content, ready_for_sale])
        SiteBookData = [format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]

        return SiteBookData

    # Change url to Site Book Data when you prepare for the bar searching.
    def find_book_matches_at_site(self, book_data):
        if book_data[0].upper() != "AUDIOBOOK":
            return None
            
        url_gotten_from_form = self.__get_search_link_from_book_data_form(book_data)

        # check to ensure search page exists
        if not url_gotten_from_form:
            return None

        site_book_data_total = []

        for url in url_gotten_from_form:

            relevant_book_links = self.__get_book_links_from_Search_site(url)
            if relevant_book_links != None:
                site_book_data_list = []

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_threads = []

                    for book_link in relevant_book_links:
                        future_threads.append(executor.submit(self.get_book_data_from_site, book_link))

                    for future in concurrent.futures.as_completed(future_threads):
                        site_book_data_list.append(future.result())
                site_book_data_total += site_book_data_list
        
        return Par_Scrape.site_book_data_relevancy(book_data, site_book_data_total)


    def convert_book_id_to_url(self, book_id):
        primary_url = "https://www.audiobooks.com/audiobook/"
        return primary_url + book_id



    def __get_book_title(self, content):
        try:
            return Par_Scrape.parse(content, self.content_table + "//h1[@class='audiobookTitle']/text()")[0]
        except:
            return None

    def __get_book_image_url(self, content):
        try:
            tail_url = Par_Scrape.parse(content, self.content_table + "//img[@class='book-cover']/@src")[0]
            full_url = "https:" + tail_url

            return full_url        
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
    def __get_book_url(self, bigger_url):
        fragmented = bigger_url.split('/')
        final_url = "https://www.audiobooks.com/audiobook/" + fragmented[-1]
        return final_url

    def __get_book_site_slug(self):
        return "AU"

    # Not been tested yet.
    def __get_book_id(self, url):
        try:
            fragmented = url.split('/')
            return fragmented[-1]
        except:
            return None

    def __get_book_format(self):
        return "AUDIOBOOK"

    def __get_book_sale_status(self, content):
        try:
            if Par_Scrape.parse(content, self.content_table + "//span[@class='nonmember-notify save-later-text']"):
                return False
            else:
                return True
        except:
            return None

    # Not implemented in extra or as another option yet
    def __get_book_sale_price(self, content):
        try:
            return Par_Scrape.parse(content, self.content_table + "//div[@class='fleft button-text']/div/p/text()")
        except:
            return None

    # optionals functions I may do
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
        try:
            response = requests.get(url)

            collected_urls = Par_Scrape.parse(response.content, ("//*[@class='browseContainer__bookItem flexer']/a/@href"))
            relevant_urls = []

            # if no search results are found.
            if len(collected_urls) == 0:
                return None


            for proper_link in collected_urls:
                relevant_urls.append(proper_link)

            return relevant_urls
        except:
            return None

            
    # Change this to be a URL construction function for making it rather than actually using Mechanize.
    # starting point below
    """
    start = "https://www.audiobooks.com/search/book/"
    end = title.replace(" ", "%20")
    return start + end
    """
    def __site_search_url(self, search):
        start = "https://www.audiobooks.com/search/book/"

        # Add more of these replace statements as you discover more stuff to replace.
        # if it becomes too many, you may need to make it a for loop or something like that.
        end = search.replace(" ", "%20").replace(".", "%20").replace("!", "%20").replace(":", "%20")
        return start + end



    def __get_search_link_from_book_data_form(self, book_data):

        book_title = book_data[1]
        book_author = book_data[9]

        # our string for the form
        book_search = ""
        links = []

        if(book_title != None) or (book_author != None):

            if book_title != None:
                resultZero = self.__site_search_url(book_title)
                if resultZero != None:
                    links.append(resultZero)

            if book_author != None:
                resultOne = self.__site_search_url(book_author)
                if resultOne != None:
                    links.append(resultOne)
        return links
        


# book_data = ["audiobook", "flip", None, None, "9781423389309", None, None, None, None, "Patrick Roghfuss", None, "au", None, None, None, None, None]
# audiob = book_site_audiobooks()

# audiob.get_book_data_from_site(URL)
# audiob.find_book_matches_at_site(book_data)
# rip = requests.get(URL)
# Par_Scrape.write_Response(rip, "ComingSoon")