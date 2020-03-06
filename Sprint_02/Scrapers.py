import Parsers.Main_Scribd as scribd_book_site
import Parsers.Main_Google_Books as google_book_site

def get_book_site(slug):
    if slug.lower() == "sd":
        return scribd_book_site.book_site_scribd()
    else if slug.lower() == "GB":
        return google_book_site.book_site_google()
    else:
        return None

