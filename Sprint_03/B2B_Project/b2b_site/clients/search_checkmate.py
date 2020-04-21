import sys

if "../../../Sprint_02" not in sys.path:
    sys.path.append("../../../Sprint_02")

import Scrapers
import json


def search_checkmate(book_data):
    list_data = book_data["bookdata"]

    try:
        format = list_data["format"]
    except:
        #format = None
        format = 'digital'

    try:
        title = list_data["title"]
    except:
        title = None

    try:
        image_url = list_data["image_url"]
    except:
        image_url = None

    try:
        isbn13 = list_data["isbn13"]
    except:
        isbn13 = None

    try:
        description = list_data["description"]
    except:
        description = None

    try:
        series = list_data["series"]
    except:
        series = None

    try:
        volume_number = list_data["volume_number"]
    except:
        volume_number = None

    try:
        subtitle = list_data["subtitle"]
    except:
        subtitle = None

    try:
        authors = list_data["authors"]
    except:
        authors = None

    site_book_data = [
        format, #00-format (String)
        title, #01-book_title (String)
        None, #02-book_image (PIL.Image)
        image_url, #03-book_image_url (String)
        isbn13, #04-isbn_13 (String)
        description, #05-description (String)
        series, #06-series (String)
        volume_number, #07-volume_number (Int)
        subtitle, #08-subtitle (String)
        authors, #09-authors (String)
        None, #10-book_id (String)
        None, #11-site_slug (String)
        None, #12-parse_status (String)
        None, #13-url (String)
        None, #14-content (String)
        None, #15-ready_for_sale (boolean)
        None #16-extra (List[])
        ]

    results = []
    
    # print("Searching Google Books")
    # google_books = Scrapers.get_book_site('gb')
    # gb_list = google_books.find_book_matches_at_site(site_book_data)
    # results.append(['gb', return_list(gb_list)])

    print("Searching Kobo")
    kobo = Scrapers.get_book_site('kb')
    kb_list = kobo.find_book_matches_at_site(site_book_data)
    results.append(['kb', return_list(kb_list)])
    
    print("Searching Livraria Cultura")
    livraria_cultura = Scrapers.get_book_site('lc')
    lc_list = livraria_cultura.find_book_matches_at_site(site_book_data)
    results.append(['lc', return_list(lc_list)])
    
    print("Searching Scribd")
    scribd = Scrapers.get_book_site('sd')
    sd_list = scribd.find_book_matches_at_site(site_book_data)
    results.append(['sd', return_list(sd_list)])

    return results

def return_list(temp_list):
    book_data_list = []

    if temp_list is not None:
        for data in temp_list:
            site_book_data = data[0]
            rating = data[1]
            book_data_list.append([site_book_data[1], site_book_data[9], site_book_data[13], site_book_data[3], rating])

    return book_data_list


if __name__ == "__main__":

    book_data = {
    "format": "digital", #00-format (String)
    "title": "anne frank", #01-book_title (String)
    "book_image": None, #02-book_image (PIL.Image)
    "image_url": "https://kbimages1-a.akamaihd.net/defcbc15-71d7-4bb5-9fcb-4835cfd17b38/353/569/90/False/anne-frank-s-tales-from-the-secret-annex-1.jpg", #03-book_image_url (String)
    "isbn13": None, #04-isbn_13 (String)
    "description": None, #05-description (String)
    "series": None, #06-series (String)
    "voulume_number": None, #07-volume_number (Int)
    "subtile": None, #08-subtitle (String)
    "authors": "anne frank", #09-authors (String)
    "book_id": None, #10-book_id (String)
    "site_slug": "gb", #11-site_slug (String)
    "parse_status": None, #12-parse_status (String)
    "url": None, #13-url (String)
    "content": None, #14-content (String)
    "ready_for_sale": None, #15-ready_for_sale (boolean)
    "extra": None} #16-extra (List[])

    search_checkmate(book_data)