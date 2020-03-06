import Scrapers
import Parsers.Parent_Scrape as Par_Scrape
from PIL import Image
import time

start_time = time.time()

''' Make the Book Data '''

#book_data_Template
#book_data = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

book_image_url = "https://imgv2-2-f.scribdassets.com/img/word_document/356970421/original/e058724125/1582611379?v=1"
tempImage = Par_Scrape.get_book_image_from_image_url(book_image_url)
book_data = ["digital", "The name of the wind", None, None, "9781423389309", "My name is Kvothe. I have stolen princesses back from sleeping barrow kings. I burned down the town of Trebon. I have spent the night with Felurian and left with both my sanity and my life. I was expelled from the University at a younger age than most people are allowed in. I tread paths by moonlight that others fear to speak of during day. I have talked to Gods, loved women, and written songs that make the minstrels weep. You may have heard of me. So begins a tale unequaled in fantasy literature-the story of a hero told in his own voice. It is a tale of sorrow, a tale of survival, a tale of one man's search for meaning in his universe, and how that search, and the indomitable will that drove it, gave birth to a legend. \"It is a rare and great pleasure to find a fantasist writing…with true music in the words…. Wherever Pat Rothfuss goes…he'll carry us with him as a good singer carries us through a song.\" -Ursula K. Le Guin, bestselling author and winner of the National Book Award", None, None, None, "Patrick Rothfuss", None, None, None, None, None, None, None]


"""
SiteBookData (List):
    00) format (String): 
    01) book_title (String):
    02) book_image:~
    03) book_image_url (String):
    04) isbn_13 (String):
    05) description (String):
    06) series (String):~
    07) volume_number (Int):~
    08) subtitle (String):~
    09) authors (String):
    10) book_id:
    11) site_slug (String):
    12) parse_status (String):~
    13) url (String):
    14) content (String):
    15) ready_for_sale (boolean):~
    16) extra:~
"""

''' Call the parsers from the Scrapes file '''
scribd = Scrapers.get_book_site("SD")

''' Test the files '''
Par_Scrape.write_Txt(str(scribd.find_book_matches_at_site(book_data)), "Test_Files/testingFile")


end_time = time.time()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("                                  FINISHED")
print("                                  TIME: ", (end_time - start_time))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
