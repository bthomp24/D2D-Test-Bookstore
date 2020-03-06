import Scrapers
import Parsers.Parent_Scrape as Par_Scrape
#from PIL import Image
import time

start_time = time.time()

''' Make the Book Data '''

"""
SiteBookData (List):
    00) format (String): 
    01) book_title (String):
    02) book_image: (PIL.Image)
    03) book_image_url (String):
    04) isbn_13 (String):
    05) description (String):
    06) series (String):~
    07) volume_number (Int):~
    08) subtitle (String):~
    09) authors (String):
    10) book_id: (String)
    11) site_slug (String):
    12) parse_status (String):~
    13) url (String):
    14) content (String):
    15) ready_for_sale (boolean):~
    16) extra:~
"""

#book_data_Template
'''
book_data = [None, #00-format (String)
    None, #01-book_title (String)
    None, #02-book_image (PIL.Image)
    None, #03-book_image_url (String)
    None, #04-isbn_13 (String)
    None, #05-description (String)
    None, #06-series (String)
    None, #07-volume_number (Int)
    None, #08-subtitle (String)
    None, #09-authors (String)
    None, #10-book_id (String)
    None, #11-site_slug (String)
    None, #12-parse_status (String)
    None, #13-url (String)
    None, #14-content (String)
    None, #15-ready_for_sale (boolean)
    None] #16-extra (List[])
'''

book_image_url = "https://imgv2-2-f.scribdassets.com/img/word_document/356970421/original/e058724125/1582611379?v=1"
tempImage = Par_Scrape.get_book_image_from_image_url(book_image_url)
book_data = ["digital", #00-format (String)
    "The name of the wind", #01-book_title (String)
    None, #02-book_image (PIL.Image)
    None, #03-book_image_url (String)
    "9781423389309", #04-isbn_13 (String)
    "My name is Kvothe. I have stolen princesses back from sleeping barrow kings. I burned down the town of Trebon. I have spent the night with Felurian and left with both my sanity and my life. I was expelled from the University at a younger age than most people are allowed in. I tread paths by moonlight that others fear to speak of during day. I have talked to Gods, loved women, and written songs that make the minstrels weep. You may have heard of me. So begins a tale unequaled in fantasy literature-the story of a hero told in his own voice. It is a tale of sorrow, a tale of survival, a tale of one man's search for meaning in his universe, and how that search, and the indomitable will that drove it, gave birth to a legend. \"It is a rare and great pleasure to find a fantasist writing…with true music in the words…. Wherever Pat Rothfuss goes…he'll carry us with him as a good singer carries us through a song.\" -Ursula K. Le Guin, bestselling author and winner of the National Book Award", #05-description (String)
    None, #06-series (String)
    None, #07-volume_number (Int)
    None, #08-subtitle (String)
    "Patrick Rothfuss", #09-authors (String)
    None, #10-book_id (String)
    "SD", #11-site_slug (String)
    None, #12-parse_status (String)
    None, #13-url (String)
    None, #14-content (String)
    None, #15-ready_for_sale (boolean)
    None] #16-extra (List[])


''' Call the parsers from the Scrapes file '''
scribd = Scrapers.get_book_site(book_data[11])

Par_Scrape.write_Txt(str(Scrapers.get_book_site(book_data[11]).find_book_matches_at_site(book_data)), "Test_Files/testingFile")


end_time = time.time()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("                                  FINISHED")
print("                                  TIME: ", (end_time - start_time))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
