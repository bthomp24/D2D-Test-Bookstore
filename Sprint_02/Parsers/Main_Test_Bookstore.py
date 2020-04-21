import requests
import re

import Parsers.Parent_Scrape as Par_Scrape

import time

from PIL import Image
import urllib.request, io

from datetime import date

import mechanize

from bs4 import BeautifulSoup

import concurrent.futures

class book_site_test_bookstore():
    def __init__(self, *args, **kwargs):
        pass
    
    
    def find_book_matches_at_site(self, book_data):
        """
        args:
            book_data (requests.get):
                represents search terms and is needed to fill out 
                the test bookstore web form.
        returns:
            relevancy_list ([[[SiteBookData],float]]):
                relevancy_list is a list of lists including
                a float and SiteBookData, with the float
                representing how closely the SiteBookData
                matches the original search terms (book_data).
        synopsis:
            The purposes of this function is to:
                1)  Use Mechanize to get relevant book detail
                    links from the text bookstore.
                2)  Parse SiteBookData based on those links.
                3)  Put SiteBookData into a list sorted based
                    similar it is to the original search terms,
                    along with a float that quantifies that
                    similarity.
        """

        br = mechanize.Browser()
        try:
            response = br.open('http://localhost:8000/bookstore/')
        except:
            print("\nError accessing Test Bookstore. Please make sure it is running.\n")
            return None

        br.select_form(nr=0)
        control = br.form.find_control("searcher")
        if control.type != "text":
            return None
        searchString = ''
        if ((book_data[1] != None) or (book_data[4] != None) or (book_data[9] != None)):
            
            if (book_data[1] != None):
                searchString += book_data[1] + ' '

            if (book_data[4] != None):
                searchString += book_data[4] + ' '

            if (book_data[9] != None):
                searchString += book_data[9]
        else:
            return None

        control.value = searchString
        br.submit()

        #print(br.geturl())

        relevant_book_links = self._navigate_pages(br,3)

        site_book_data_list = []

        #get site_book_data from book_links and place into list
        with concurrent.futures.ThreadPoolExecutor() as executor:
            Future_Threads = []
            for book_link in relevant_book_links:
                Future_Threads.append(executor.submit(self.get_book_data_from_site, book_link))
            
            for future in concurrent.futures.as_completed(Future_Threads):
                site_book_data_list.append(future.result())


        '''
        for book_link in relevant_book_links:
            site_book_data_list.append(self.get_book_data_from_site(book_link))
        '''
        #sort by relevancy
        return Par_Scrape.site_book_data_relevancy(book_data, site_book_data_list)

    
    def get_book_data_from_site(self, url):
        """
        args:
            url (String):
                Test Bookstore book url to be parsed
        returns:
            SiteBookData (List):
                format (String): 
                book_title (String):
                book_image:~
                book_image_url:~
                isbn_13 (String):
                description (String):
                series (String):*
                volume_number (Int):*
                subtitle:~
                authors (String):
                book_id (String):
                site_slug (String):
                parse_status (String):
                url (String):
                content (String):
                ready_for_sale (boolean):
                extra:~
        synopsis:
            The purpose of this function is to parse a url of the Test
            Bookstore website.  The url should be a specific book's url,
            in order for the following function to work.
        """

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
        url = None
        content = None
        ready_for_sale = None
        extra = None

        #book_title
        book_title = self._get_book_title(response.content)
        
        #isbn_13
        isbn_13 = self._get_book_isbn_13(response.content)

        #description
        description = self._get_book_description(response.content)
        
        #series
        series = self._get_book_series(response.content)

        #volume_number
        volume_number = self._get_book_volume_number(response.content)

        #authors
        authors = self._get_book_authors(response.content)

        #url
        url = self._get_book_url(response.content)

        #site_slug
        site_slug = self._get_book_site_slug()

        #book_id
        book_id = self._get_book_id(response.content)

        #format
        format = self._get_book_format()

        #content
        content = response.content

        #ready_for_sale
        ready_for_sale = self._get_ready_for_sale(response.content)

        #parse_status
        if series == "None" and volume_number == "None":
            parse_status = Par_Scrape.parse_status([format, book_title, isbn_13, description, authors, book_id, site_slug, url, content, ready_for_sale])
        elif series == "None":
            parse_status = Par_Scrape.parse_status([format, book_title, isbn_13, description, volume_number, authors, book_id, site_slug, url, content, ready_for_sale])
        elif volume_number == "None":
            parse_status = Par_Scrape.parse_status([format, book_title, isbn_13, description, series, authors, book_id, site_slug, url, content, ready_for_sale])
        else:
            parse_status = Par_Scrape.parse_status([format, book_title, isbn_13, description, series, volume_number, authors, book_id, site_slug, url, content, ready_for_sale])

        SiteBookData = [format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]

        return SiteBookData

    
    def convert_book_id_to_url(self, book_id):
        """
        args:
            book_id (String):
                This is the unique string that is required to 
                build a working link to the specific book's
                detail page.
        returns:
            url (String):
                This is a working url to the book's detail page.
        synopsis:
            The purpose of this function is to use the passed
            book_id in order to create a link to the specific
            book's detail page.
        """

        primary_url = "http://localhost:8000/bookstore/"
        return primary_url + book_id + "/details"

    
    def _get_book_title(self, content):
        """
        args:
            content (requests.get)
                content is required in order to scrape the book's
                title.
        returns:
            title (String):
                title is the book's title that is being scraped.
        synopsis:
            Thepurpose of this function is to determine what the book's
            title is.
        """

        try:
            return Par_Scrape.parse(content, ".//p[@class='bookTitle']/b")[0].text
        except:
            return None

    
    def _get_book_isbn_13(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to scrape the book's
                isbn_13.
        returns:
            isbn_13 (String):
                isbn_13 is the book's isbn_13 that is being
                scraped.
        synopsis:
            The purpose of this function is to determine the
            book's isbn_13.
        """

        try:
            return Par_Scrape.parse(content,".//tr[td='ISBN 13#:']/td[@class='bookDetail']")[0].text
        except:
            return None
    
    
    def _get_book_description(self, content):
        """
        args:
            content (requests.get):
                content is needed in orde to scrape the book's
                description
        returns:
            description (String):
                description is the book's description that is
                being scraped.
        synopsis:
            The purpose of this function is to determine what
            the book's description
        """

        try:
            description_elements = Par_Scrape.parse(content,".//div[@class='right']/p")[1:]
            description = ""
            for i in range(len(description_elements)):
                if not description_elements[i].text is None:
                    description += description_elements[i].text + ' '
            soup = BeautifulSoup(description, features='lxml')
            description_text = soup.get_text()
            return description_text.strip()
        except:
            return None

    
    def _get_book_series(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to get the series.
        returns:
            series (String):
                series is the book's series
        synopsis:
            The purpose of this function is to determine what the
            series is for the book being scraped (if it exists).
        """

        try:
            return Par_Scrape.parse(content,".//tr[td='Series:']/td[@class='bookDetail']")[0].text
        except:
            return None

    
    def _get_book_volume_number(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to get the volume
                number.
        returns:
            volume_number (Int):
                volume_number is the book's volume_number
        synopsis:
            The purpose of this function is to determine what the
            volume_number is for the book being scraped (if it exists).
        """

        try:
            volume_number = Par_Scrape.parse(content,".//tr[td='Volume#:']/td[@class='bookDetail']")[0].text
            if volume_number == "None":
                return "None"
            else:
                return int(volume_number)
        except:
            return None

    
    def _get_book_authors(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to get the authors
                names.
        returns:
            authors (String):
                authors is the book's authors
        synopsis:
            The purpose of this function is to determine what the
            authors are for the book being scraped.
        """

        try:
            authorsText = Par_Scrape.parse(content,".//tr[td='Author:']/td[@class='bookDetail']")[0].text
            author_array = authorsText.split(',')
            for i in range(len(author_array)):
                author_array[i] = author_array[i].strip()
            authors = ', '
            authors = authors.join(author_array)
            return authors
        except:
            return None
    
    
    def _get_book_url(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to scrape the book's url.
        returns:
            url (String):
                url is book's url that is normally used, as determined
                by the website.
        synopsis:
            The purpose of this function is to determine what the book's
            url is that is being scraped.  This is required in order for
            functions to work properly.
        """

        try:
            return "http://localhost:8000/bookstore/" + Par_Scrape.parse(content,".//tr[td='ISBN 13#:']/td[@class='bookDetail']")[0].text + "/details"
        except:
            return None

    
    def _get_book_site_slug(self):
        """
        args:
            None
        returns:
            site_slug (String):
                site_slug is the book's 'non-static' url, as
                determined by the website
        synopsis:
            The purpose of this function is to determine what the
            book's site_slug is that is being scraped, using the
            book's url.  This site_slug can be used in order to
            create a static url for the book.
        """

        return "TB"

    
    def _get_book_id(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to scrape the book's id.
        returns:
            id (String):
                id is the book's id, as determined by the website
        synopsis:
            The purpose of this function is to determine what the
            book's id that is being scraped.
        """

        try:
            return Par_Scrape.parse(content,".//tr[td='ISBN 13#:']/td[@class='bookDetail']")[0].text
        except:
            return None
    
    
    def _get_book_format(self):
        """
        args:
            None
        returns:
            format (String):
                format is what type of book was scraped
        synopsis:
            The purpose of this function is to determine what kind of
            book is being scraped.
        """

        return "DIGITAL"

    
    def _get_ready_for_sale(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to scrape the book's release
                date.
        returns:
            ready_for_sale (Boolean):
                ready_for_sale is the book's availability, as determined by
                the website
        synopsis:
            The purpose of this function is to determine if the book
            is available or not.
        """

        try:
            release_array = Par_Scrape.parse(content,".//tr[td='Release Date:  ']/td[@class='bookDetail']")[0].text.split('/')
            release_date = date(int(release_array[0]),int(release_array[1]),int(release_array[2]))
            today = date.today()
            return release_date <= today
        except:
            return None

    
    def _navigate_pages(self, br, max_pages=float("inf")):
        """
        args:
            br (Mechanize Browser object):
                br is needed in order to get book detail links
                and follow next page links
            max_pages (Int): *optional*
                defines the max number of pages to get book
                detail links from
        returns:
            links ([String]):
                links is a list of book detail urls as Strings
        synopsis:
            The purpose of this function is get all book detail links
            over a number of pages.
        """

        links = []

        nextLink = None
        pages = 0
        
        for link in br.links():
            if link.text == 'Detail':
                links.append('http://localhost:8000' + link.url)
            if link.text == 'next':
                nextLink = link

        pages += 1

        while not nextLink == None and pages < max_pages:
            br.follow_link(nextLink)

            nextLink = None

            for link in br.links():
                if link.text == 'Detail':
                    links.append('http://localhost:8000' + link.url)
                if link.text == 'next':
                    nextLink = link

            pages += 1

        return links
