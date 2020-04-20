import io
from lxml import etree
import requests
import Parsers.Parent_Scrape as Par_Scrape
import mechanize
import concurrent.futures
import time

class book_site_google():
    def __init__(self, *args, **kwargs):
        self.content_table = "//*[@id='metadata_content_table']/"


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
            The purpose of this function is to parse a url of the Google   
            Books website.  The url should be a specific book's url, in 
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
        book_title = self._get_book_title(response.content)

        # book_image_url
        book_image_url = self._get_book_image_url(response.content)

        # book_image
        book_image = Par_Scrape.get_book_image_from_image_url(book_image_url)

        # isbn_13
        isbn_13 = self._get_book_isbn_13(response.content)

        # description
        description = self._get_book_description(response.content)

        # series
        series = self._get_book_series(response.content)

        # volume_number
        volume_number = self._get_book_volume(response.content)
        
        # book_subtitle
        subtitle = self._get_book_subtitle(response.content)

        # book_authors
        authors = self._get_book_authors(response.content)

        # url
        book_url = self._get_book_url(response.content)

        # site_slug
        site_slug = self._get_book_site_slug()

        # book_id
        book_id = self._get_book_id(response.url)

        # format
        format = self._get_book_format(response.content)

        # content
        content = response.content

        # ready_for_sale
        ready_for_sale = self._get_book_sale_status(response.content)

        # parse_status
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

        if book_data[0].upper() == "AUDIOBOOK":
            return None


        # Perform whatever form making for the website in order to get a relevant search link
        #url_gotten_from_form = "https://books.google.com/"
        url_gotten_from_form = self._get_search_link_from_book_data_form(book_data)
        
        # check to ensure search page exists
        if not url_gotten_from_form:
            return None

        site_book_data_total = []

        for url in url_gotten_from_form:

            relevant_book_links = self._get_book_links_from_search_site(url, 0)
            if relevant_book_links != None:
                site_book_data_list = []
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    Future_Threads = []

                    for book_link in relevant_book_links:
                        Future_Threads.append(executor.submit(self.get_book_data_from_site, book_link))
            
                    for future in concurrent.futures.as_completed(Future_Threads):
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

        primary_url = "https://books.google.com/"
        tail_url = "&source=gbs_navlinks_s"
        return primary_url + book_id + tail_url

    
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
            The purpose of this function is to determine what the book's
            title is.
        """

        try:
            title_data = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label'][contains(text(), 'Title')]" + "/following-sibling::td/span/text()"))
            
            # Process here is to compensate for google books combining the series, volume, and title.
            # removes at the ':' which is the seperator. 
            title = [x.strip() for x in title_data[0].split(':')]
            return title[0]
        except:
            return None

    
    def _get_book_image_url(self, content):
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
            return Par_Scrape.parse(content, "//*[@title='Front Cover']/@src")[0]
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
            data = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label']/span[contains(text(), 'ISBN')]" + "/../following-sibling::td/span/text()"))
            
            # Process here is to compensate for google books displaying both isbn_10
            # and isbn_13. Seperates the two and only returns the isbn_13 by length compare 
            isbn_13 = [x.strip() for x in data[0].split(',')]
            for x in isbn_13:
                if len(x) == 13:
                    return x
            return None
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
            desc_parts = Par_Scrape.parse(content, ("//*[@id='synopsistext']//text()"))

            # Process here is to compensate for returning empty variables
            # as well as acquiring all the text in between HTML tags.
            # Solution to the dynamic html formatting of google books descriptions.
            if len(desc_parts) == 0:
                return None

            full_desc = ""            
            for parts in desc_parts:
                full_desc += parts
                
            return full_desc
        except:
            return None


    def _get_book_series(self, content):
        """
        WARNING:
            The programmer was unable to determine a way in such,
            that a series and volume could be seperated consistently.
        args:
            content (requests.get):
                content is needed in orde to scrape the book's
                series
        returns:
            series (String):
                the series (and entry) the book that is
                being scraped.
        synopsis:
            The purpose of this function is to determine what
            the book's series
        """

        try:
            data = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label'][contains(text(), 'Title')]" + "/following-sibling::td/span/text()"))
            
            # Process here is to compensate for google books combining the series, volume, and title.
            # removes at the ':' which is the seperator. 
            series = [x.strip() for x in data[0].split(':')]
            if len(series) > 1:
                arching_series = ''
                count = 1
                for x in series:
                    if count > 1:
                        arching_series += x + " "
                    count += 1
                
                return arching_series
            else:
                return None
        except:
            return None

    
    def _get_book_volume(self, content):
        """
        WARNING:
            The programmer was unable to determine a way in such,
            that a series and volume could be seperated consistently.
        """

        return None

    
    def _get_book_subtitle(self, content):
        """
        args:
            content (requests.get):
                content is needed in order to scrape the book's
                subtitle
        returns:
            subtitle (String):
                the subtitle of the book that is being scraped.
        synopsis:
            The purpose of this function is to determine what
            the book's subtitle is.
        """

        try:
            subtitle = Par_Scrape.parse(content, ("//*[@class='subtitle']/text()"))
           
            # Process here is to compensate for google books placement of the text().
            # if the text is in a deeper <div> tag it will be able to access it. 
            if len(subtitle) == 0:
                subtitle = Par_Scrape.parse(content, ("//*[@class='subtitle']/span[@dir='ltr']/text()"))

            if len(subtitle) == 0:
                return None

            true_subtitle = ""

            for part in subtitle:
                true_subtitle += part

            return true_subtitle
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
            authors = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label']/span[contains(text(), 'Author')]" + "/../following-sibling::td/a/span/text()"))
            all_authors = ""

            if len(authors) == 0:
                return None

            # Process here is to compensate for multiple authors.
            for author in authors:
                all_authors += author + " "

            return all_authors
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
            return Par_Scrape.parse(content, "//*[@class='bookcover']/a/@href")
        except:
            return None

    
    def _get_book_site_slug(self):
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

        return "GB"

    
    def _get_book_id(self, url):
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
        
        if url != None:
            first = ".com/"
            last = "&"
            start = url.rindex(first) + len(first)
            end = url.index(last, start)
            site_slug = url[start:end]
            return site_slug
        else:
            return None

    
    def _get_book_format(self, content):
        """
        args:
        returns:
            format (String):
                format is what type of book was scraped
                google books only has E-books available on their
                own site.
        synopsis:
            The purpose of this function is to return the book format
            "DIGITAL" since google books only has E-books on their 
            own site.
        """
        try:
            if Par_Scrape.parse(content, "//*[@id='gb-get-book-not-available']"):
                return "PRINT"
            else:    
                return "DIGITAL"
        except:
            return None
    
    def _get_book_sale_status(self, content):
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
            if Par_Scrape.parse(content, "//*[@id='gb-get-book-not-available']"):
                return False
            else:
                return True
        except:
            return None

    def _get_book_sale_price(self, content):
        """
        args:
            content (Request.get):
                content is needed in order to scrape the e-book's
                price if applicable
        returns:
            price:
                This is this price of the ebook.
            (None):
                If there is no ebook for the book searched.
        synopsis:
            The purpose of this function is to parse the to scrape
            for the ebook's price and return it.
        """
        try:
            if Par_Scrape.parse(content, "//*[@id='gb-get-book-not-available']"):
                return None
        except:
            return None

    
    def __get_book_links_from_search_site(self, url, page_number):
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
            
            collected_urls = Par_Scrape.parse(response.content, ("//*[@class='ZINbbc xpd O9g5cc uUPGi']/div[@class='kCrYT'][1]/a/@href"))
            relevant_urls = []

            # if no search results are found.
            if len(collected_urls) == 0:
                return None

            # Process for formatting the urls collected into direct links.
            # This process is due to google books links acquired taking the
            # browser to a "Preview" book page which doesn't have the data we
            # are after.
            for proper_link in collected_urls:
                url_split = "&"
                
                proper_link = proper_link.split(url_split, 1)[0]
                proper_link += "&source=gbs_navlinks_s"
                
                
                if "https://books.google.com/books?id=" in proper_link:
                    relevant_urls.append(proper_link)
                else:
                    relevant_urls.append(None)
            
            # statement for going to get links on next page.
            # recursive calling function that stops after
            # 5 page search results full. (60 results)
            if page_number < 5:

                # process to construct the url for the page linked by the next button on google books.
                next_page_tail = Par_Scrape.parse(requests.get(url).content, "//*[@class='nBDE1b G5eFlf'][@aria-label='Next page']/@href")

                # if there is no next page.
                if len(next_page_tail) == 0:
                    return relevant_urls
                
                next_page = "https://www.google.com" + next_page_tail[0]

                page_number += 1
                next_group = self.__get_book_links_from_search_site(next_page, page_number)

                # if there is a next page but it contains no results
                if next_group == None:
                    return relevant_urls
                
                for url in next_group:
                    relevant_urls.append(url)    

            return relevant_urls    
        except:
            return None

    def _Is_search_valid(self, search):
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
        time.sleep(.3)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        response = br.open("https://books.google.com/")
        br.form = list(br.forms())[0]
        control = br.form.controls[1]
        if control.type != "text":
            return None
        control.value = search
        br.submit()
        link = br.geturl()

        #Newly Added
        test_validity = requests.get(link)
        returned =  Par_Scrape.parse(test_validity.content, "//span[@class='JZCD0c r0bn4c rQMQod']")
        if len(returned) != 0:
            return None

        return link

    
    def _get_search_link_from_book_data_form(self, book_data):
        """
        args:
            book_data (List[]):
                The search that will be determined based upon the data
                that is passed in from book_data.
        returns:
            result_url:
                A search link that can be parsed for results
        synopsis:
            The purpose of this function is to return the search
            link that can be parsed for individual book links, 
            depending on what is passed in the book_data.
        """
        
        book_title = book_data[1]
        book_ISBN = book_data[4]
        book_author = book_data[9]

        # our string for the form
        book_search = ""
        links = []

        if (book_title != None) or (book_ISBN != None) or (book_author != None):
            
            if book_ISBN != None:
                result0 = self._Is_search_valid(book_ISBN)
                if result0 != None:
                    links.append(result0)
            
            if book_title != None:
                result1 = self._Is_search_valid(book_title)
                if result1 != None:
                    links.append(result1)
            
            if book_author != None:
                result2 = self._Is_search_valid(book_author)
                if result2 != None:
                    links.append(result2)
        else:
            return None

        return links