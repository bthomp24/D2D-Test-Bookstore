from lxml import etree
from .models import Book
from bs4 import BeautifulSoup


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
        bookIsAvailable=[]
      

        for book in bookList:
            #parse ISBN 13 of the current book 
            isbn =  book.xpath(".//ns:ProductIdentifier[ns:ProductIDType = '15']/ns:IDValue", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            isbnBuffer = isbn[0].text
            if (len(isbnBuffer)<13):
                isbnBuffer = '978'+ isbnBuffer
            bookIsbn.insert(i,isbnBuffer)

            #parse title of the current book
            title =  book.xpath(".//ns:TitleElement[ns:SequenceNumber = '1']/ns:TitleText", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            bookTitle.insert(i, title[0].text)

            #parse the Series title of the book if it exists
            seriesTitle =  book.xpath(".//ns:Collection/ns:TitleDetail/ns:TitleElement[ns:SequenceNumber = '2']/ns:TitleText", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(seriesTitle)>0):
                bookSeriesTitle.insert(i, seriesTitle[0].text)
            else:
                bookSeriesTitle.insert(i, "None")

            #parse the volume number of the series if exists
            volumeNumber =  book.xpath(".//ns:Collection/ns:TitleDetail/ns:TitleElement[ns:SequenceNumber = '3']/ns:PartNumber", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
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
                        bookSecondaryAuthor[i] = secondaryAuthor[n].text+", "+bookSecondaryAuthor[i]
                        n=n-1
            else:
                bookSecondaryAuthor.insert(i, "None")

            #parse the description of the book if it exist
            description = book.xpath(".//ns:CollateralDetail/ns:TextContent[ns:TextType='03']/ns:Text", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(description)>0):
                #buffer = BeautifulSoup(description[0].text)
                #formatDescription = buffer.get_text()
                formatDescription = description[0].text
                bookDescription.insert(i, formatDescription)
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
                date = releaseDate[0].text
                formattedDate = date[0:4]+"/"+date[4:6]+"/"+date[-2:]
                bookReleaseDate.insert(i, formattedDate)
            else:
                bookReleaseDate.insert(i, "None")

            #parse the price of the book
            price =  book.xpath(".//ns:Price[ns:PriceType = '01']/ns:PriceAmount", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(price)>0):
                formatPrice = "$ " + price[0].text
                bookPrice.insert(i, formatPrice)
            else:
                bookPrice.insert(i, "None")

            #parse the info on is book is available for sale
            isAvailable = book.xpath(".//ns:PublishingDetail/ns:PublishingStatus", namespaces={'ns':'http://ns.editeur.org/onix/3.0/reference'})
            if (len(isAvailable)>0):
                print(isAvailable[0].text)
                if (isAvailable[0].text== '04'):
                    bookIsAvailable.insert(i, True)
                elif(isAvailable[0].text =='07'):
                    bookIsAvailable.insert(i, False)    
            else:
                bookIsAvailable.insert(i, False)

            try:
                checkBook = Book.objects.get(ISBN=bookIsbn[i])
                
                checkBook.ISBN = bookIsbn[i]
                checkBook.title = bookTitle[i]
                checkBook.primary_author = bookPrimaryAuthor[i]
                checkBook.series = bookSeriesTitle[i]
                checkBook.volume_number = bookVolumeNumber[i]
                checkBook.secondary_authors = bookSecondaryAuthor[i]
                checkBook.description = bookDescription[i]
                checkBook.release_date = bookReleaseDate[i]
                checkBook.price = bookPrice[i]
                checkBook.publisher = bookPublisher[i]
                checkBook.is_available = bookIsAvailable[i]
                checkBook.save() 
            except:    
                Book.objects.create(
                 ISBN = bookIsbn[i],
                 title = bookTitle[i],
                 primary_author = bookPrimaryAuthor[i],
                 series = bookSeriesTitle[i],
                 volume_number = bookVolumeNumber[i],
                 secondary_authors = bookSecondaryAuthor[i],
                 description = bookDescription[i],
                 release_date = bookReleaseDate[i],
                 price = bookPrice[i],
                 publisher = bookPublisher[i],
                 is_available = bookIsAvailable[i]
                 )
                 
            i= i+1

        if (i)==len(bookList):
            return 1
        else:
            return 0
           

if __name__ == "__main__":
    parseXML("onix3.xml")