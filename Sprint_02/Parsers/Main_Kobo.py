
import re
import io
from lxml import etree
import requests
import Parsers.Parent_Scrape as Par_Scrape
import urllib.request, io
from bs4 import BeautifulSoup
from datetime import date, datetime

from PIL import Image

import mechanize

class book_site_kobo():
    def __init__(self, *args, **kwargs):
        pass

    """
    args:
        url (String):
            Kobo book url to be parsed
    returns:
        SiteBookData (List):
            format (String): 
            book_title (String):
            book_image:~
            book_image_url (String):
            isbn_13 (String):
            description (String):
            series (String):~
            volume_number (Int):~
            subtitle (String):~
            authors (String):
            book_id:
            site_slug (String):
            parse_status (String):~
            url (String):
            content (String):
            ready_for_sale (boolean):~
            extra:~
    synopsis:
        The purpose of this function is to parse a url of the Kobo
        website.  The url should be a specific book's url, in order
        for the following function to work.  This function works with
        both digital books and audio books.
    """
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
        url = None
        content = None
        ready_for_sale = None
        extra = None

        #book_title
        book_title = self.__get_book_title(response.content)

        #book_image_url
        book_image_url = self.__get_book_image_url(response.content)

        #book_image
        book_image = Par_Scrape.get_book_image_from_image_url(book_image_url)
        
        #isbn_13
        isbn_13 = self.__get_book_isbn_13(response.content)

        #description
        description = self.__get_book_description(response.content)
        
        #series
        series = self.__get_book_series(response.content)

        #volume_number
        volume_number = self.__get_book_volume_number(response.content)

        #subtitle
        subtitle = self.__get_book_subtitle(response.content)

        #authors
        authors = self.__get_book_authors(response.content)

        #url
        url = self.__get_book_url(response.content)

        #site_slug
        site_slug = self.__get_book_site_slug()

        #book_id
        book_id = self.__get_book_id(response.content)

        #format
        book_format = self.__get_book_format(response.content)

        #content
        content = response.content

        #ready_for_sale
        ready_for_sale = self.__get_book_availability(response.content)
 

        #parse_status
        parse_status = Par_Scrape.parse_status([book_format, book_title, book_image, book_image_url, isbn_13, description, authors, book_id, site_slug, url, content, ready_for_sale])

        SiteBookData = [book_format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]

        return SiteBookData

    """
    args:
        book_data (List):
            This is a list that has various book attirbutes retrieed from the user.
    returns:
        Par_Scrape.site_book_data_relevancy(book_data, site_book_data_list) (List):
            This list of all the relevant books sorted using relevency rating.
    synopsis:
        The purpose of this function is to create a list of relevent books
        sorted using the relevancy rating.
    """

    def find_book_matches_at_site(self, book_data):
    
        site_book_data_list = []

        url = self.get_search_link_from_book_data_form(book_data)
        if url == None:
            return None
        #get the links from 4 pages of search results

        for i in range(1,5):

            # Perform whatever form making for the website in order to get a relevant search link
            url_gotten_from_form = url + "&pageNumber=" + str(i)
            response = requests.get(url_gotten_from_form)
            content = response.content

            #Get relevant book links
            relevant_book_links = self.__get_book_links_from_search_site(content)

            if relevant_book_links != None:

                #get site_book_data from book_links and place into list
                for book_link in relevant_book_links:
                    site_book_data_list.append(self.get_book_data_from_site(book_link))

            #sort by relevancy
        return Par_Scrape.site_book_data_relevancy(book_data, site_book_data_list)

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
        book_id in order to create a final book url.
    """
    def convert_book_id_to_url(self, book_id):
        primary_url = "https://www.kobo.com/us/en/"
        return primary_url + book_id

    """
    args:
        month (String):
            month to be converted to an integer for purposes of
            comparing.
    returns:
        month_num (Number):
            the number that is related to the month that was
            passed
    synopsis:
        The purpose of this function is to return the number
        of a specific month that it is passed, so that it
        may be used for comparison purposes.
    """
    def __score_month(self,month):
        try:
            if (month == "January") or (month =="Jan"):
                return 1
            elif (month == "Febuary") or (month == "Feb"):
                return 2
            elif (month == "March") or (month == "Mar"):
                return 3
            elif (month == "April") or (month == "Apr"):
                return 4
            elif (month == "May"):
                return 5
            elif month == "June" or (month == "Jun"):
                return 6
            elif month == "July" or (month == "Jul"):
                return 7
            elif month == "August" or (month == "Aug"):
                return 8
            elif month == "September" or (month == "Sep"):
                return 9
            elif month == "October" or (month == "Oct"):
                return 10
            elif month == "November" or (month == "Nov"):
                return 11
            elif month == "December" or (month == "Dec"):
                return 12
            else:
                return 0
        except:
                return 0
    
    """
    args:
        content (requests.get)
            content is required in order to scrape the book's
            availability.
    returns:
        Bool:
            Tell if the book is available to be purchased.
    synopsis:
        The purpose of this functin is to confirm that the book is for sale.
    """    

    def __get_book_availability(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//div[@class = 'bookitem-secondary-metadata']/ul/li[2]/span"
            publish_date_element = root.xpath(xpath)[0]
            publish_date = publish_date_element.text
            soup = BeautifulSoup(publish_date, features='lxml')
            text = soup.get_text()
            text = text.strip()


            converted_date = text.replace(",", "").replace(" ", "-")

            today = date.today().strftime("%b-%d-%Y")
            today_string = str(today)

            #release year is in the future
            #NOT RELEASED
            if(int(today_string.split("-")[2]) < int(converted_date.split("-")[2])):
                return False

            #if the years equal
            if(int(today_string.split("-")[2]) < int(converted_date.split("-")[2])):
                return False

            #if the years equal
            elif(int(today_string.split("-")[2]) == int(converted_date.split("-")[2])):
                publish_month = self.__score_month(converted_date.split("-")[0])
                if publish_month == 0:
                    return None

                today_month = self.__score_month(today_string.split("-")[0])
                if today_month == 0:
                    return None

                #release month is in the future
                #NOT RELEASED
                if today_month < publish_month:
                    return False

                #if the months equal
                elif today_month == publish_month:
                    publish_day = int(converted_date.split("-")[1])
                    today_day = int(today_string.split("-")[1])

                    if today_day < publish_day:
                        return False
                        
                    elif today_day == publish_day:
                        return True

                    elif today_day > publish_day:
                        return True
                        
                    else:
                        return None
                    
                #publish month passed
                elif today_month > publish_month:
                    return True

                #FAIL somewhere
                else:
                    return None

            #if the publish date has already passed
            elif(int(today_string.split("-")[2]) > int(converted_date.split("-")[2])):
                return True

            else:
                return None
        except:
            return None      

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
    def __get_book_title(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            title_element = root.xpath(".//span[@class ='title product-field']")[0]
            title = title_element.text
            soup = BeautifulSoup(title, features='lxml')
            text = soup.get_text()
            return text
        except:
            return None

    """
    args:
        content (requests.get):
            content is required in order to scrape the book's cover
            image url.
    returns:
        image_url (String):
            image_url is the book's url for the book's cover
            image.
    synopsis:
        This purpose of this function is to determine what the
        url is for the cover image.
    """
    def __get_book_image_url(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//img[@class = 'cover-image  notranslate_alt']/@src"
            book_image_url_element = root.xpath(xpath)[0]
            book_image_url = "https:" + str(book_image_url_element)
            return book_image_url
        except:
            return None
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
    def __get_book_isbn_13(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//div[@class = 'bookitem-secondary-metadata']/ul/li[4]/span"
            isbn_element = root.xpath(xpath)[0]
            isbn13 = isbn_element.text
            return isbn13
        except:
            return None
    
    """
    args:
        content (requests.get):
            content is needed in order to scrape the book's
            description
    returns:
        description (String):
            description is the book's description that is
            being scraped.
    synopsis:
        The purpose of this function is to determine what
        the book's description
    """
    def __get_book_description(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//div[@class = 'synopsis-description']"
            description_element = root.xpath(xpath)[0]
            description = etree.tostring(description_element, encoding = 'utf8', method = 'xml')
            soup = BeautifulSoup(description, features='lxml')
            text = soup.get_text()
            return text
            
        except:
            return None

    """
    args:
        content (requests.get):
            content is needed in order to scrape the book's
            series title
    returns:
        series_title (String):
            series_title is the book series title that is
            being scraped if it is exists.
    synopsis:
        The purpose of this function is to determine what
        the series title is.
    """

    def __get_book_series(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//span[@class = 'product-sequence-field']/a"
            series_title__element = root.xpath(xpath)
            if (len(series_title__element)>0):
                series_title__element = root.xpath(xpath)[0]
                series_title = series_title__element.text
            else:
                series_title = 'None'

            return series_title;
        except:
            return None

    """
    WARNING:
        The programmer was unable to determine a way in such,
        that a subtitle could not be scraped.
    """
    def __get_book_volume_number(self, content):
        return None

    """
    WARNING:
        The programmer was unable to determine a way in such,
        that a subtitle could not be scraped.
    """
    def __get_book_subtitle(self, content):
        return None

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
    def __get_book_authors(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//a[@class = 'contributor-name']"
            author_element = root.xpath(xpath)[0]
            author = author_element.text
            return author    
        except:
            return None
    
    """
    args:
        content (requests.get):
            content is needed in order to scrape the book's url.
    returns:
        book_final_url (String):
            book_final_url is book's url that is normally used, as determined
            by the website.
    synopsis:
        The purpose of this function is to determine what the book's
        url is that is being scraped.  This is required in order for
        functions to work properly.
    """
    def __get_book_url(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//meta[@property='og:url']/@content"
            book_final_url_element = root.xpath(xpath)[0]
            book_final_url = book_final_url_element;
            return book_final_url;
        except:
            return None

    """
    args:
        url (String):
            url is used to scrape the book's site_slug
    returns:
        site_slug (String):
            site_slug is the website's ID.
    synopsis:
        The purpose of this function is to determine what the
        book's site_slug is.
    """
    def __get_book_site_slug(self):
        return "KB"

    """
    args:
        content (requests.get):
            content is needed in order to scrape the book's id.
    returns:
        book_id (String):
            id is the book's id, as determined by the website
    synopsis:
        The purpose of this function is to determine what the
        book's id that is being scraped, using the already
        scraped site_slug
    """
    def __get_book_id(self, content):
        try:
            url = self.__get_book_url(content)
            first = "en/"
            last = ""
            start = url.rindex(first) + len(first)
            end = url.rindex(last, start)
            book_id = url[start:end]
            return book_id
        except:
            return None

    

    """
    args:
        content (requests.get):
            content is needed in order to scrape the book's format.
    returns:
        format (String):
            format is what type of book was scraped
    synopsis:
        The purpose of this function is to determine what kind of
        book is being scraped.
    """
    def __get_book_format(self, content):
        try: 
           parser = etree.HTMLParser(remove_pis=True)
           tree = etree.parse(io.BytesIO(content), parser)
           root = tree.getroot()
           xpath = ".//div[@class = 'bookitem-secondary-metadata']/h2"
           book_format_element = root.xpath(xpath)[0]
           book_format = book_format_element.text
           book_format = book_format.split()
           book_format = book_format[0]
           if (book_format == "eBook"): book_format = "DIGITAL"
           elif (book_format =="Audiobook"): book_format = "AUDIOBOOK"
           else:
                book_format = None

           return book_format
        except:
            return None

    """
    args:
        content (request.get):
            Content is required to scarpe the all links in the search results
    returns:
        list_of_matches_urls:
            This is a list of links that is located on the url
            that is passed.
        (None):
            This is returned if the url passed is not an
            acceptable input.
    synopsis:
        The purpose of this function is to parse the url that is
        passed, and search for book url's dependent upon the url.
        It will return a list of the book url's.
    """
    def __get_book_links_from_search_site(self, content):
        try:
            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
            xpath = ".//p[@class='title product-field']/a/@href"
            num_matches = len(root.xpath(xpath))
            list_of_matches_urls = []

            for i in range(num_matches):
                buffer = root.xpath(xpath)[i]
                list_of_matches_urls.append(root.xpath(xpath)[i])
            return list_of_matches_urls
        except:
            return None

    """
    args:
        url (url):
            url is the search page url with all the queries included.
        formatting(String):
            formatting is the string that decides if we are searching for audiobook oe ebook
    returns:
        url:
            url that was passed if no formatting is required
        url + formatting:
            url with the filter using the formatting

        (None):
            This is returned if the url passed is not an
            acceptable input.
    synopsis:
        The purpose of this function is to generate the final search url.
    """

    def __format_mechanize_url(self, formatting, url):
        if formatting == None:
            return url
        else:
            if formatting.lower() == "digital":
                return url + "Book"
            elif formatting.lower() == "audiobook":
                return url + "Audiobook"
            else:
                return url
        return None

    """
    args:
        search (String):
            Search includes all the keywords which will be used to filter the search results

    returns:
        link:
            url that can be used to search for relevant books

        (None):
            if the url is invalid or produces no search results.
    synopsis:
        The purpose of this function is to generate a search url.
    """

    def __Is_Search_Valid(self, search):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        response = br.open("https://www.kobo.com/us/en/search?query=&fcmedia=")

        br.form = list(br.forms())[0]

        control = br.form.controls[0]
        if control.type != "search":
            return None
        
        control.value = search
        br.submit()
        link = br.geturl()

        #Parse and ensure link has results, and does not return a 404 error page
        response = requests.get(link)
        content = response.content
        
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        xpath = ".//p[@class='title product-field']/a/@href"
        num_links = len(root.xpath(xpath))
        if (num_links == 0):
            return None
        else:
            return link

    """
    args:
        book_data (Python List):
            It includes book attributes that will be used as keywords for search purposes.

    returns:
        link:
            url that can be used to search for relevant books

        (None):
            if the url is invalid or produces no search results.
    synopsis:
        The purpose of this function is to generate a search url.
    """

    def get_search_link_from_book_data_form(self, book_data):
        book_title = book_data[1]
        book_ISBN = book_data[4]
        book_author = book_data[9]

        link = ""
        
        was_previous = False

        if (book_title != None) or (book_ISBN != None) or (book_author != None):
            what_to_search = ""
            if book_title != None:
                what_to_search += book_title
                was_previous = True
            if book_ISBN != None:
                if was_previous == False:
                    what_to_search += " "
                what_to_search += book_ISBN
                was_previous = True
            if book_author != None:
                if was_previous == False:
                    what_to_search += " "
                what_to_search += book_author
                was_previous = True
            
            link = self.__Is_Search_Valid(what_to_search)
            if link == None:
                return None

        else:
            return None

        formatted_link = self.__format_mechanize_url(book_data[0], link)

        return formatted_link