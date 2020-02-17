import os, sys
sys.path.append('/D2D_project/D2D_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'D2D_project.settings'
import django
django.setup()
from test_bookstore.models import Book

"""
args:
    Not Applicable
returns:
    Book Objects: Book Objects that are in the database
synopsis:
    The purpose of this function is to return every BOOK object in the database
"""
def __Get_All_Book_Objects():
    return Book.objects.all()

"""
args:
    New (String): Search String to be tested
    Old (String): Original String testing against
returns:
    Num: Likelyness rating for two specific words
synopsis:
    The purpose of this function is to return a likelyness rating for the
    comparison of two words against each other.
"""
def __Difference_Calculation(New, Old):
    return ((len(New) / len(Old)) * 100)

"""
args:
    Book_Object (Book Object): Book Object that will be tested
returns:
    Num: total number of words that will be tested
synopsis:
    The purpose of this function is to return the total number
    of words that will be tested for a specific book object
"""
def __Total_Checks(Book_Object):
    Total = 0

    Title_Split = Book_Object.title.split()
    Total += len(Title_Split)

    Author = __Return_Author_Total(Book_Object)
    Author_Split = Author.split()
    Total += len(Author_Split)

    ISBN_Split = Book_Object.ISBN.split()
    #Total += len(ISBN_Split)
    Total += 1

    return Total

"""
args:
    Possible_ISBN (String): String that will be tested to see if
    it is an ISBN
    Book_Object (Book Object): Book Object which will have the ISBN
    that we are checking
returns:
    Num: Returns either a 100 or 0 depending upon whether or not the
    ISBN matches the possible ISBN
synopsis:
    The purpose of this function is to determine whether or not
    the possible_ISBN completely matches the ISBN of the book
    we are checking
"""
def ____Compare_Book_ISBN(Possible_ISBN, Book_Object):
    try:
        Possible_ISBN = Possible_ISBN.replace("-", "")
        if len(Possible_ISBN) == 10:
            Possible_ISBN = "978" + Possible_ISBN
        elif len(Possible_ISBN) == 13:
            pass
        else:
            return 0

        if Possible_ISBN == Book_Object.ISBN:
            return 100
        else:
            return 0
    except:
        return 0

"""
args:
    Book_Object (Book_Object): Book_Object that will be checked for authors
returns:
    String: String will contain the authors that we will be checking
synopsis:
    The purpose of this function is to return a single string that can
    be used later to check if a word matches within it.
"""
def __Return_Author_Total(Book_Object):
    Author_String = Book_Object.primary_author
    if Book_Object.secondary_authors != "None":
        Author_String += " " + Book_Object.secondary_authors
    return Author_String

"""
args:
    Possible_Author (String): String that will be checked to determine
    if it matches any of the author names within the book object
    Book_Object (Book Object): Book Object that will be checked
returns:
    Num: Likelyness rating of the Possible_Author matching an author
    name withing the Book Object
synopsis:
    The purpose of this function is to check whether or not a Possible_Author
    matches any of the words that are in any of the authors names
"""
def ____Compare_Book_Authors(Possible_Author, Book_Object):
    Author = __Return_Author_Total(Book_Object)
    Author_Split = Author.split()
    for Author_Part in Author_Split:
        if Possible_Author == Author_Part.lower():
            return 100

    Score = 0.0

    for Author_Part in Author_Split:
        if Possible_Author in Author_Part.lower():
            if Score < __Difference_Calculation(Possible_Author, Author_Part.lower()):
                Score = __Difference_Calculation(Possible_Author, Author_Part.lower())

    return Score

"""
args:
    Possible_Title (String): String that will be checked to determine
    if it matches any of the words within the book objects title
    Book_Object (Book Object): Book Object that will have its title
    checked for likelynes.
returns:
    Num: Likelyness rating of the Possible_Title matching any of the
    words of the Book Objects title
synopsis:
    The purpose of this function is to determine whether or not the
    Possible_Title matches any of the words within the Book Objects
    title
"""
def ____Compare_Book_Title(Possible_Title, Book_Object):
    Split_Title = Book_Object.title.split()

    for Split in Split_Title:
        if Possible_Title == Split.lower():
            return 100
    
    Score = 0.0

    for Split in Split_Title:
        if Possible_Title in Split.lower():
            if Score < __Difference_Calculation(Possible_Title, Split.lower()):
                Score = __Difference_Calculation(Possible_Title, Split.lower())
    return Score

"""
args:
    SplitString (List of Strings): List of Strings that will be compared
    to every aspect of the book object to determine how well it matches
    the Book Object.
    Book_Object (Book Object): Book Object that is going to be checked for
    how well it matches.
returns:
    Num: End result of Likelyness rating that was calculated
synopsis:
    The purpose of this function is to determine whether or not the List of Strings
    matches the apporpriate paramaters for a Book Object
"""
def __Compare_Book(SplitString, Book_Object):
    TotalScore = 0.0

    for Split in SplitString:
        TempScore = 0.0
        #Check ISBN
        if ____Compare_Book_ISBN(Split, Book_Object) == 100:
            return 1

        #Check Title
        if TempScore < ____Compare_Book_Title(Split, Book_Object):
            TempScore = ____Compare_Book_Title(Split, Book_Object)
        
        #Check Authors
        if TempScore < ____Compare_Book_Authors(Split, Book_Object):
            TempScore = ____Compare_Book_Authors(Split, Book_Object)
        TotalScore += TempScore
    
    TotalPossible = 100 * __Total_Checks(Book_Object)
    TotalScore = TotalScore / TotalPossible
    
    return round(TotalScore, 3)

"""
args:
    SplitString (List of Strings): List of Strings that will be checked for
    duplicates
returns:
    List of Strings: SplitString but with duplicates removed.
synopsis:
    The purpose of this function is to remove any duplicates that are gived
    to it within a list of strings
"""
def __Remove_Duplicates(SplitString):
    UniqueSplit = []
    for Split in SplitString:
        if Split not in UniqueSplit:
            UniqueSplit.append(Split)
    return UniqueSplit

"""
args:
    String (string): String that will be be converted to lowercase
returns:
    string: String that has been converted to lowercase
synopsis:
    The purpose of this function is to convert whatever string is
    given to it, to lowercase.
"""
def __Clean_Search(String):
    return String.lower()

"""
args:
    elem (element): double array that will be used for sorting
returns:
    elem[1]: returns whatever is within elem[1]
synopsis:
    The purpose of this function is to return whatever is within
    the second element of the list.  This is primarily used for
    sorting based upon the second element of the list.
"""
def __Sort_By_Rating(elem):
    return elem[1]

"""
args:
    String (string): String that will be used to check the database
    for any likely candidates
returns:
    Double List (Book Object, Num): sorted list with a book object and a
    likelyness rating
synopsis:
    The purpose of this function is to return a list of book objects with
    corresponding ratings that are based upon the likelyness that the
    book object matches whatever string was given.
"""
def Search_Query(String):
    String = __Clean_Search(String)
    SplitString = __Remove_Duplicates(String.split())
    
    Book_Objects = __Get_All_Book_Objects()

    Book_Ratings = []

    for Book_Object in Book_Objects:
        Book_Ratings.append([Book_Object, __Compare_Book(SplitString, Book_Object)])
    Book_Ratings.sort(key=__Sort_By_Rating, reverse=True)
    return Book_Ratings
    
#print(Search_Query("an assassin simon harrak i forgot to kiss"))