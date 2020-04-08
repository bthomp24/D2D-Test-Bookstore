import io
from lxml import etree

import time

import six

import concurrent.futures

from PIL import Image, ImageChops
import urllib.request,io

from fuzzywuzzy import fuzz

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                     the following is a selection of generic functions                     
                                that are useful for parsing                                
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

def write_Response(response, target):
    """
    args:
        response (requests.get()):
            What you wish to input into an .html file
        target (String):
            What you wish to name the .html file
    returns:
        NOT APPLICABLE
    synopsis:
        This function will take any imput that you place in the first
        parameter, then it will write it to an .html file, which you
        will name using the second parameter.
    """

    target = target + ".html"
    text_file = open(target, "w", encoding="utf-8")
    text_file.write(response.text)
    text_file.close()


def write_Txt(text, target):
    """
    args:
        text (String):
            What you wish to input into a .txt file
        target (String):
            What you wish to name the .txt file
    returns:
        NOT APPLICABLE
    synopsis:
        This function will take any imput that you place in the first
        parameter, then it will write it to an .txt file, which you
        will name using the second parameter.
    """

    target = target + ".txt"
    text_file = open(target, "w", encoding="utf-8")
    text_file.write(text)
    text_file.close()


def parse(content, path):
    """
    args:
        content (requests.get()):
            What you wish to be searched using xpath
        path (String(xpath format)):
            what the xpath will use to search the content
    returns:
        result (filtered requests.get() according to 'path'):
            what is returned by the xpath searching the content
    synopsis:
        This function will search a the first parameter using the
        second parameter as an xpath.
    """

    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root.xpath(path)


def get_book_image_from_image_url(image_url):
    """
    args:
        image_url (String):
            needs to be a url of an image
    returns:
        image (Image):
            open image that was returned from the site,
            it was then converted to grayscale
    synopsis:
        The purpose of this function is to parse an image from a specific
        url, convert it to grayscale, and then return it.
    """

    if image_url != None:
        try:
            return Image.open(io.BytesIO(urllib.request.urlopen(image_url).read())).convert("L")
        except:
            return None
    else:
        None


def parse_status(parse_list):
    """
    args:
        parse_list[]:
            list of objects to test
    returns:
        Result (String):
            "FULLY_PARSED":
                if not a single object is None
            "UNSUCCESSFUL"
                :if there is even one object that is None
    synopsis:
        The purpose of this function is to return a consistent and
        predetermined response based upon the outcome of whether or
        not the 'parse_list', at all, contains a ''None''.
            UNSUCCESSFUL:
                Will be returned upon the list containing any
                ''None'' attribute at all.
            FULLY_PARSED:
                Will be returned upon the list containing no
                ''None'' attributes.
    """

    for parse_content in parse_list:
        if parse_content == None:
            return "UNSUCCESSFUL"
    return "FULLY_PARSED"


def site_book_data_relevancy(original_book_data, site_book_data_list):
    """
    args:
        original_book_data[]:
            list of data that will be tested against the data that is contained
            withing the site_book_data_list
        site_book_daata_list[]:
            list of site_book_data's, this will be checked against by the
            'original_book_data'.
    returns:
        book_data_relevancy_list[]:
            This is a list of site_book_data, and their correcsponding
            relevancy rates.
    synopsis:
        The purpose of this function is to return a list of
        'site_book_data', as well as its corresponding relevancy
        rating, determined by the 'original_book_data'
    """

    start = time.time()

    book_data_relevancy_list = []

    if len(original_book_data) != 17:
        print("Parent_Scrape ~ site_book_data_relevancy ~ site_book_data: CRITICAL ERROR => len(original_book_data): ", len(original_book_data))
        return None
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            Future_Threads = {}
            for site_book_data in site_book_data_list:
                if len(site_book_data) != 17:
                    print("Parent_Scrape ~ site_book_data_relevancy ~ site_book_data: CRITICAL ERROR => len(site_book_data): ", len(site_book_data))
                    book_data_relevancy_list.append([None, 0])
                else:
                    Future_Threads[executor.submit(__compare_book_data_lists, original_book_data, site_book_data)] = site_book_data

            for future in concurrent.futures.as_completed(Future_Threads):
                site_book_data_temp = Future_Threads[future]
                book_data_relevancy_list.append([site_book_data_temp, future.result()])

            book_data_relevancy_list.sort(key=__sort_by_relevancy_rating, reverse=True)
        
    end = time.time()
    print("Sorting TIME: ", (end - start))
    return book_data_relevancy_list


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       following private functions are necessary for the site_book_relevancy function       
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


def __compare_string(book_data_string, site_book_data_string, cleanup):
    """
    args:
        book_data_string (String):
            String that will be tested to determine to what degree
            it matched 'site_book_data_string'.
        site_book_data_string (String):
            String that is being tested against for the purposes
            of determining the liklyness that 'book_data_string'
            matches itself.
    returns:
        result (Number):
            The relevancy rating that the 'book_data_string' is
            related to the 'site_book_data_string'.
    synopsis:
        The purpose of this function is to take two strings and
        compare them.  It will then be scored, based upon the
        liklyness that 'book_data_string' matches
        'site_book_data_string'.
    """
    if cleanup == True:
        book_data_string = book_data_string.replace("\t", " ").replace("\"", "").replace("\'", "").replace(".", "").replace(",","").replace("?", "")
        site_book_data_string = site_book_data_string.replace("\n", "").replace("\t", " ").replace("\"", "").replace("\'", "").replace(".", "").replace(",","").replace("?", "")

    return fuzz.ratio(book_data_string.lower(), site_book_data_string.lower())


def __compare_images(image1, image2):
    """
    args:
        image1 (Image):
            Original image to be compared against
        image2 (Image):
            image that is a potential match
    returns:
        result (Number):
            score based upon number of matching pixels
    synopsis:
        The purpose of this function is to take two Images, compare them,
        then return a percentage, that is the 'result' of the comparison
        between the two.
    """
    try:
        image1 = image1.convert("L")
        diff = ImageChops.difference(image1, image2)

        diff_bbox = diff.getbbox()
        if not diff_bbox:
            return 1
        
        image1_bbox = image1.getbbox()
        if not image1_bbox:
            return 0
        image2_bbox = image2.getbbox()
        if not image2_bbox:
            return 0
        
        image1_pixels = sum((image1.crop(image1_bbox).point(lambda x: 255 if x else 0).convert("L").point(bool).getdata()))
        image2_pixels = sum((image2.crop(image2_bbox).point(lambda x: 255 if x else 0).convert("L").point(bool).getdata()))
        diff_pixels = sum((diff.crop(diff_bbox).point(lambda x: 255 if x else 0).convert("L").point(bool).getdata()))
        image_pixels_mean = ((image1_pixels + image2_pixels) / 2)
        numerator = 0
        if image1_pixels > image2_pixels:
            numerator = image1_pixels
        else:
            numerator = image2_pixels
            
        result = 1 - (diff_pixels / numerator)
        return result 
    except:
        print("comapre_images => FAILED")
        return 0


def __compare_book_data_lists(original_book_data, site_book_data):
    """
    args:
        original_book_data[]:
            list of objects that will be tested against the
            'site_book_data' list
        site_book_data[]:
            list of objects that is being tested against
    returns:
        score (Number):
            this number is represents the liklyness that
            'original_book_data' matches 'site_book_data'
    synopsis:
        The purpose of this function is to return a relevancy
        rating of two list objects matching each other.
    """

    object_number = len(site_book_data)
    total_score = 0
    objects_scored = 0
    for x in range(object_number):
        """
        Don't compare:
            x == 3:
                Image Url
        """
        if x != 3:
            #Only test objects where neither of them are None
            if (original_book_data[x] != None) and (site_book_data[x] != None):
                #Specifically tests if both objects are Strings
                if (isinstance(original_book_data[x], six.string_types)) and (isinstance(site_book_data[x], six.string_types)):
                    cleanup = False
                    """
                    x == 4:
                        isbn-13
                    x == 5:
                        description
                    """
                    if (x == 4) or (x == 5):
                        cleanup = True
                    total_score += __compare_string(original_book_data[x].lower(), site_book_data[x].lower(), cleanup)
                    objects_scored += 1
                #Image Comparison
                elif x == 2:
                    total_score += __compare_images(original_book_data[x], site_book_data[x])
                    objects_scored += 1
    if objects_scored != 0:
        score = total_score / objects_scored
    else:
        score = 0
    return round(score, 2)

def __sort_by_relevancy_rating(element):
    """
    args:
        element[]:
            list that will be used for the purposes of ordering same list
    returns:
        result (Number):
            number that will be used for orddering a list, with the relevancy
            rating being in the second option.
    synopsis:
        The purpose of this function be used specifically for sorting another
        list using only the second objects of the array.
    """
    return element[1]


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                               list of public functions below                               
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
                              write_Response(response, target)                   
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
                                   write_Txt(text, target)                       
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
                                    parse(content, path)                         
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
                                  parse_status(parse_list)                       
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
             site_book_data_relevancy(origninal_book_data, site_book_data_list)  
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
"""
'''
returns:
        SiteBookData (List):
            format (String): 
            book_title (String):
            book_image:~
            book_image_url:~
            isbn_13 (String):
            description (String):
            series (String):*
            volume_number (Int):*
            subtitle:~
            authors (String):
            book_id (String):
            site_slug (String):
            parse_status (String):
            url (String):
            content (String):
            ready_for_sale (boolean):
            extra:~
'''