import Parsers.Main_Scribd as scribd_book_site

def get_book_site(slug):
    if slug.lower() == "sd":
        return scribd_book_site.book_site_scribd()
    else:
        return None

