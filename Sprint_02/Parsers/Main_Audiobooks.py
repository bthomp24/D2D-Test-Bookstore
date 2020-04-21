import io
from lxml import etree
import requests
import Parsers.Parent_Scrape as Par_Scrape

from bs4 import BeautifulSoup

import mechanize
import concurrent.futures


class book_site_audiobooks():
    def __init__(self, *args, **kwargs):
        pass


    def get_book_data_from_site(self, url):
        """
        args:
            url (String):
                Google Books book url to be parsed
        returns:
            SiteBookData (List):
                format (String): 
                book_title (String):
                book_image:~
                book_image_url (String):
                isbn_13 (String):
                description (String):
                series (String):~
                volume_number (String):~
                subtitle (String):~
                authors (String):
                book_id (String):
                site_slug (String):
                parse_status (String):~
                url (String):
                content (String):
                ready_for_sale (boolean):~
                extra:~
        synopsis:
            The purpose of this function is to parse a url of the 
            Audiobooks website. The url should be a specific book's url, in 
            order for the following function to work.
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
        book_url = None
        content = None
        ready_for_sale = None
        extra = None

        # book_title
        book_title = self.__get_book_title(response.content)

        # book_image_url
        book_image_url = self.__get_book_image_url(response.content)

        # book_image
        book_image = Par_Scrape.get_book_image_from_image_url(book_image_url)
        
        # book_isbn_13
        isbn_13 = self.__get_book_isbn_13()

        # description
        description = self.__get_book_description(response.content)

        # series
        series = self.__get_book_series()

        # volume_number
        volume_number = self.__get_book_volume()

        # subtitle
        subtitle = self.__get_book_subtitle()

        # authors
        authors = self.__get_book_authors(response.content)

        # book_url
        book_url = url

        # site_slug
        site_slug = self.__get_book_site_slug()

        # book_id
        book_id = self.__get_book_id(response.url)

        # format
        format = self.__get_book_format()

        # content
        content = response.content

        # ready_for_sale
        ready_for_sale = self.__get_book_sale_status(response.content)

        # parse_status
        parse_status = Par_Scrape.parse_status([format, book_title, book_image, book_image_url, description, authors, book_id, site_slug, url, content, ready_for_sale])
        
        SiteBookData = [format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]

        return SiteBookData



    def find_book_matches_at_site(self, book_data):
        """
        args:
            book_data (List[]):
                book_data that will be used to search the target
                website
        returns:
            site_book_data_list ([[SiteBookData[], rating],...]):
                a list of site_book_data's with their relevant ratings.
        synopsis:
            The purpose of this function is to use a book_data object,
            and then use that to search Audiobooks.com for related
            book_data objects (known as site_book_data objects),
            and then sort them in order of how related they are to
            the book_data object.
        """

        if book_data[0].upper() != "AUDIOBOOK":
            return None

        # getting the search pages for the book data we pass in.    
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
        """
        args:
            book_id (String):
                This is the site_slug that is required to build a
                working link to the website.
        returns:
            url (String):
                This is a working url to the book's website.
        synopsis:
            The purpose of this function is to use the passed
            book_id in order to create a direct url to the book.
        """
        
        primary_url = "https://www.audiobooks.com/audiobook/"
        return primary_url + book_id



    def __get_book_title(self, content):
        """
        args:
            content (requests.get)
                content is required in order to scrape the book's
                title.
        returns:
            title (String):
                title is the book's title that is being scraped.
        synopsis:
            The purpose of this function is to determine what the book's
            title is.
        """

        try:
            return Par_Scrape.parse(content, self.content_table + "//h1[@class='audiobookTitle']/text()")[0]
        except:
            return None


    def __get_book_image_url(self, content):
        """
        args:
            content (requests.get):
                content is required in order to scrape the book image's
                url.
        returns:
            image_url (String):
                image_url is the book's url for the book's cover
                image.
        synopsis:
            This purpose of this function is to determine what the
            url is for the book's cover image.
        """
        try:
            # audiobooks has the image without the front end of an acceptable URL
            tail_url = Par_Scrape.parse(content, self.content_table + "//img[@class='book-cover']/@src")[0]
            full_url = "https:" + tail_url

            return full_url        
        except:
            return None

    def __get_book_isbn_13(self):
        """
        WARNING:
            Audiobooks.com does not offer book_isbn_13 for their books.
            So there will only be a return of None.
        """

        return None

    def __get_book_description(self, content):
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
            description = Par_Scrape.parse(content, self.content_table + "//div[@class='book-description']/p/text()")

            if len(description) > 1:
                true_description = ""

                # removal of HTML. Does miss some '\' characters
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
        """
        WARNING:
            The programmer was unable to determine a way to acquire,
            the book series consistently or to differentiate the series
            from other data.
        """

        return None
    
    def __get_book_volume(self):
        """
        WARNING:
            The programmer was unable to determine a way to acquire,
            the book volume consistently or to differentiate the series
            from other data.
        """

        return None
    
    def __get_book_subtitle(self):
        """
        WARNING:
            Audiobooks.com does not offer a subtitle attribute for an audiobook.
            All are assigned the same thing.
        """

        return None

    def __get_book_authors(self, content):
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
            authors = Par_Scrape.parse(content, self.content_table + "//h4[@class='book-written-by']//a/text()")
            
            if len(authors) > 1:
                all_authors = ""
                for writer in authors:
                    
                    if writer == authors[-1]:
                        all_authors += writer
                    else:
                        all_authors += writer + ", "    
                return all_authors

            # purpose of return format is due to object list incase more than one author.
            return authors[0]
        except:
            return None

    def __get_book_url(self, bigger_url):
        """
        args:
            bigger_url (String):
                The current URL of the book.
        returns:
            url (String):
                url is book's url that is normally used, as determined
                by the website.
        synopsis:
            The purpose of this function is to determine what the book's
            url is that is being scraped. This function shortens the URL
            to it's defining book ID and is not needed for other functions
            to work properly.
        """

        # constructing the url by fragmenting it's end off and adding it to the basic url.
        fragmented = bigger_url.split('/')
        final_url = "https://www.audiobooks.com/audiobook/" + fragmented[-1]
        return final_url

    def __get_book_site_slug(self):
        """
        args:
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

        return "AU"

    def __get_book_id(self, url):
        """
        args:
            url (String):
                site_slug is used to scrape the book's id
        returns:
            id (String):
                id is the book's id, as determined by the website.
        synopsis:
            The purpose of this function is to determine what the
            book's id that is being scraped, using the already
            url and seperates the id from it to return.
        """

        try:
            # retrieving the id part of the URL
            fragmented = url.split('/')
            return fragmented[-1]
        except:
            return None

    def __get_book_format(self):
        """
        args:
        returns:
            format (String):
                format is what type of book was scraped
                google books only has E-books available on their
                own site.
        synopsis:
            The purpose of this function is to return the book format
            "AUDIOBOOK" since Audiobooks.com only sells audiobook format.
        """

        return "AUDIOBOOK"

    def __get_book_sale_status(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to scrape the book's
                subtitle
        returns:
            sale_status (Boolean):
                the sales status of the book that is being scraped.
        synopsis:
            The purpose of this function is to determine if the
            book is available for sale.
        """

        try:
            if Par_Scrape.parse(content, self.content_table + "//span[@class='nonmember-notify save-later-text']"):
                return False
            else:
                return True
        except:
            return None

    def __get_book_sale_price(self, content):
        """
        args:
            content (Request.get):
                content is needed in order to scrape the audiobook's
                price if applicable
        returns:
            price:
                This is this price of the ebook.
            (None):
                If there is no ebook for the book searched.
        synopsis:
            The purpose of this function is to parse the to scrape
            for the audiobook's price and return it if applicable.
        """
        try:
            return Par_Scrape.parse(content, self.content_table + "//div[@class='fleft button-text']/div/p/text()")
        except:
            return None

    # optionals functions that can be implemented based on audiobooks.com data
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
        """
        args:
            url (String):
                This is the link to the search page that is going
                to be parsed for relevant book links
        returns:
            relevant_urls[]:
                This is a list of links that is located on the url
                that is passed.
            (None):
                This is returned if the url passed is not an
                acceptable input.
        synopsis:
            The purpose of this function is to parse the url that is
            passed, and search for book url's dependent upon the url.
            It will return a list of the book url's formatted to take
            the browser directly to the book source.
        """

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

            
    
    def __site_search_url(self, search):
        """
        args:
            search (String):
                This is the parameter that will be searched for in the
                bookstore
        returns:
            link (String):
                This is the link that was generated based upon the
                search parameter
            None
        synopsis:
            The purpose of this function is to format the search
            query into a valid URL for audiobooks.com.
        """

        start = "https://www.audiobooks.com/search/book/"

        # process for replacing certain characters to fit the constructed URL of the search page.
        end = search.replace(" ", "%20").replace(".", "%20").replace("!", "%20").replace(":", "%20")
        return start + end



    def __get_search_link_from_book_data_form(self, book_data):
        """
        args:
            book_data (List[]):
                The search that will be determined based upon the data
                that is passed in from book_data.
        returns:
            links (list[]):
                A list of search links that can be parsed for results
        synopsis:
            The purpose of this function is to return the search
            link that can be parsed for individual book links, 
            depending on what is passed in the book_data.
        """

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