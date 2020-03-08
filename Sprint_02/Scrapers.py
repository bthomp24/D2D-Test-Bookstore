import Parsers.Main_Google_Books as google_books_book_site
import Parsers.Main_Kobo as kobo_site
import Parsers.Main_Scribd as scribd_book_site
import Parsers.Main_Test_Bookstore as test_bookstore_book_site

def get_book_site(slug):
    #Google Books Parser
    if slug.lower() == "gb":
        return google_books_book_site.book_site_google()

    #Kobo Parser
    elif slug.lower() == "kb":
        return kobo_site.book_site_kobo()

    elif slug.lower() == "lc":
        pass

    #Scribd Parser
    elif slug.lower() == "sd":
        return scribd_book_site.book_site_scribd()

    #Test Bookstore Parser
    elif slug.lower() == "tb":
        return test_bookstore_book_site.book_site_test_bookstore()

    #Available slug not passed
    else:
        print("Unknown slug:" + str(slug))
        return None

