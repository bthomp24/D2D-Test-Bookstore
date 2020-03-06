import io
from lxml import etree
import requests
import Parent_Scrape as Par_Scrape

# important class names to remember.
# Yr5TG Xpath during the search results page.

# <table id="metadata_content_table">

# You can get the book id and put it in the url to basically construct the appropriate page for searching.

# this is to get to the table. Xpath to this. /html/body/div[7]/div[2]/div/div[7]/div/div[1]/table/tbody


# for the price of e-book //*[@id="gb-get-book-content"]

URL = "https://books.google.com/books?id=NuMx6tmf5iIC&source=gbs_navlinks_s"


class book_site_google():
    def __init__(self, *args, **kwargs):
        # super().__init__()
        self.content_table = "//*[@id='metadata_content_table']/"



    def get_book_format(self, content):
        return "DIGITAL"

    def get_book_title(self, content):
        try:
            data = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label'][contains(text(), 'Title')]" + "/following-sibling::td/span/text()"))
            title = [x.strip() for x in data[0].split(',')]
            return title[0]
        except:
            return None

    def get_book_image_url(self, content):
        try:
            return Par_Scrape.parse(content, "//*[@title='Front Cover']/@src")
        except:
            return None

    def get_book_image(self):
        pass
    # adjust for Pillow when learning how to do it.


    def get_book_isbn_13(self, content):
        
        try:
            data = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label']/span[contains(text(), 'ISBN')]" + "/../following-sibling::td/span/text()"))
            isbn_13 = [x.strip() for x in data[0].split(',')]
            for x in isbn_13:
                if len(x) == 13:
                    return x

            return None
        except:
            return None


    def get_book_description(self, content):
        try:
            return Par_Scrape.parse(content, ("//*[@id='synopsistext']/text()"))
        except:
            return None


    """
    WARNING:
        The volume and series are both in the same string. The
        manner of order is also inconsistent so the programmer
        is unable to accurately distinguish the two in Google
        Book's site data.
    """
    def get_book_series(self, content):
        return None

    """
    WARNING:
        The volume and series are both in the same string. The
        manner of order is also inconsistent so the programmer
        is unable to accurately distinguish the two in Google
        Book's site data.
    """
    def get_book_volume(self, content):
        """try:
            data = Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label'][contains(text(), 'Title')]" + "/following-sibling::td/span/text()"))
            volume = [x.strip() for x in data[0].split(':')]
            if len(volume) > 1:
                arching_volume = ''
                count = 1
                for x in volume:
                    if count > 1:
                        arching_volume += x + " "
                    count += 1
                
                return arching_volume
            else:
                return None
        except:"""
        return None

    def get_book_subtitle(self, content):
        try:
            subtitle = Par_Scrape.parse(content, ("//*[@class='subtitle']/text()"))

            for x in subtitle:
                if False == isinstance(x, str):
                    subtitle = Par_Scrape.parse(content, ("//*[@class='subtitle']/span/text()"))

            return subtitle
        except:
            return None

    def get_book_authors(self, content):
        try:
            return Par_Scrape.parse(content, (self.content_table + "/tr[@class='metadata_row']/td[@class='metadata_label']/span[contains(text(), 'Author')]" + "/../following-sibling::td/a/span/text()"))
        except:
            return None


    def get_book_id(self, url):
        
        if url != None:
            first = ".com/"
            last = "&"
            start = url.rindex(first) + len(first)
            end = url.index(last, start)
            site_slug = url[start:end]
            return site_slug
        else:
            return None

    def get_book_site_slug(self):
        return "GB"


    def get_book_url(self, content):
        try:
            return Par_Scrape.parse(content, "//*[@class='bookcover']/a/@href")
        except:
            return None
        
    def get_book_sale_status(self, content):
        if Par_Scrape.parse(content, "//*[@id='gb-get-book-not-available']"):
            return False
        else:
            return True
            
    

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

        # book_title
        book_title = self.get_book_title(response.content)

        # book_image

        # book_image_url
        book_image_url = self.get_book_image_url(response.content)

        # isbn_13
        isbn_13 = self.get_book_isbn_13(response.content)

        # description
        description = self.get_book_description(response.content)

        # series
        series = self.get_book_series(response.content)

        # volume_number
        volume_number = self.get_book_volume(response.content)
        
        # book_subtitle
        subtitle = self.get_book_subtitle(response.content)

        # book_authors
        book_authors = self.get_book_authors(response.content)

        # url
        book_url = self.get_book_url(response.content)

        # site_slug
        ready_for_sale = self.get_book_sale_status(response.content)

        # book_id
        book_id = self.get_book_id(response.url)

        # format
        format = self.get_book_format(response.content)

        # content
        content = response.content

        # ready_for_sale
        ready_for_sale = self.get_book_sale_status(response.content)

        # parse_status
        parse_status = Par_Scrape.parse_status([format, book_title, book_image, book_image_url, isbn_13, description, authors, book_id, site_slug, url, content, ready_for_sale])
        
        SiteBookData = [format, book_title, book_image, book_image_url, isbn_13, description, series, volume_number, subtitle, authors, book_id, site_slug, parse_status, url, content, ready_for_sale, extra]
        
        return SiteBookData


    def get_book_links_from_search_site(self, url):
           pass
        # &source=gbs_navlinks_s


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
    def convert_book_id_to_url(self, book_id):
        primary_url = "https://books.google.com/"
        tail_url = "&source=gbs_navlinks_s"
        return primary_url + book_id + tail_url

This = book_site_google()

This.get_book_data_from_site(URL)
