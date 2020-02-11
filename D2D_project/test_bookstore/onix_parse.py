from lxml import etree
from .models import Book


def parseXML(xmlFile):

        root = etree.parse(xmlFile)
        bookList = root.xpath(".//ns:Product", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
        bookQuantity = len(bookList)

        i = 0 #counter

        #lists to store book attributes according to book's index number 
        bookIsbn=[]
        bookTitle=[] 
        bookSeriesTitle = []
        bookVolumeNumber=[]
        bookPrimaryAuthor=[]
        bookSecondaryAuthor=[]
        bookDescription = []
        bookPublisher=[]
        bookReleaseDate=[]
        bookPrice =[]
        book_dict = {}

        for book in bookList:
            #parse ISBN 13 of the current book 
            isbn =  book.xpath(".//ns:ProductIdentifier[ns:ProductIDType = '15']/ns:IDValue", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            bookIsbn.insert(i,isbn[0].text)

            #parse title of the current book
            title =  book.xpath(".//ns:TitleElement[ns:SequenceNumber = '1']/ns:TitleText", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            bookTitle.insert(i, title[0].text)

            #parse the Series title of the book if it exists
            seriesTitle =  book.xpath(".//ns:TitleElement[ns:SequenceNumber = '2']/ns:TitleText", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(seriesTitle)>0):
                bookSeriesTitle.insert(i, seriesTitle[0].text)
            else:
                bookSeriesTitle.insert(i, "None")

            #parse the volume number of the series if exists
            volumeNumber =  book.xpath(".//ns:TitleElement[ns:SequenceNumber = '3']/ns:PartNumber", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if(len(volumeNumber)>0):
                bookVolumeNumber.insert(i, volumeNumber[0].text)
            else:
                bookVolumeNumber.insert(i, "None")

            #parse the author of the current book
            primaryAuthor =  book.xpath(".//ns:Contributor[ns:SequenceNumber = '1']/ns:PersonName", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(primaryAuthor)>0):
                bookPrimaryAuthor.insert(i, primaryAuthor[0].text)
            else:
                bookPrimaryAuthor.insert(i, "None")

            #parse co-author/s of the book if exists
            secondaryAuthor = book.xpath(".//ns:Contributor[ns:SequenceNumber>1]/ns:PersonName", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(secondaryAuthor)>0):
                bookSecondaryAuthor.insert(i, secondaryAuthor[0].text)
                if (len(secondaryAuthor)>1):
                    n = len(secondaryAuthor)-1
                    while n>=1:
                        bookSecondaryAuthor[i] = bookSecondaryAuthor[i] +" "+ secondaryAuthor[n].text
                        n=n-1;
            else:
                bookSecondaryAuthor.insert(i, "None")

            #parse the description of the book if it exist
            description = book.xpath(".//ns:CollateralDetail/ns:TextContent[ns:TextType='03']/ns:Text", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(description)>0):
                bookDescription.insert(i, description[0].text)
            else:
                bookDescription.insert(i, "None")
            
            #parse the publisher of the book
            publisher = book.xpath(".//ns:PublishingDetail/ns:Publisher[ns:PublishingRole = '01']/ns:PublisherName", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(publisher)>0):
                bookPublisher.insert(i, publisher[0].text)
            else:
                bookPublisher.insert(i, "None")
            
            #parse the release date of the book
            releaseDate = book.xpath(".//ns:PublishingDetail/ns:PublishingDate[ns:PublishingDateRole = '01']/ns:Date", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(releaseDate)>0):
                bookReleaseDate.insert(i, releaseDate[0].text)
            else:
                bookReleaseDate.insert(i, "None")

            #parse the price of the book
            price =  book.xpath(".//ns:Price[ns:PriceType = '01']/ns:PriceAmount", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(price)>0):
                bookPrice.insert(i, price[0].text)
            else:
                bookPrice.insert(i, "None")

            Book.objects.create(
                 ISBN = bookIsbn[i],
                 title = bookTitle[i],
                 primary_author = bookPrimaryAuthor[i],
                 series = bookSeriesTitle[i],
                 volume_number = bookVolumeNumber[i],
                 secondary_authors = bookSecondaryAuthor[i],
                 description = bookDescription[i],
                 releaseDate = bookReleaseDate[i],
                 price = bookPrice[i]
                 )

            book_dict[bookIsbn[i]]= (bookIsbn[i], bookTitle[i], bookPrimaryAuthor[i])
            i= i+1

        
        for n in range(i):
            print("\n")
            print("\n")
            print("Book #", n)
            print("ISBN:13:", bookIsbn[n])
            print("Title:", bookTitle[n])
            print("Series Title:", bookSeriesTitle[n])
            print("Volume #:",bookVolumeNumber[n])
            print("Author:", bookPrimaryAuthor[n])
            print("Co-Authors:", bookSecondaryAuthor[n])
            print("Descritption:",bookDescription[n])
            print("Publisher:", bookPublisher[n])
            print("Release Date:", bookReleaseDate[n])
            print("Price:", bookPrice[n])
           

        print (book_dict)

if __name__ == "__main__":
    parseXML("kobo.xml")