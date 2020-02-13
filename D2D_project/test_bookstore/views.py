from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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



def search(request):

    """
    if not request.method == 'POST':
        if 'search-persons-post' in request.session:
            request.POST = request.session['search-persons-post']
            request.method = 'POST'
            """
    
    if request.method == 'POST' or 'page' in request.GET:

        form = searchBar(request.POST)

        if form.is_valid():

            searcher = form.cleaned_data['searcher']

            results = Search_Query(searcher)

            paginator = Paginator(results, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'page_obj': page_obj,
                'results': results,
                'form': form,
                }
    else:
        
        form = searchBar()
        context = {
        'form': form,
        }

            
    

    return render(request, 'test_bookstore/search.html', context=context)


class bookDetail(generic.DetailView):
    model = Book

    def detail(self, request, primary_key):
        template = loader.get_template('test_bookstore/book_detail.html')

        book = get_object_or_404(Book, pk=primary_key)

        context = {
            'book': book
            }

        return render(request, 'test_bookstore/book_detail.html', context=context)
