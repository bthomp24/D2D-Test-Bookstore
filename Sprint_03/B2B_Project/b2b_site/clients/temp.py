import sys

if "../Sprint_02" not in sys.path:
    sys.path.append("../Sprint_02")

import Scrapers

book_site = Scrapers.get_book_site('gb')

book_data = ["digital", #00-format (String)
    "anne frank", #01-book_title (String)
    None, #02-book_image (PIL.Image)
    "https://kbimages1-a.akamaihd.net/defcbc15-71d7-4bb5-9fcb-4835cfd17b38/353/569/90/False/anne-frank-s-tales-from-the-secret-annex-1.jpg", #03-book_image_url (String)
    None, #04-isbn_13 (String)
    None, #05-description (String)
    None, #06-series (String)
    None, #07-volume_number (Int)
    None, #08-subtitle (String)
    "anne frank", #09-authors (String)
    None, #10-book_id (String)
    "gb", #11-site_slug (String)
    None, #12-parse_status (String)
    None, #13-url (String)
    None, #14-content (String)
    None, #15-ready_for_sale (boolean)
    None] #16-extra (List[])

book_site.find_book_matches_at_site(book_data)