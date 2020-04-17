import requests
import re
import concurrent.futures

import Parsers.Parent_Scrape as Par_Scrape

from datetime import date, datetime

from PIL import Image

import mechanize

class book_site_scribd():
    def __init__(self, *args, **kwargs):
        self.meta_Father_Type = ".//meta[@property='og:type']"
        self.columns_container = ".//div[@class='columns_container']"
        self.right_col = self.columns_container + "/section[@class='right_col']" 
        self.details = ".//span[@class='meta_label']/span"


    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   The following is a list of public functions that are designed               
                                  to be used outside of this class                              
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    
    def get_book_data_from_site(self, url):
        """
        args:
            url (String):
                Scribd book url to be parsed
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
            The purpose of this function is to parse a url of the Scribd
            website.  The url should be a specific book's url, in order
            for the following function to work.  This function works with
            both digital books and audio books.
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
        book_id = self.__get_book_id(url)

        #ready_for_sale
        ready_for_sale = self.__get_book_availability(response.content)

        #format
        format = self.__get_book_format(url)

        #content
        content = response.content

        #parse_status
        parse_status = Par_Scrape.parse_status([format, book_title, book_image, book_image_url, isbn_13, description, authors, book_id, site_slug, url, content, ready_for_sale])

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
            and then use that to search Scribd.com for related
            book_data objects (known as site_book_data objects),
            and then sort them in order of how related they are to
            the book_data object.
        """

        # Perform whatever form making for the website in order to get a relevant search link
        #url_gotten_from_form = "https://www.scribd.com/search?content_type=books&page=1&query=name%20of%20the%20wind&language=1"
        url_gotten_from_from = self.__get_search_link_from_book_data_form(book_data)
        
        if not url_gotten_from_from:
            return None
        
        ''' \/\/ the following should not change \/\/ '''
        
        #print("url_gotten_from_form: ", url_gotten_from_from)

        site_book_data_total = []

        for url in url_gotten_from_from:
            relevant_book_links = self.__get_book_links_from_search_site(url)
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
            book_id in order to create 
        """

        primary_url = "https://www.scribd.com/book/"
        return primary_url + book_id

    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   The following is a list of private functions that are designed               
                               to never be used outside of this class                           
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    
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
            Thepurpose of this function is to determine what the book's
            title is.
        """

        try:
            return Par_Scrape.parse(content, (self.meta_Father_Type + "/following-sibling::meta[@property='og:title']/@content"))[0]
        except:
            return None
    
    
    def __get_book_image_url(self, content):
        """
        args:
            content (requests.get):
                content is required in order to scrape the book's
                url.
        returns:
            image_url (String):
                image_url is the book's url for the book's cover
                image.
        synopsis:
            This purpose of this function is to determine what the
            book's url is for the cover image.
        """

        try:
            return Par_Scrape.parse(content, (self.meta_Father_Type + "/following-sibling::meta[@property='og:image']/@content"))[0]
        except:
            return None

    
    def __get_book_isbn_13(self, content):
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
            return Par_Scrape.parse(content, (self.meta_Father_Type + "/following-sibling::meta[@property='books:isbn']/@content"))[0]
        except:
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
            return Par_Scrape.parse(content, (self.meta_Father_Type + "/following-sibling::meta[@property='og:description']/@content"))[0].replace("\n", "").replace("\t", "").replace("\'", "").replace("\xa0", " ")
        except:
            return None

    
    def __get_book_series(self, content):
        """
        WARNING:
            The programmer was unable to determine a way in such,
            that a series could not be scraped.
        """

        return None

    
    def __get_book_volume_number(self, content):
        """
        WARNING:
            The programmer was unable to determine a way in such,
            that a volume number could not be scraped.
        """

        return None

    
    def __get_book_subtitle(self, content):
        """
        WARNING:
            The programmer was unable to determine a way in such,
            that a subtitle could not be scraped.
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
            return Par_Scrape.parse(content, (self.right_col + "/div[@class='contributors']/p/span/a/text()"))[0]
        except:
            return None
    
    
    def __get_book_url(self, content):
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
            return Par_Scrape.parse(content, (self.meta_Father_Type + "/following-sibling::meta[@property='og:url']/@content"))[0]
        except:
            return None

    
    def __get_book_site_slug(self):
        """
        args:
            url (String):
                url is used to scrape the book's site_slug
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

        return "SD"

    
    def __get_book_id(self, url):
        """
        args:
            site_slug (String):
                site_slug is used to scrape the book's id
        returns:
            id (String):
                id is the book's id, as determined by the website
        synopsis:
            The purpose of this function is to determine what the
            book's id that is being scraped, using the already
            scraped site_slug
        """

        try:  
            if url != None:
                first = ".com/"
                last = "/"
                start = url.rindex(first) + len(first)
                end = url.rindex(last, start)
                site_slug = url[start:end]
                return site_slug.split("/")[1]
            else:
                return None
        except:
            return None
    
    
    def __get_book_format(self, url):
        """
        args:
            site_slug (String):
                site_slug is used to scrape the format of the book
        returns:
            format (String):
                format is what type of book was scraped
        synopsis:
            The purpose of this function is to determine what kind of
            book is being scraped, using on the the books, already
            scraped, site_slug
        """

        try:
            if url != None:
                first = ".com/"
                last = "/"
                start = url.rindex(first) + len(first)
                end = url.rindex(last, start)
                site_slug = url[start:end]
                if site_slug.split("/")[0] == "audiobook":
                    return "AUDIOBOOK"
                elif site_slug.split("/")[0] == "book":
                    return "DIGITAL"
                else:
                    return None
            else:
                return None
        except:
            return None

    
    def __score_month(self, month):
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

        try:
            if month == "Jan":
                return 1
            elif month == "Feb":
                return 2
            elif month == "Mar":
                return 3
            elif month == "Apr":
                return 4
            elif month == "May":
                return 5
            elif month == "Jun":
                return 6
            elif month == "Jul":
                return 7
            elif month == "Aug":
                return 8
            elif month == "Sep":
                return 9
            elif month == "Oct":
                return 10
            elif month == "Nov":
                return 11
            elif month == "Dec":
                return 12
            else:
                return 0
        except:
            return 0

    
    def __get_book_availability(self, content):
        """
        args:
            content (requests.get()):
                content is needed in order to scrape the book's
                publishing date.
        returns:
            availability (Boolean):
                returns whether or not a book is available
        synopsis:
            The purpose of this function is to determine whether or
            not a book is available.  It determines this by checking
            whether or not the release date is in the future.  If it
            is, then the book is not available.
        """

        try:
            publish_date = Par_Scrape.parse(content, (self.right_col + "/dl[@class='metadata']/dd[@class='meta_description released_date']/text()"))[0]

            converted_date = publish_date.replace(",", "").replace(" ", "-")

            today = date.today().strftime("%b-%d-%Y")
            today_string = str(today)

            #release year is in the future
            #NOT RELEASED
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

    
    def __parse_dynamic_search(self, response):
        """
        args:
            reponse (requests.get):
                response is needed in order to get the content
                that should be parsed for search links.
        returns:
            response_split[1]:
                This is the section of the code that contains
                what will need to be parsed for getting the
                different search links.
        synopsis:
            The purpose of this function is to support the other functions
            that will be parsing the search link page.
        """

        try:
            response_split = response.text.split("ReactDOM.render")
            dynamic_table_location = 1
            return response_split[dynamic_table_location]
        except:
            return None

    
    def __parse_audiobooks(self, response):
        """
        args:
            response (relevant section of (requests.get)):
                This is the section of the code that is needed in order
                to parse the different book links of a search page.
        returns:
            response_filtered (String):
                This is a selection of objects that are only considered to
                be audiobooks.
        synopsis:
            The purpose of this function is to parse the code that it is given
            and only returns a selection of code that is considered to be
            audiobooks.
        """

        try:
            response_filtered = self.__parse_dynamic_search(response)
            if response_filtered == None:
                return None

            first = "\"audiobooks\":{\"content\":{\"documents\":"
            last = "}}}"

            start = response_filtered.rindex(first) + len(first)
            end = response_filtered.index(last, start)

            return response_filtered[start:end]
        except:
            return None

    
    def __parse_books(self, response):
        """
        args:
            response (relevant section of (requests.get)):
                This is the section of the code that is needed in order
                to parse the different book links of a search page.
        returns:
            response_filtered (String):
                This is a selection of objects that are only considered to
                be books.
        synopsis:
            The purpose of this function is to parse the code that is given
            and only returns a selection of code that is considered to be
            books.
        """

        try:
            response_filtered = self.__parse_dynamic_search(response)
            if response_filtered == None:
                return None

            first = "\"books\":{\"content\":{\"documents\":"
            last = "}}}"

            start = response_filtered.rindex(first) + len(first)
            end = response_filtered.index(last, start)

            return response_filtered[start:end]
        except:
            return None

    
    def __generate_dynamic_link_list(self, parsed_book_info):
        """
        args:
            parsed_book_info (relevant selection of (requests.get)):
                This is a selection of code that contains book 'objects'
                that contains urls to the different book objects.
        returns:
            links[]:
                This is a list of the different book objects that is
                located within the code that is passed.
        synopsis:
            The purpose of this function is to parse parsed_book_info
            and return a list of book_urls that are contained within.
                ~This works with both the '__parsed_audiobooks()' and
                the '__parsed_books()' functions.
        """

        try:
            parse_split = parsed_book_info.split("\"book_preview_url\":\"")

            links = []
            for splitup in parse_split:
                if "https://www.scribd.com/" in splitup:
                    seperator = "\"}"
                    splitup = splitup.split(seperator, 1)[0]
                    links.append(splitup)
            return links
        except:
            return None

    
    def __get_book_links_from_search_site(self, url):
        """
        args:
            url (String):
                This is the link to the search page that is going
                to be parsed for relevant book links
        returns:
            search_link_list[]:
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

        url_split = "content_type="
        final_url_split = "&query"
        book_format = url.split(url_split)[1]
        book_format = book_format.split(final_url_split)[0].replace(" ", "")

        response = requests.get(url)

        search_link_list = []

        if book_format == "audiobooks":
            return self.__generate_dynamic_link_list(self.__parse_audiobooks(response))
        elif book_format == "books":
            return self.__generate_dynamic_link_list(self.__parse_books(response))
        elif book_format == "tops":
            search_link_list = self.__generate_dynamic_link_list(self.__parse_audiobooks(response))
            search_link_list += self.__generate_dynamic_link_list(self.__parse_books(response))
            return search_link_list
        else:
            return None
    
    
    def __format_mechanize_url(self, formatting, url):
        """
        args:
            formatting (String):
                This determines how the url will be formatted
            url (String):
                Mechanize generated url that is to be formatted
        returns:
            formatted_url (String):
                Url that was formatted to fit the passed format
        synopsis:
            The purpose of this function is to format a url using the formatting
            that was passed in order to make a proper url.
        """

        url_split = url.split("search?query")
        new_start = url_split[0] + "search?content_type="
        new_end = "&query" + url_split[1]
        new_formatting = ""
        if formatting.lower() == "digital":
            new_formatting = "books"
        elif formatting.lower() == "audiobook":
            new_formatting = "audiobooks"
        else:
            new_formatting = "tops"
        return new_start + new_formatting + new_end

    
    def __Is_Search_Valid(self, search):
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
            The purpose of this function is to check whether or not
            a search link is valid.  If it is, then return the link,
            otherwise return None.
        """

        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        response = br.open("https://www.scribd.com/search?content_type=books&page=1&query=&language=1")
        br.form = list(br.forms())[0]
        control = br.form.controls[0]
        if control.type != "text":
            return None
        control.value = search
        br.submit()
        link = br.geturl()
        response = requests.get(link)

        detection = self.__parse_dynamic_search(response)

        detect_books = "\"books\":{\"content\":{\"documents\":"
        detect_audiobooks = "\"audiobooks\":{\"content\":{\"documents\":"

        if (detect_books not in detection) and (detect_audiobooks not in detection):
            return None
        return link

    
    def __get_search_link_from_book_data_form(self, book_data):
        """
        args:
            book_data (List[]):
                The search that will be determined based upon the data
                that is passed in from book_data
        returns:
            search_links (List[]):
                A list of search links that can be parsed for results
        synopsis:
            The purpose of this function is to return a list of search
            links that can be parsed for individual book links, depending
            upon what is passed in the book_data.
        """

        book_title = book_data[1]
        book_ISBN = book_data[4]
        book_author = book_data[9]

        links = []
        
        if (book_title != None) or (book_ISBN != None) or (book_author != None):
            
            if book_ISBN != None:
                result0 = self.__Is_Search_Valid(book_ISBN)
                if result0 != None:
                    links.append(result0)
            
            if book_title != None:
                result1 = self.__Is_Search_Valid(book_title)
                if result1 != None:
                    links.append(result1)
            
            if book_author != None:
                result2 = self.__Is_Search_Valid(book_author)
                if result2 != None:
                    links.append(result2)
        else:
            return None

        formatted_links = []

        for link in links:
            formatted_links.append(self.__format_mechanize_url(book_data[0], link))

        return formatted_links
