import django_tables2 as tables
from django_tables2.utils import A
from django_tables2.tables import Table
from .models import Book

"""
args:
    a DjangoTable2 Table: This is our constructor for creating
    the table that will dispaly the search results and rating number.
returns:
    not applicable
synopsis:
    This table is designed to display the search results from a user
    query made in the search bar on the search page. The results will
    be displayed in a table format with the five rows. There will be only
    a "search results" displayed for a header
"""
class ResultsTable(tables.Table):

    title = tables.Column('Search Results')
    author = tables.Column("Author")
    ISBN = tables.Column("ISBN")
    rating = tables.Column("Rating")

    # Constructing our links to the book details page in the form of a 5th column
    book_details = tables.LinkColumn('test_bookstore:book_detail', args=[A("ISBN")], orderable=False, empty_values=())

    class Meta:
        attr = {"class" : "search_table"}
        orderable = False
         
    
        
    # This function's purpose is to display the "Detail" name for the links
    # underneath the "Book_Details" column header.   
    def render_book_details(self):
        return 'Detail'
