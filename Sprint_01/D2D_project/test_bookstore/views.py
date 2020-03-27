from django.shortcuts import render, get_object_or_404

from django.template import loader, RequestContext
from django.views import generic

from django_tables2.config import RequestConfig

# Create your views here.
from rest_framework import viewsets

from .serializers import BookSerializer
from .models import Book

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .onix_parse import parseXML

from .models import File
import os

from .models import Book
from .tables import ResultsTable
from .forms import searchBar

from .search import Search_Query


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessXML(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):

        if (parseXML('media/onix3.xml')==1):
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)



"""
args:
    Http request: Requests from either POST or GET. Will
    be used for list display, searcher, and to paginate.
returns:
    An Http Render: A render of the Search Bar Form and
    Results Table to be displayed in "search.html"
synopsis:
    The view serves as the search page as well as listing
    the search results from the query made. It will also
    provide options to visit each individual entry with a
    "details" link. It will contain all the books from the
    database and list them accordingly with no cut off point,
    though one could be implemented in the future.
"""
def search(request):

    # empty list that will hold our search display data for
    # the ResultsTable    
    results_display = []
    results = ""
    # POST forcer for our "page" GET request. So we can
    # access our old POST data when we move to the next page.
    if not request.method == 'POST' and 'page' in request.GET:
        if 'searcher' in request.session:
            request.POST = request.session['searcher']
            request.method = 'POST'

    
    if request.method == 'POST':

        # Acquiring the user's input on the search bar
        form = searchBar(request.POST)
        request.session['searcher'] = request.POST

        # checking data and using it for our Search_Query function.
        if form.is_valid():

            searcher = form.cleaned_data['searcher']

            # Receiving results in a list of [Book Object, float]
            results = Search_Query(searcher)


            # Loop for constructing the list of dictionaries to build our ResultsTable
            for books in results:
                if float(books[1])> float(0) and getattr(books[0], "is_available"):
                    dicts = {}
                    dicts["title"] = getattr(books[0], "title")
                    dicts["author"] = getattr(books[0], "primary_author")
                    dicts["ISBN"] = getattr(books[0], "ISBN")
                    dicts["rating"] = books[1]
                    results_display.append(dicts)            
    else:
        # Purposes of hiding the list until a query is made.
        form = searchBar()

    # Building our Results Table from the list of dictionary data.
    # and creating the paginator for the results.
    results_table = ResultsTable(results_display)
    RequestConfig(request, paginate={"per_page": 10}).configure(results_table)

    context = {
        'table': results_table,
        'results': results,
        'form': form,
    }

    return render(request, 'test_bookstore/search.html', context=context)


"""
args:
    generic Detail View: for creating the Book Detail class view
returns:
    not applicable
synopsis:
    This is the class that will allow direct mapping to our
    database for displaying book details in the book detail
    view. This will simplify the connections and it's primary
    function will be responsible for location and passing in the
    render.
"""
class bookDetail(generic.DetailView):
    model = Book

    """
    args:
        Http request: to acquire the request from the browser to
        open the page.
        primary key: This will be the key we use to locate the
        specific book in the database that the user was wanting to
        see the details about.
    returns:
        An Http Render: This render will be for our book data's context
        as well as directing to the 'book_detail.html' file.
    synopsis:
        This is our other page whose purpose is to display the
        various bits of information about books from the database.
        To reach this page, a user must click on the "details" link
        from their queries and will be brought to the details page with
        all the book data displayed accordingly.
    """
    def detail(self, request, primary_key):

        book = get_object_or_404(Book, pk=primary_key)

        context = {
            'book': book
            }

        return render(request, 'test_bookstore/book_detail.html', context=context)
